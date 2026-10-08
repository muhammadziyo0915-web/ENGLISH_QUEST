from django.db import migrations, models
import django.db.models.deletion
import django.contrib.auth.models

class Migration(migrations.Migration):
    initial = True
    dependencies = [('auth','0012_alter_user_first_name_max_length')]
    operations = [
        migrations.CreateModel(name='Stage', fields=[('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),('number',models.PositiveIntegerField(unique=True)),('title',models.CharField(max_length=120)),('topic',models.CharField(max_length=180)),('level',models.CharField(default='Beginner',max_length=30)),('xp',models.PositiveIntegerField(default=100)),('badge',models.CharField(default='⭐',max_length=80)),('is_active',models.BooleanField(default=True))], options={'ordering':['number']}),
        migrations.CreateModel(name='Question', fields=[('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),('prompt',models.TextField()),('option_a',models.CharField(max_length=200)),('option_b',models.CharField(max_length=200)),('option_c',models.CharField(max_length=200)),('option_d',models.CharField(max_length=200)),('correct',models.CharField(max_length=1)),('explanation',models.CharField(blank=True,max_length=300)),('stage',models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name='questions',to='game.stage'))]),
        migrations.CreateModel(name='Progress', fields=[('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),('unlocked_stage',models.PositiveIntegerField(default=1)),('xp',models.PositiveIntegerField(default=0)),('streak',models.PositiveIntegerField(default=0)),('hearts',models.PositiveIntegerField(default=5)),('coins',models.PositiveIntegerField(default=0)),('best_score',models.PositiveIntegerField(default=0)),('completed',models.PositiveIntegerField(default=0)),('user',models.OneToOneField(on_delete=django.db.models.deletion.CASCADE,to='auth.user'))])
    ]
