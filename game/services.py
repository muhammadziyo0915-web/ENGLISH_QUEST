from django.db import transaction
from django.db.models import F
from django.utils import timezone

from .models import Inventory
from .shop import HEART_MAX, HEART_REGEN_SECONDS


def qty(user, item):
    inv = Inventory.objects.filter(user=user, item=item).first()
    return inv.qty if inv else 0


def inventory_map(user):
    return {i.item: i.qty for i in Inventory.objects.filter(user=user)}


def add_item(user, item, n=1):
    inv, _ = Inventory.objects.get_or_create(user=user, item=item)
    Inventory.objects.filter(pk=inv.pk).update(qty=F('qty') + n)


def consume(user, item):
    """Zaxiradan 1 ta ishlatadi. Bor bo'lsa True qaytaradi."""
    with transaction.atomic():
        inv = Inventory.objects.filter(user=user, item=item, qty__gt=0).first()
        if not inv:
            return False
        Inventory.objects.filter(pk=inv.pk).update(qty=F('qty') - 1)
        return True


def regen_hearts(p):
    """Yuraklar vaqt o'tishi bilan qaytadi (har HEART_REGEN_SECONDS da 1 ta)."""
    now = timezone.now()
    if p.hearts >= HEART_MAX:
        if p.hearts_at is not None:
            p.hearts_at = None
            p.save(update_fields=['hearts_at'])
        return
    if p.hearts_at is None:
        p.hearts_at = now
        p.save(update_fields=['hearts_at'])
        return
    gained = int((now - p.hearts_at).total_seconds() // HEART_REGEN_SECONDS)
    if gained > 0:
        p.hearts = min(HEART_MAX, p.hearts + gained)
        p.hearts_at = None if p.hearts >= HEART_MAX else p.hearts_at + timezone.timedelta(seconds=gained * HEART_REGEN_SECONDS)
        p.save(update_fields=['hearts', 'hearts_at'])


def seconds_to_next_heart(p):
    if p.hearts >= HEART_MAX or p.hearts_at is None:
        return 0
    passed = (timezone.now() - p.hearts_at).total_seconds()
    return max(0, int(HEART_REGEN_SECONDS - passed))
