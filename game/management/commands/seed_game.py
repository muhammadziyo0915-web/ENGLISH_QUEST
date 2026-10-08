from django.core.management.base import BaseCommand
from game.models import Stage, Question

TOPICS = [
    'Greetings & Introductions','Family & People','Daily Routines','School & Study',
    'Food & Drinks','Home & Rooms','Time & Dates','Places in Town','Shopping',
    'Weather','Hobbies','Travel','Transport','Health & Habits','Work',
    'Present Simple','Present Continuous','Past Simple','Future Plans','Review'
]

# English word | Uzbek meaning | easy pronunciation guide.
RAW = '''
after|keyin|af-ter
again|yana|ə-gen
age|yosh|eyj
airport|aeroport|e-ər-port
animal|hayvon|e-ni-məl
answer|javob|an-sər
apple|olma|epəl
April|aprel|ey-prəl
arm|qo‘l|arm
arrive|yetib kelmoq|ə-rayv
art|san’at|art
ask|so‘ramoq|ask
August|avgust|o-gəst
aunt|xola yoki amma|ant
away|uzoqda|ə-vey
baby|chaqaloq|bey-bi
back|orqa|bek
bag|sumka|beg
ball|to‘p|bol
banana|banan|bə-na-nə
bank|bank|benk
bath|vanna|baath
bathroom|hammom|baath-rum
beautiful|chiroyli|byu-ti-fəl
because|chunki|bi-koz
bed|karavot|bed
bedroom|yotoqxona|bed-rum
begin|boshlamoq|bi-gin
behind|orqasida|bi-haynd
believe|ishonmoq|bi-li:v
below|pastda|bi-lo
between|orasida|bi-twi:n
big|katta|big
bike|velosiped|bayk
bird|qush|bərd
birthday|tug‘ilgan kun|bərth-dey
black|qora|blek
blue|ko‘k|blu:
book|kitob|buk
bottle|butilka|botəl
box|quti|boks
boy|o‘g‘il bola|boy
bread|non|bred
break|tanaffus|breyk
breakfast|nonushta|brek-fəst
bring|olib kelmoq|bring
brother|aka yoki uka|bradhər
brown|jigarrang|braun
build|qurmoq|bild
bus|avtobus|bas
business|biznes|biz-nis
busy|band|bi-zi
buy|sotib olmoq|bay
cake|tort|keyk
call|qo‘ng‘iroq qilmoq|kol
camera|kamera|kem-rə
can|qila olmoq|ken
car|mashina|kar
card|karta|kard
care|g‘amxo‘rlik|ker
carry|olib yurmoq|ke-ri
cat|mushuk|ket
chair|stul|cher
change|o‘zgartirmoq|cheynj
cheap|arzon|chi:p
child|bola|chayld
choose|tanlamoq|chu:z
city|shahar|si-ti
class|sinf|klas
classroom|sinf xonasi|klas-rum
clean|toza|kli:n
climb|ko‘tarilmoq|klaym
clock|soat|klok
close|yopmoq|kloz
clothes|kiyimlar|kloz
cloud|bulut|klaud
cold|sovuq|kold
college|kollej|ko-lij
come|kelmoq|kam
computer|kompyuter|kəm-pyu-tər
cook|ovqat pishirmoq|kuk
country|mamlakat|kan-tri
course|kurs|kors
cousin|amakivachcha yoki tog‘avachcha|ka-zən
cow|sigir|kau
cup|piyola|kap
dance|raqs tushmoq|dens
dangerous|xavfli|deyn-jə-rəs
dark|qorong‘i|dark
date|sana|deyt
day|kun|dey
decide|qaror qilmoq|di-sayd
desk|parta|desk
different|turli|dif-rənt
dinner|kechki ovqat|di-nər
dirty|iflos|dər-ti
doctor|shifokor|dok-tər
dog|it|dog
door|eshik|dor
down|pastga|daun
draw|rasm chizmoq|dro
 dress|ko‘ylak|dres
drink|ichmoq|drink
drive|haydamoq|drayv
ear|quloq|ir
eat|yemoq|i:t
eight|sakkiz|eyt
evening|kechqurun|i:v-ning
every|har bir|ev-ri
example|misol|ig-zam-pəl
exercise|mashq|ek-sər-sayz
expensive|qimmat|ik-spen-siv
eye|ko‘z|ay
face|yuz|feys
family|oila|fe-mə-li
far|uzoq|far
farm|ferma|farm
father|ota|fa-dhər
February|fevral|feb-ru-e-ri
feel|his qilmoq|fi:l
few|bir nechta|fyu:
find|topmoq|faynd
finish|tugatmoq|fi-nish
fire|olov|fayər
first|birinchi|fərst
fish|baliq|fish
five|besh|fayv
floor|pol|flor
flower|gul|flauər
food|ovqat|fu:d
football|futbol|fut-bol
for|uchun|for
forget|unutmoq|fər-get
four|to‘rt|for
Friday|juma|fray-dey
friend|do‘st|frend
from|dan|from
front|old tomon|frant
fruit|meva|fru:t
full|to‘la|ful
fun|qiziqarli|fan
game|o‘yin|geym
garden|bog‘|gar-dən
get|olmoq|get
girl|qiz|gərl
give|bermoq|giv
glass|stakan|glas
go|bormoq|gou
good|yaxshi|gud
grandfather|bobo|gren-fa-dhər
grandmother|buvi|gren-ma-dhər
green|yashil|gri:n
group|guruh|gru:p
grow|o‘smoq|grou
guess|taxmin qilmoq|ges
hair|soch|her
half|yarim|haf
hand|qo‘l|hend
happy|xursand|he-pi
hard|qiyin|hard
hat|shapka|het
have|ega bo‘lmoq|hev
he|u, erkak|hi:
head|bosh|hed
health|sog‘liq|helth
hear|eshitmoq|hir
help|yordam bermoq|help
here|bu yerda|hir
high|baland|hay
holiday|ta’til|ho-li-dey
home|uy|houm
hope|umid qilmoq|houp
horse|ot|hors
hospital|kasalxona|hos-pi-təl
hot|issiq|hot
hour|soat|auər
house|uy|haus
how|qanday|hau
hundred|yuz|han-drəd
hungry|och|hang-gri
idea|fikr|ay-di-ə
important|muhim|im-por-tənt
in|ichida|in
inside|ichkarida|in-sayd
interesting|qiziqarli|in-trəs-ting
January|yanvar|jen-yu-e-ri
job|ish|job
join|qo‘shilmoq|joyn
July|iyul|ju-lay
June|iyun|ju:n
keep|saqlamoq|ki:p
key|kalit|ki:
kitchen|oshxona|ki-chən
know|bilmoq|nou
language|til|leng-gwij
large|katta|larj
last|oxirgi|last
late|kech|leyt
learn|o‘rganmoq|lərn
leave|ketmoq|li:v
left|chap|left
lesson|dars|le-sən
letter|harf|le-tər
library|kutubxona|lay-bre-ri
life|hayot|layf
light|yorug‘|layt
like|yoqtirmoq|layk
listen|tinglamoq|lis-ən
little|kichik|litəl
live|yashamoq|liv
long|uzun|long
look|qaramoq|luk
love|sevmoq|lav
lunch|tushlik|lanch
machine|mashina|mə-shi:n
make|yasamoq|meyk
man|erkak|men
many|ko‘p|me-ni
market|bozor|mar-kit
May|may|mey
meet|uchrashmoq|mi:t
minute|daqiqa|mi-nit
Monday|dushanba|man-dey
money|pul|ma-ni
month|oy|manth
morning|ertalab|mor-ning
mother|ona|ma-dhər
mountain|tog‘|maun-tən
move|harakatlanmoq|mu:v
movie|kino|mu:-vi
much|ko‘p|mach
music|musiqa|myu-zik
name|ism|neym
near|yaqin|nir
need|kerak bo‘lmoq|ni:d
never|hech qachon|ne-vər
new|yangi|nyu:
next|keyingi|nekst
night|tun|nayt
nine|to‘qqiz|nayn
no|yo‘q|nou
noise|shovqin|noyz
north|shimol|north
not|emas|not
November|noyabr|nou-vem-bər
now|hozir|nau
number|raqam|nam-bər
office|idora|o-fis
often|tez-tez|of-ən
old|eski|ould
one|bir|wan
open|ochmoq|ou-pən
orange|to‘q sariq|o-rinj
outside|tashqarida|aut-sayd
over|ustidan|ou-vər
page|sahifa|peyj
parent|ota-ona|per-ənt
park|bog‘|park
part|qism|part
party|bazm|par-ti
pay|to‘lamoq|pey
people|odamlar|pi-pəl
person|odam|pər-sən
phone|telefon|foun
photo|rasm|fou-tou
place|joy|pleys
plan|reja|plen
play|o‘ynamoq|pley
please|iltimos|pli:z
police|politsiya|pə-li:s
poor|kambag‘al|pur
popular|mashhur|po-pyu-lər
practice|mashq qilmoq|prek-tis
problem|muammo|prob-ləm
put|qo‘ymoq|put
question|savol|kwes-chən
quick|tez|kwik
quiet|tinch|kwai-ət
rain|yomg‘ir|reyn
read|o‘qimoq|ri:d
ready|tayyor|re-di
red|qizil|red
remember|eslamoq|ri-mem-bər
right|o‘ng|rayt
river|daryo|ri-vər
road|yo‘l|roud
room|xona|ru:m
run|yugurmoq|ran
Saturday|shanba|sa-tər-dey
school|maktab|skul
science|fan|sayəns
second|ikkinchi|se-kənd
see|ko‘rmoq|si:
sell|sotmoq|sel
September|sentabr|sep-tem-bər
seven|yetti|se-vən
she|u, ayol|shi
shop|do‘kon|shop
short|qisqa|short
show|ko‘rsatmoq|shou
sick|kasal|sik
sing|kuylamoq|sing
sister|opa yoki singil|sis-tər
six|olti|siks
sit|o‘tirmoq|sit
sleep|uxlamoq|sli:p
small|kichik|smol
snow|qor|snou
some|ba’zi|sam
son|o‘g‘il|san
song|qo‘shiq|song
soon|tez orada|su:n
speak|gapirmoq|spi:k
sport|sport|sport
spring|bahor|spring
stand|turmoq|stend
start|boshlamoq|start
station|bekat|stey-shən
stay|qolmoq|stey
street|ko‘cha|stri:t
strong|kuchli|strong
student|o‘quvchi|styu-dənt
study|o‘qimoq|sta-di
summer|yoz|samər
sun|quyosh|san
Sunday|yakshanba|san-dey
supermarket|supermarket|su-pər-mar-kit
table|stol|tey-bəl
take|olmoq|teyk
talk|gaplashmoq|tok
teacher|o‘qituvchi|ti-chər
team|jamoa|ti:m
tell|aytmoq|tel
ten|o‘n|ten
test|test|test
than|ga qaraganda|dhen
thank|rahmat aytmoq|thengk
that|ana u|dhet
the|aniq artikl|dhə
there|u yerda|dher
thing|narsa|thing
think|o‘ylamoq|thingk
three|uch|thri:
time|vaqt|taym
tired|charchagan|tayər
today|bugun|tə-dey
together|birga|tə-ge-dhər
tomorrow|ertaga|tə-mo-rou
town|shahar|taun
train|poyezd|treyn
travel|sayohat qilmoq|tre-vəl
tree|daraxt|tri:
try|urinib ko‘rmoq|tray
Tuesday|seshanba|tyuz-dey
two|ikki|tu:
under|ostida|an-dər
understand|tushunmoq|an-dər-stend
university|universitet|yu-ni-vər-si-ti
use|ishlatmoq|yu:z
usually|odatda|yu-zhu-ə-li
very|juda|ve-ri
visit|tashrif buyurmoq|vi-zit
wait|kutmoq|weyt
walk|piyoda yurmoq|wok
want|xohlamoq|wont
warm|iliq|worm
wash|yuvmoq|wosh
watch|tomosha qilmoq|woch
water|suv|wo-tər
way|yo‘l|wey
wear|kiymoq|wer
Wednesday|chorshanba|wenz-dey
week|hafta|wi:k
welcome|xush kelibsiz|wel-kəm
well|yaxshi|wel
white|oq|wayt
who|kim|hu:
why|nega|way
window|deraza|win-dou
winter|qish|win-tər
woman|ayol|wu-mən
word|so‘z|wərd
work|ishlamoq|wərk
world|dunyo|wərld
write|yozmoq|rayt
year|yil|yir
yellow|sariq|ye-lou
yes|ha|yes
yesterday|kecha|yes-tər-dey
young|yosh|yang
your|sening|yor
zero|nol|zi-rou
'''

WORDS = []
for line in RAW.strip().splitlines():
    word, meaning, pronunciation = [x.strip() for x in line.split('|')]
    WORDS.append((word, meaning, pronunciation))

class Command(BaseCommand):
    help = 'Create 180 English vocabulary units with 20 words per unit.'

    def handle(self, *args, **kwargs):
        Question.objects.all().delete()
        Stage.objects.all().delete()

        for n in range(1, 181):
            topic = TOPICS[(n - 1) % len(TOPICS)]
            level = 'Beginner' if n <= 60 else 'Elementary' if n <= 120 else 'Pre-Intermediate'
            stage = Stage.objects.create(
                number=n,
                title=f'Unit {n}',
                topic=topic,
                level=level,
                xp=100 + n * 5,
                badge=['⭐', '🔥', '💎', '👑'][(n - 1) % 4],
            )

            # 20 different words inside each unit; a fresh attempt randomizes their order.
            start = ((n - 1) * 17) % len(WORDS)
            selected = [WORDS[(start + i) % len(WORDS)] for i in range(20)]
            for i, (word, meaning, pronunciation) in enumerate(selected):
                options = [meaning]
                # Pick three different Uzbek meanings as distractors.
                cursor = 37 + i * 3
                while len(options) < 4:
                    candidate = WORDS[(start + cursor) % len(WORDS)][1]
                    if candidate not in options:
                        options.append(candidate)
                    cursor += 17
                shift = (n + i + len(word)) % 4
                options = options[shift:] + options[:shift]
                correct = 'ABCD'[options.index(meaning)]
                Question.objects.create(
                    stage=stage,
                    prompt=f'{word} ({pronunciation})',
                    option_a=options[0],
                    option_b=options[1],
                    option_c=options[2],
                    option_d=options[3],
                    correct=correct,
                    explanation=f'{word} — {meaning}.',
                )

        self.stdout.write(self.style.SUCCESS('Created 180 units and 3,600 vocabulary questions.'))
