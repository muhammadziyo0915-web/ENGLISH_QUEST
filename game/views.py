import random
import time

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, redirect, render

from django.contrib import messages
from django.utils import timezone

from .models import Stage, Question, Progress, Profile
from . import services as svc
from .shop import (HEART_MAX, PASS_COINS, PASS_SCORE, PERFECT_BONUS, REPLAY_RATE)

QUIZ_SECONDS = 5 * 60
QUESTION_COUNT = 20


def get_progress(request):
    if not request.user.is_authenticated:
        return None
    p, _ = Progress.objects.get_or_create(user=request.user)
    Profile.objects.get_or_create(user=request.user)
    svc.regen_hearts(p)
    return p


def home(request):
    return render(request, "home.html", {"p": get_progress(request)})


def register(request):
    if request.user.is_authenticated:
        return redirect("home")
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        Progress.objects.create(user=user)
        login(request, user)
        return redirect("stages")
    return render(request, "registration/register.html", {"form": form})


def stages(request):
    p = get_progress(request)
    return render(
        request,
        "stages.html",
        {
            "stages": Stage.objects.filter(is_active=True),
            "unlocked": p.unlocked_stage if p else 1,
            "passed": p.passed_set() if p else set(),
            "p": p,
        },
    )


def _attempt_key(number):
    return f"english_quest_attempt_{number}"


def _start_attempt(request, stage):
    questions = list(stage.questions.all())
    random.shuffle(questions)
    questions = questions[:QUESTION_COUNT]
    attempt = {
        "ids": [q.id for q in questions],
        "answers": {},
        "started": time.time(),
    }
    request.session[_attempt_key(stage.number)] = attempt
    request.session.modified = True


def _get_attempt(request, stage):
    return request.session.get(_attempt_key(stage.number))


def _remaining(attempt):
    elapsed = max(0, int(time.time() - float(attempt["started"])))
    return max(0, QUIZ_SECONDS + int(attempt.get("bonus", 0)) - elapsed)


def _finish_attempt(request, stage, attempt, timed_out=False):
    ids = attempt.get("ids", [])
    answers = attempt.get("answers", {})
    questions = list(Question.objects.filter(stage=stage, id__in=ids))
    by_id = {q.id: q for q in questions}

    score = 0
    results = []
    for qid in ids:
        q = by_id.get(qid)
        if not q:
            continue
        selected = answers.get(str(qid), "")
        correct = selected == q.correct
        if correct:
            score += 1
        selected_text = dict(q.options()).get(selected, "Javob berilmagan")
        correct_text = dict(q.options()).get(q.correct, "")
        results.append(
            {
                "number": len(results) + 1,
                "word": q.prompt,
                "selected": selected_text,
                "correct_answer": correct_text,
                "ok": correct,
                "meaning": q.explanation,
            }
        )

    p = get_progress(request)
    unlocked = False
    replay = False
    xp_gained = coins_gained = 0
    notes = []
    if p:
        passed = score >= PASS_SCORE
        if not passed and score == PASS_SCORE - 1 and svc.consume(request.user, "shield"):
            passed = True
            notes.append("🛡 Qalqon ishlatildi: Unit o‘tilgan hisoblandi")
        if passed:
            replay = stage.number in p.passed_set()
            xp_gained = stage.xp
            coins_gained = PASS_COINS
            if score == len(ids) and len(ids) > 0:
                coins_gained += PERFECT_BONUS
                notes.append("🌟 Mukammal natija: bonus coin")
            if replay:
                # Oldin o'tilgan Unit: 20% XP va coin. Boosterlar sarflanmaydi.
                xp_gained = max(1, round(xp_gained * REPLAY_RATE))
                coins_gained = max(1, round(coins_gained * REPLAY_RATE))
                notes.append("🔁 Takrorlash: XP va coin 20% hisoblandi")
            else:
                if svc.consume(request.user, "xp2"):
                    xp_gained *= 2
                    notes.append("⚡ XP x2 ishlatildi")
                if svc.consume(request.user, "coin2"):
                    coins_gained *= 2
                    notes.append("🪙 Coin x2 ishlatildi")
                p.completed += 1
                p.mark_passed(stage.number)
            p.unlocked_stage = max(p.unlocked_stage, stage.number + 1)
            p.xp += xp_gained
            p.coins += coins_gained
            p.streak += 1
            unlocked = True
        else:
            if svc.consume(request.user, "freeze"):
                notes.append("🧊 Streak himoyasi ishlatildi: streak saqlandi")
            else:
                p.streak = 0
            if p.hearts >= HEART_MAX:
                p.hearts_at = timezone.now()
            p.hearts = max(0, p.hearts - 1)
        p.best_score = max(p.best_score, score)
        p.save()

    result = {
        "stage_number": stage.number,
        "score": score,
        "total": len(ids),
        "wrong": len(ids) - score,
        "results": results,
        "timed_out": timed_out,
        "unlocked": unlocked,
        "replay": replay,
        "xp_gained": xp_gained,
        "coins_gained": coins_gained,
        "notes": notes,
        "final_unit": stage.number == Stage.objects.filter(is_active=True).count(),
    }
    request.session[_attempt_key(stage.number)] = None
    request.session["english_quest_last_result"] = result
    request.session.modified = True
    return redirect("result")


def start_stage(request, number):
    stage = get_object_or_404(Stage, number=number, is_active=True)
    p = get_progress(request)
    unlocked = p.unlocked_stage if p else 1
    if number > unlocked:
        return redirect("stages")

    if p and p.hearts <= 0:
        messages.error(request, "Yuraklaringiz tugadi ❤️ Biroz kuting yoki do‘kondan yurak sotib oling.")
        return redirect("shop")

    # Every fresh entry starts a brand-new 5-minute randomized attempt.
    _start_attempt(request, stage)
    return redirect("play_question", number=number, qno=1)


def play_question(request, number, qno):
    stage = get_object_or_404(Stage, number=number, is_active=True)
    p = get_progress(request)
    unlocked = p.unlocked_stage if p else 1
    if number > unlocked:
        return redirect("stages")

    attempt = _get_attempt(request, stage)
    if not attempt or not attempt.get("ids"):
        return redirect("start_stage", number=number)

    if qno < 1 or qno > len(attempt["ids"]):
        return redirect("start_stage", number=number)

    remaining = _remaining(attempt)
    if remaining <= 0:
        return _finish_attempt(request, stage, attempt, timed_out=True)

    qid = attempt["ids"][qno - 1]
    question = get_object_or_404(Question, id=qid, stage=stage)

    if request.method == "POST":
        selected = request.POST.get("answer", "")
        if selected in {"A", "B", "C", "D"}:
            attempt["answers"][str(question.id)] = selected
        request.session[_attempt_key(stage.number)] = attempt
        request.session.modified = True

        if _remaining(attempt) <= 0 or qno >= len(attempt["ids"]):
            return _finish_attempt(
                request, stage, attempt, timed_out=_remaining(attempt) <= 0
            )
        return redirect("play_question", number=number, qno=qno + 1)

    word_text, pronunciation = question.prompt, ""
    if " (" in question.prompt and question.prompt.endswith(")"):
        word_text, pronunciation = question.prompt.rsplit(" (", 1)
        pronunciation = pronunciation[:-1]

    return render(
        request,
        "play.html",
        {
            "stage": stage,
            "question": question,
            "word_text": word_text,
            "pronunciation": pronunciation,
            "qno": qno,
            "total": len(attempt["ids"]),
            "remaining": remaining,
            "p": p,
            "replay": bool(p and number in p.passed_set()),
            "hidden": attempt.get("fifty", {}).get(str(question.id), []),
            "inv": svc.inventory_map(request.user) if request.user.is_authenticated else {},
        },
    )


def result(request):
    data = request.session.get("english_quest_last_result")
    if not data:
        return redirect("stages")
    p = get_progress(request)
    stage = get_object_or_404(Stage, number=data["stage_number"])
    return render(request, "result.html", {"data": data, "stage": stage, "p": p})


def book(request):
    words = [
        ("school", "maktab", "skul"), ("teacher", "o‘qituvchi", "ti-chər"),
        ("student", "o‘quvchi", "styu-dənt"), ("family", "oila", "fe-mə-li"),
        ("friend", "do‘st", "frend"), ("house", "uy", "haus"),
        ("room", "xona", "ruːm"), ("food", "ovqat", "fuːd"),
        ("water", "suv", "wo-tər"), ("breakfast", "nonushta", "brek-fəst"),
        ("morning", "ertalab", "mor-ning"), ("evening", "kechqurun", "iːv-ning"),
        ("happy", "xursand", "he-pi"), ("tired", "charchagan", "taiər"),
        ("learn", "o‘rganmoq", "lörn"), ("speak", "gapirmoq", "spiːk"),
        ("listen", "tinglamoq", "lis-n"), ("write", "yozmoq", "rait"),
        ("read", "o‘qimoq", "riːd"), ("travel", "sayohat qilmoq", "trevəl"),
    ]
    return render(request, "book.html", {"words": words})


@login_required
def profile(request):
    p = get_progress(request)
    profile_obj, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        bio = request.POST.get("bio", "").strip()[:500]
        profile_obj.bio = bio
        if request.FILES.get("avatar"):
            profile_obj.avatar = request.FILES["avatar"]
        profile_obj.save()
        return redirect("profile")
    return render(request, "profile.html", {"p": p, "profile_obj": profile_obj, "level": min(180, p.unlocked_stage)})
