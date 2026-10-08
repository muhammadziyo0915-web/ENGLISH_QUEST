import random

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from . import services as svc
from .models import Profile, Progress, Stage
from .shop import (BY_KEY, DAILY_BASE, DAILY_STREAK_BONUS, HEART_MAX, ITEMS, KIND_LABEL,
                   LOOT_TABLE, TABS)
from .views import _get_attempt, _remaining, get_progress, QUIZ_SECONDS


def _daily_state(p):
    today = timezone.localdate()
    can = p.last_daily != today
    nxt = p.daily_streak + 1 if (p.last_daily == today - timezone.timedelta(days=1)) else 1
    reward = DAILY_BASE + min(nxt - 1, 7) * DAILY_STREAK_BONUS
    return can, reward


@login_required
def shop(request):
    p = get_progress(request)
    profile = request.user.profile
    inv = svc.inventory_map(request.user)
    cards = []
    for it in ITEMS:
        c = dict(it)
        c['owned'] = inv.get(it['key'], 0)
        c['equipped'] = False
        if it['kind'] in ('frame', 'title', 'theme'):
            c['has'] = c['owned'] > 0
            c['equipped'] = getattr(profile, it['kind']) == it['key']
            c['label'] = KIND_LABEL[it['kind']]
        c['afford'] = p.coins >= it['price']
        c['missing'] = max(0, it['price'] - p.coins)
        cards.append(c)
    can_daily, daily_reward = _daily_state(p)
    return render(request, 'shop.html', {
        'p': p, 'cards': cards, 'tabs': TABS, 'profile_obj': profile,
        'can_daily': can_daily, 'daily_reward': daily_reward,
        'next_heart': svc.seconds_to_next_heart(p), 'hearts_max': HEART_MAX,
        'max_stage': Stage.objects.filter(is_active=True).count(),
    })


def _roll_loot():
    total = sum(w for w, _, _ in LOOT_TABLE)
    r = random.uniform(0, total)
    acc = 0
    for w, kind, val in LOOT_TABLE:
        acc += w
        if r <= acc:
            return kind, val
    return LOOT_TABLE[0][1], LOOT_TABLE[0][2]


@login_required
@require_POST
def buy(request):
    key = request.POST.get('item', '')
    it = BY_KEY.get(key)
    if not it:
        messages.error(request, 'Bunday mahsulot yo‘q.')
        return redirect('shop')
    with transaction.atomic():
        p = Progress.objects.select_for_update().get(user=request.user)
        svc.regen_hearts(p)
        kind = it['kind']
        if kind in ('frame', 'title', 'theme') and svc.qty(request.user, key) > 0:
            messages.info(request, 'Bu narsa sizda allaqachon bor.')
            return redirect('shop')
        if p.coins < it['price']:
            messages.error(request, f"Coin yetarli emas: yana {it['price'] - p.coins} 🪙 kerak.")
            return redirect('shop')
        if key == 'heart1' and p.hearts >= HEART_MAX:
            messages.info(request, 'Yuraklaringiz allaqachon to‘la ❤️')
            return redirect('shop')
        if key == 'heart_full' and p.hearts >= HEART_MAX:
            messages.info(request, 'Yuraklaringiz allaqachon to‘la ❤️')
            return redirect('shop')

        p.coins -= it['price']
        if key == 'heart1':
            p.hearts += 1
            msg = '❤️ +1 yurak qo‘shildi.'
        elif key == 'heart_full':
            p.hearts = HEART_MAX
            msg = '💖 Yuraklar to‘ldirildi.'
        elif key == 'lootbox':
            kind_, val = _roll_loot()
            if kind_ == 'coin':
                p.coins += val
                msg = f'🎁 Qutidan {val} 🪙 chiqdi!' + (' Yutdingiz!' if val > it['price'] else '')
            else:
                svc.add_item(request.user, val, 1)
                msg = f"🎁 Qutidan sovg‘a: {BY_KEY[val]['icon']} {BY_KEY[val]['name']}!"
        else:
            svc.add_item(request.user, key, 1)
            msg = f"✅ {it['icon']} {it['name']} sotib olindi."
            if kind in ('frame', 'title', 'theme'):
                msg += ' Endi “Kiyish” tugmasini bosing.'
        if p.hearts >= HEART_MAX:
            p.hearts_at = None
        p.save()
    messages.success(request, msg)
    return redirect('shop')


@login_required
@require_POST
def equip(request):
    key = request.POST.get('item', '')
    kind = request.POST.get('kind', '')
    if kind not in ('frame', 'title', 'theme'):
        return redirect('shop')
    profile = request.user.profile
    if key == '':
        setattr(profile, kind, '')
        profile.save()
        messages.success(request, 'Standart holatga qaytarildi.')
        return redirect('shop')
    it = BY_KEY.get(key)
    if not it or it['kind'] != kind or svc.qty(request.user, key) < 1:
        messages.error(request, 'Avval uni sotib olishingiz kerak.')
        return redirect('shop')
    setattr(profile, kind, key)
    profile.save()
    messages.success(request, f"{it['icon']} {it['name']} kiyildi.")
    return redirect('shop')


@login_required
@require_POST
def daily(request):
    with transaction.atomic():
        p = Progress.objects.select_for_update().get(user=request.user)
        can, reward = _daily_state(p)
        if not can:
            messages.info(request, 'Bugungi sovg‘ani olib bo‘lgansiz. Ertaga qaytib keling!')
            return redirect('shop')
        today = timezone.localdate()
        p.daily_streak = p.daily_streak + 1 if p.last_daily == today - timezone.timedelta(days=1) else 1
        p.last_daily = today
        p.coins += reward
        p.save()
    messages.success(request, f'🎉 Kunlik sovg‘a: +{reward} 🪙 (ketma-ket {p.daily_streak} kun)')
    return redirect('shop')


@login_required
@require_POST
def use_unlock(request):
    with transaction.atomic():
        p = Progress.objects.select_for_update().get(user=request.user)
        max_stage = Stage.objects.filter(is_active=True).count()
        if p.unlocked_stage >= max_stage:
            messages.info(request, 'Barcha Unitlar allaqachon ochiq.')
            return redirect('shop')
        if not svc.consume(request.user, 'unlock'):
            messages.error(request, 'Sizda Unit kaliti yo‘q.')
            return redirect('shop')
        p.unlocked_stage += 1
        p.save()
    messages.success(request, f'🗝 Unit {p.unlocked_stage} ochildi!')
    return redirect('shop')


@require_POST
def use_item(request):
    """Test paytida yordamchilarni ishlatish (AJAX)."""
    if not request.user.is_authenticated:
        return JsonResponse({'ok': False, 'msg': 'Avval tizimga kiring.'}, status=403)
    item = request.POST.get('item', '')
    try:
        number = int(request.POST.get('number', '0'))
        qno = int(request.POST.get('qno', '0'))
    except ValueError:
        return JsonResponse({'ok': False, 'msg': 'Noto‘g‘ri so‘rov.'}, status=400)
    if item not in ('time', 'fifty'):
        return JsonResponse({'ok': False, 'msg': 'Noto‘g‘ri yordamchi.'}, status=400)
    stage = Stage.objects.filter(number=number, is_active=True).first()
    attempt = _get_attempt(request, stage) if stage else None
    if not attempt or qno < 1 or qno > len(attempt.get('ids', [])):
        return JsonResponse({'ok': False, 'msg': 'Test topilmadi.'}, status=400)
    if _remaining(attempt) <= 0:
        return JsonResponse({'ok': False, 'msg': 'Vaqt tugagan.'})

    key = f'english_quest_attempt_{number}'
    if item == 'time':
        if attempt.get('time_used', 0) >= 2:
            return JsonResponse({'ok': False, 'msg': 'Bir testda 2 marta ishlatish mumkin.'})
        if not svc.consume(request.user, 'time'):
            return JsonResponse({'ok': False, 'msg': 'Sizda ⏱ yo‘q. Do‘kondan oling.'})
        attempt['bonus'] = int(attempt.get('bonus', 0)) + 60
        attempt['time_used'] = attempt.get('time_used', 0) + 1
        request.session[key] = attempt
        request.session.modified = True
        return JsonResponse({'ok': True, 'msg': '⏱ +1 daqiqa qo‘shildi!', 'remaining': _remaining(attempt),
                             'left': svc.qty(request.user, 'time')})

    # fifty
    from .models import Question
    qid = attempt['ids'][qno - 1]
    fifty = attempt.setdefault('fifty', {})
    if str(qid) in fifty:
        return JsonResponse({'ok': True, 'msg': 'Bu savolda 50/50 ishlatilgan.', 'hide': fifty[str(qid)],
                             'left': svc.qty(request.user, 'fifty')})
    q = Question.objects.filter(id=qid, stage=stage).first()
    if not q:
        return JsonResponse({'ok': False, 'msg': 'Savol topilmadi.'}, status=400)
    if not svc.consume(request.user, 'fifty'):
        return JsonResponse({'ok': False, 'msg': 'Sizda ✂️ yo‘q. Do‘kondan oling.'})
    wrong = [l for l in 'ABCD' if l != q.correct]
    hide = random.sample(wrong, 2)
    fifty[str(qid)] = hide
    request.session[key] = attempt
    request.session.modified = True
    return JsonResponse({'ok': True, 'msg': '✂️ 2 ta noto‘g‘ri variant olib tashlandi.', 'hide': hide,
                         'left': svc.qty(request.user, 'fifty')})
