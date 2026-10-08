from django.db import models
from django.contrib.auth.models import User


class Stage(models.Model):
    number = models.PositiveIntegerField(unique=True)
    title = models.CharField(max_length=120)
    topic = models.CharField(max_length=180)
    level = models.CharField(max_length=30, default='Beginner')
    xp = models.PositiveIntegerField(default=100)
    badge = models.CharField(max_length=80, default='⭐')
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['number']

    def __str__(self):
        return f'{self.number}. {self.title}'


class Question(models.Model):
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, related_name='questions')
    prompt = models.TextField()
    option_a = models.CharField(max_length=200)
    option_b = models.CharField(max_length=200)
    option_c = models.CharField(max_length=200)
    option_d = models.CharField(max_length=200)
    correct = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')])
    explanation = models.CharField(max_length=300, blank=True)

    def options(self):
        return [('A', self.option_a), ('B', self.option_b), ('C', self.option_c), ('D', self.option_d)]


class Progress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    unlocked_stage = models.PositiveIntegerField(default=1)
    xp = models.PositiveIntegerField(default=0)
    streak = models.PositiveIntegerField(default=0)
    hearts = models.PositiveIntegerField(default=5)
    coins = models.PositiveIntegerField(default=0)
    best_score = models.PositiveIntegerField(default=0)
    completed = models.PositiveIntegerField(default=0)
    hearts_at = models.DateTimeField(null=True, blank=True)
    last_daily = models.DateField(null=True, blank=True)
    daily_streak = models.PositiveIntegerField(default=0)
    passed_units = models.TextField(blank=True, default='')   # "1,2,3": haqiqatan o'tilgan Unitlar

    def passed_set(self):
        return {int(x) for x in self.passed_units.split(',') if x.strip().isdigit()}

    def mark_passed(self, number):
        s = self.passed_set()
        s.add(number)
        self.passed_units = ','.join(str(x) for x in sorted(s))

    def __str__(self):
        return self.user.username


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    frame = models.CharField(max_length=30, blank=True, default='')
    title = models.CharField(max_length=30, blank=True, default='')
    theme = models.CharField(max_length=30, blank=True, default='')

    @property
    def title_name(self):
        from .shop import TITLE_NAMES
        return TITLE_NAMES.get(self.title, '')

    def __str__(self):
        return f'Profile: {self.user.username}'


class Inventory(models.Model):
    """Foydalanuvchi sotib olgan narsalar (yordamchilar soni, ramka/unvon/mavzu = 1)."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inventory')
    item = models.CharField(max_length=30)
    qty = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('user', 'item')

    def __str__(self):
        return f'{self.user.username}: {self.item} x{self.qty}'
