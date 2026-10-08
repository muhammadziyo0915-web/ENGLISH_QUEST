"""Do'kon katalogi. Narxlar va nomlarni shu yerdan o'zgartirsangiz bo'ladi."""

HEART_MAX = 5
HEART_REGEN_SECONDS = 10 * 60      # har 10 daqiqada 1 ta yurak qaytadi

TABS = [
    ('all', 'Hammasi'),
    ('help', 'Yordamchilar'),
    ('frame', 'Ramkalar'),
    ('title', 'Unvonlar'),
    ('theme', 'Mavzular'),
    ('luck', 'Omad'),
]

# kind: instant (darhol), consumable (zaxirada saqlanadi), frame/title/theme (doimiy, kiyiladi)
ITEMS = [
    # ---- Yordamchilar ----
    dict(key='heart1', kind='instant', tab='help', icon='❤️', name='+1 yurak', price=25,
         desc='Darhol 1 ta yurak qo‘shadi (eng ko‘pi bilan 5 ta).'),
    dict(key='heart_full', kind='instant', tab='help', icon='💖', name='Yuraklarni to‘ldirish', price=100,
         desc='Barcha yuraklarni 5 taga to‘ldiradi.'),
    dict(key='time', kind='consumable', tab='help', icon='⏱', name='+1 daqiqa', price=40,
         desc='Test paytida tugmani bosing: vaqtga +60 soniya. Bir testda 2 martagacha.'),
    dict(key='fifty', kind='consumable', tab='help', icon='✂️', name='50/50', price=35,
         desc='Test paytida 2 ta noto‘g‘ri variantni olib tashlaydi.'),
    dict(key='shield', kind='consumable', tab='help', icon='🛡', name='Qalqon', price=150,
         desc='18/20 bo‘lsa ham Unit o‘tilgan hisoblanadi. O‘zi avtomatik ishlaydi.'),
    dict(key='freeze', kind='consumable', tab='help', icon='🧊', name='Streak himoyasi', price=60,
         desc='Unitdan o‘ta olmasangiz ham streak nolga tushmaydi. Avtomatik ishlaydi.'),
    dict(key='xp2', kind='consumable', tab='help', icon='⚡', name='XP x2', price=120,
         desc='Keyingi o‘tilgan Unitda XP ikki baravar. Avtomatik ishlaydi.'),
    dict(key='coin2', kind='consumable', tab='help', icon='🪙', name='Coin x2', price=90,
         desc='Keyingi o‘tilgan Unitda coin ikki baravar. Avtomatik ishlaydi.'),
    dict(key='unlock', kind='consumable', tab='help', icon='🗝', name='Unit kaliti', price=500,
         desc='Keyingi yopiq Unitni testsiz ochadi. Do‘kondagi “Ishlatish” tugmasi bilan.'),
    # ---- Ramkalar (profil rasmi uchun) ----
    dict(key='gold', kind='frame', tab='frame', icon='🟡', name='Oltin ramka', price=150, desc='Profil rasmingiz atrofida oltin hoshiya.'),
    dict(key='neon', kind='frame', tab='frame', icon='🟢', name='Neon ramka', price=200, desc='Yashil-ko‘k neon yorug‘lik.'),
    dict(key='fire', kind='frame', tab='frame', icon='🔥', name='Olov ramka', price=300, desc='Yonib turuvchi qizil-to‘q sariq ramka.'),
    dict(key='rainbow', kind='frame', tab='frame', icon='🌈', name='Kamalak ramka', price=450, desc='Ranglari almashib turadigan ramka.'),
    dict(key='diamond', kind='frame', tab='frame', icon='💎', name='Olmos ramka', price=700, desc='Eng noyob, yaltirab turadigan ramka.'),
    # ---- Unvonlar ----
    dict(key='hunter', kind='title', tab='title', icon='🏹', name='So‘z ovchisi', price=120, desc='Profilingizda ismingiz tagida ko‘rinadi.'),
    dict(key='scholar', kind='title', tab='title', icon='🎓', name='Bilimdon', price=250, desc='Profilingizda ismingiz tagida ko‘rinadi.'),
    dict(key='hero', kind='title', tab='title', icon='🦸', name='Ingliz tili qahramoni', price=500, desc='Profilingizda ismingiz tagida ko‘rinadi.'),
    dict(key='legend', kind='title', tab='title', icon='👑', name='Legenda', price=1000, desc='Eng yuqori unvon.'),
    # ---- Mavzular ----
    dict(key='ocean', kind='theme', tab='theme', icon='🌊', name='Okean', price=200, desc='Sayt fonini ko‘k-moviy ranglarga bo‘yaydi.'),
    dict(key='sunset', kind='theme', tab='theme', icon='🌇', name='Quyosh botishi', price=250, desc='Iliq pushti-to‘q sariq fon.'),
    dict(key='forest', kind='theme', tab='theme', icon='🌲', name='O‘rmon', price=250, desc='Tinch yashil fon.'),
    dict(key='onyx', kind='theme', tab='theme', icon='🖤', name='Qora olmos', price=400, desc='Juda to‘q, minimal fon.'),
    # ---- Omad ----
    dict(key='lootbox', kind='instant', tab='luck', icon='🎁', name='Omad qutisi', price=60,
         desc='Ichidan tasodifiy coin yoki yordamchi chiqadi. Ba’zan yutasiz, ba’zan yo‘q!'),
]

BY_KEY = {i['key']: i for i in ITEMS}
KIND_LABEL = {'frame': 'Ramka', 'title': 'Unvon', 'theme': 'Mavzu'}
TITLE_NAMES = {i['key']: i['name'] for i in ITEMS if i['kind'] == 'title'}

# Omad qutisi: (og'irlik, turi, qiymat)
LOOT_TABLE = [
    (30, 'coin', 20), (25, 'coin', 40), (15, 'coin', 60), (10, 'coin', 100), (3, 'coin', 200),
    (8, 'item', 'time'), (6, 'item', 'fifty'), (3, 'item', 'freeze'),
]

# Daromad
DAILY_BASE = 10
DAILY_STREAK_BONUS = 5       # har ketma-ket kun uchun +5 (7 kungacha)
PASS_COINS = 25
PERFECT_BONUS = 15           # 20/20 uchun qo'shimcha
PASS_SCORE = 19
REPLAY_RATE = 0.2            # oldin o'tilgan Unitni takrorlaganda XP va coin ulushi (20%)
