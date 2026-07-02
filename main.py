import os
import telebot
from telebot import types

# ---------- Токен ----------
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "7067641317:AAHOXUhb1_TTlEFCC2Au8ACmKOD4ryErpXg")
bot = telebot.TeleBot(TOKEN)

# ---------- Состояние чата ----------
user_state = {}   # { chat_id: {"msg_id": int, "current_callback": str, "history": list} }

def init_state(chat_id):
    if chat_id not in user_state:
        user_state[chat_id] = {"msg_id": None, "current_callback": None, "history": []}

def push_history(chat_id, callback):
    if callback != "back":
        user_state[chat_id]["history"].append(callback)

def pop_history(chat_id):
    if user_state[chat_id]["history"]:
        return user_state[chat_id]["history"].pop()
    return None


# ---------- Универсальная клавиатура ----------
def back_button():
    return types.InlineKeyboardButton("⬅️ Back", callback_data="back")

def make_keyboard(*rows, add_back=False):
    """Каждый row — список кортежей (текст, callback_data/url)."""
    markup = types.InlineKeyboardMarkup()
    for row in rows:
        buttons = []
        for text, data in row:
            if data.startswith("http"):
                buttons.append(types.InlineKeyboardButton(text, url=data))
            else:
                buttons.append(types.InlineKeyboardButton(text, callback_data=data))
        markup.row(*buttons)
    if add_back:
        markup.row(back_button())
    return markup

# ---------- Реестр меню ----------
MENUS = {}

def reg(cb, text, kb_func):
    MENUS[cb] = (text, kb_func)

# ===================== СТАРТ =====================
reg("start", "Choose your language 🌍",
    lambda: make_keyboard(
        [("🇸🇾 عربي", "arabic"), ("English 🇺🇸", "English")],
        [("Русский 🇷🇺", "Russian"), ("French 🇫🇷", "French")]
    ))

# =============== ГЛАВНЫЕ МЕНЮ (языки) ===============
def main_ar(): return make_keyboard(
    [("الدراسة في جمهورية بيلاروسيا 🇧🇾", "edubel")],
    [("نحن على وسائل التواصل الإجتماعي", "social media")],
    [("تواصل معنا", "https://wa.me/message/2552FHKOBKBYH1")],
    add_back=True)
def main_en(): return make_keyboard(
    [("Studying in the Republic of Belarus 🇧🇾", "edubel en")],
    [("We are on social media", "social media")],
    [("Contact us", "https://wa.me/message/2552FHKOBKBYH1")],
    add_back=True)
def main_ru(): return make_keyboard(
    [("Обучение в Республике Беларусь 🇧🇾", "edubel ru")],
    [("Мы в социальных сетях", "social media")],
    [("Свяжитесь с нами", "https://wa.me/message/2552FHKOBKBYH1")],
    add_back=True)
def main_fr(): return make_keyboard(
    [("Étudier en République de Biélorussie 🇧🇾", "edubel fr")],
    [("Nous sommes sur les réseaux sociaux.", "social media")],
    [("Contactez-nous", "https://wa.me/message/2552FHKOBKBYH1")],
    add_back=True)

reg("arabic",   "مرحباً! اهلا بك في شركة يوني هايبر! 🙌", main_ar)
reg("English",  "Hello! Welcome to UniHyper! 🙌", main_en)
reg("Russian",  "Привет! Добро пожаловать в компанию UniHyper! 🙌", main_ru)
reg("French",   "Bonjour ! Bienvenue chez UniHyper ! 🙌", main_fr)

# =============== СОЦСЕТИ ===============
def social_kb():
    markup = types.InlineKeyboardMarkup()
    markup.row(types.InlineKeyboardButton("Instagram 📱", url="https://www.instagram.com/unihyper_education/"),
               types.InlineKeyboardButton("Telegram 📱", url="https://t.me/unihyper_public_chat"))
    markup.row(types.InlineKeyboardButton("Tik-Tok 📱", url="https://www.tiktok.com/@unihyper_edu"),
               types.InlineKeyboardButton("Facebook 📱", url="https://www.facebook.com/share/1Cags8MM83/"))
    markup.row(back_button())
    return markup
reg("social media", "Let's be social ❤️", social_kb)

# =============== EDU BELARUS ===============
def edubel_ar(): return make_keyboard(
    [("نبذة عن جمهورية بيلاروسيا", "historybela")],
    [("تخصصات البكالوريوس", "bacalora")],
    [("تخصصات الماجستير و الدكتوراه", "magestra")],
    add_back=True)
def edubel_en(): return make_keyboard(
    [("About Belarus", "historybele")],
    [("Available Specialties", "bacalore")],
    [("Master's and Doctoral (PhD) Programs / Specialties", "magestre")],
    add_back=True)
def edubel_ru(): return make_keyboard(
    [("О Республике Беларусь", "historybelr")],
    [("Доступные специальности", "bacalorr")],
    [("Специальности магистратуры и аспирантуры / докторантуры", "magestrr")],
    add_back=True)
def edubel_fr(): return make_keyboard(
    [("Présentation de la République de Biélorussie", "historybelf")],
    [("Spécialités disponibles", "bacalorf")],
    [("Spécialités de master et de doctorat", "magestrf")],
    add_back=True)
reg("edubel",    "الدراسة في جمهورية بيلاروسيا 🇧🇾", edubel_ar)
reg("edubel en", "Studying in the Republic of Belarus 🇧🇾", edubel_en)
reg("edubel ru", "Обучение в Республике Беларусь 🇧🇾", edubel_ru)
reg("edubel fr", "Étudier en République de Biélorussie 🇧🇾", edubel_fr)

# =============== ИСТОРИЯ БЕЛАРУСИ ===============
text_hist_ar = ("اكتشف بيلاروسيا: بوابتك للتعليم العالمي والفرص الواعدة.\n\n"
"مرحباً بك في قلب أوروبا! جمهورية بيلاروسيا ليست مجرد وجهة دراسية، إنها تجربة حياة متكاملة تمزج بين العراقة الأكاديمية والحداثة الآمنة. تخيل أن تدرس في جامعات يعود تاريخها لعقود، تحمل إرثاً علمياً عريقاً في تخصصات مثل الطب، والهندسة، وتكنولوجيا المعلومات، بتكاليف معقولة وجودة تعليمية تنافس العالمية.\n\n"
" لماذا شركتنا هي خيارك الأمثل؟\n\n"
" نحن لا نقدم لك قبولاً جامعياً فحسب، بل نبني لك مستقبلاً. مع شركتنا، أنت لست مجرد طالب، أنت فرد من عائلتنا. نضمن لك:\n\n"
" - قبولاً مضموناً في أفضل الجامعات الحكومية والخاصة.\n\n"
" - دعماً شاملاً يمتد من لحظة تقديمك وحتى تخرجك، بما في ذلك الاستقبال من المطار، والسكن المريح، والتأمين الصحي.\n\n"
" - إجراءات مبسطة وسريعة للتأشيرة، حيث نكون حلقة الوصل بينك وبين السفارة.\n\n"
" - بيئة آمنة ومستقرة، فبيلاروسيا بلد يتمتع بمعدلات أمان عالية وطبيعة خلابة وتكلفة معيشة مناسبة جداً للطلاب.\n\n"
" انضم إلى آلاف الطلاب الذين اختاروا بيلاروسيا نقطة انطلاق لنجاحهم المهني. معنا، أنت لا تختار جامعة، بل تختار مستقبلاً واعداً في بلد يحترم العلم ويقدر الطموح.")
text_hist_en = ("Discover Belarus: Your Gateway to World-Class Education and Promising Opportunities\n\n"
"Welcome to the heart of Europe! The Republic of Belarus is more than just a study destination; it's a complete life experience that blends rich academic heritage with modern-day security. Imagine studying at universities with decades of history, carrying a profound scientific legacy in fields like Medicine, Engineering, and IT, all at an affordable cost and with a quality of education that competes on a global scale.\n\n"
" Why is our company your perfect choice?\n\n"
" We don’t just offer you university admission; we build your future. With us, you are not just a student, you are a member of our family. We guarantee:\n\n"
" - Guaranteed admission to the best public and private universities.\n\n"
" - Comprehensive support from the moment you apply until your graduation, including airport pickup, comfortable accommodation, and health insurance.\n\n"
" - Simple and fast visa procedures, as we act as the bridge between you and the embassy.\n\n"
" - A safe and stable environment. Belarus is a country with high safety standards, stunning nature, and a very affordable cost of living for students.\n\n"
" Join the thousands of students who have chosen Belarus as the launching pad for their professional success. With us, you are not just choosing a university; you are choosing a promising future in a country that respects science and values ambition.")
text_hist_ru = ("Добро пожаловать в сердце Европы! Республика Беларусь — это не просто место учёбы, это полноценный жизненный опыт, сочетающий академические традиции и современную безопасность. Представьте себе обучение в университетах с десятилетиями истории, которые несут в себе богатейшее научное наследие в области медицины, инженерии и IT-технологий — и всё это по доступной стоимости с качеством, конкурирующим на мировом уровне.\n\n"
"Почему наша компания — ваш идеальный выбор?\n\n"
" Мы не просто оформляем поступление в вуз — мы строим ваше будущее. С нами вы не просто студент, вы — часть нашей семьи. Мы гарантируем:\n\n"
" - Гарантированное зачисление в лучшие государственные и частные университеты.\n\n"
" - Комплексную поддержку на всех этапах: от подачи заявки до получения диплома, включая встречу в аэропорту, комфортное жильё и медицинскую страховку.\n\n"
" - Простые и быстрые визовые процедуры — мы становимся вашим связующим звеном с посольством.\n\n"
" - Безопасную и стабильную среду. Беларусь — страна с высоким уровнем безопасности, живописной природой и очень доступной стоимостью жизни для студентов.\n\n"
" Присоединяйтесь к тысячам студентов, которые выбрали Беларусь как трамплин для своего профессионального успеха. С нами вы выбираете не просто университет, а надёжное будущее в стране, где уважают науку и ценят амбиции.")
text_hist_fr = ("Découvrez la Biélorussie : Votre porte d'entrée vers une éducation mondiale et des opportunités prometteuses\n\n"
"Bienvenue au cœur de l'Europe ! La République de Biélorussie n'est pas qu'une simple destination d'études, c'est une expérience de vie complète alliant un riche patrimoine académique à une sécurité moderne. Imaginez étudier dans des universités chargées d'histoire, porteuses d'un héritage scientifique profond dans des domaines comme la Médecine, l'Ingénierie et les Technologies de l'Information, le tout à un coût abordable et avec une qualité d'enseignement de niveau mondial.\n\n"
" Pourquoi notre entreprise est-elle le choix idéal pour vous ?\n\n"
" Nous ne nous contentons pas de vous offrir une admission à l'université ; nous construisons votre avenir. Avec nous, vous n'êtes pas qu'un simple étudiant, vous faites partie de notre famille. Nous vous garantissons :\n\n"
" - Une admission assurée dans les meilleures universités publiques et privées.\n\n"
" - Un soutien complet depuis votre candidature jusqu'à l'obtention de votre diplôme, y compris l'accueil à l'aéroport, un logement confortable et une assurance maladie.\n\n"
" - Des procédures de visa simples et rapides, car nous sommes le lien direct entre vous et l'ambassade.\n\n"
" - Un environnement sûr et stable. La Biélorussie est un pays jouissant d'un haut niveau de sécurité, d'une nature magnifique et d'un coût de la vie très abordable pour les étudiants.\n\n"
" Rejoignez les milliers d'étudiants qui ont choisi la Biélorussie comme tremplin vers leur réussite professionnelle. Avec nous, vous ne choisissez pas seulement une université, vous choisissez un avenir prometteur dans un pays qui respecte la science et valorise l'ambition.")

reg("historybela", text_hist_ar, lambda: make_keyboard(add_back=True))
reg("historybele", text_hist_en, lambda: make_keyboard(add_back=True))
reg("historybelr", text_hist_ru, lambda: make_keyboard(add_back=True))
reg("historybelf", text_hist_fr, lambda: make_keyboard(add_back=True))

# =============== БАКАЛАВРИАТ ===============
def bach_ar(): return make_keyboard(
    [("الهندسات", "Engineera"), ("الطب", "Medicinea")],
    [("طب البيطري", "Veterinarya"), ("تربية الرياضية", "Sporta")],
    [("ادارة أعمال و اقتصاد", "Economa")],
    add_back=True)
def bach_en(): return make_keyboard(
    [("Engineerings", "Engineere"), ("Medicine", "Medicinee")],
    [("Veterinary Medicine", "Veterinarye"), ("Sports Education", "Sporte")],
    [("Management and Economics", "Econome")],
    add_back=True)
def bach_ru(): return make_keyboard(
    [("Инженерия", "Engineerr"), ("Медицина", "Mediciner")],
    [("Ветеринарная медицина", "Veterinaryr"), ("Спортивное образование", "Sportr")],
    [("Менеджмент и экономика", "Economr")],
    add_back=True)
def bach_fr(): return make_keyboard(
    [("Ingénieries", "Engineerf"), ("Médecine", "Medicinef")],
    [("la médecine vétérinaire", "Veterinaryf"), ("Éducation sportive", "Sportf")],
    [("Gestion d'entreprise et économie", "Economf")],
    add_back=True)
reg("bacalora", "تخصصات البكالوريوس", bach_ar)
reg("bacalore", "Available Specialties", bach_en)
reg("bacalorr", "Доступные специальности", bach_ru)
reg("bacalorf", "Spécialités disponibles", bach_fr)

# =============== МЕДИЦИНА ===============
def med_ar(): return make_keyboard(
    [("الجامعة الحكومية البيلاروسية للطب (العاصمة مينسك)", "bsmua")],
    [("الجامعة الحكومية للطب في مدينة غرودنا", "grsmua")],
    add_back=True)
def med_en(): return make_keyboard(
    [("Belarusian State Medical University (capital Minsk)", "bsmue")],
    [("Grodno State University of Medicine", "grsmue")],
    add_back=True)
def med_ru(): return make_keyboard(
    [("Белорусский государственный медицинский университет (столица Минск)", "bsmur")],
    [("Гродненский государственный медицинский университет", "grsmur")],
    add_back=True)
def med_fr(): return make_keyboard(
    [("Université médicale d'État biélorusse (capitale Minsk)", "bsmuf")],
    [("Université d'État de médecine de Grodno", "grsmuf")],
    add_back=True)
reg("Medicinea", "الطب", med_ar)
reg("Medicinee", "Medicine", med_en)
reg("Mediciner", "Медицина", med_ru)
reg("Medicinef", "Médecine", med_fr)

# =============== BSMU ===============
def bsmu_ar(): return make_keyboard(
    [("نبذة عن الجامعة", "historybsmua")],
    [("التخصصات و الرسوم الجامعية", "https://drive.google.com/file/d/1u5OENQ-HV9_3dOAiWlunLGOGPSF0GQRG/view")],
    add_back=True)
def bsmu_en(): return make_keyboard(
    [("About the University", "historybsmue")],
    [("Majors and annual fees", "https://drive.google.com/file/d/1nINLezTkQs7phRaP7hCQwjqwzvpGBESI/view")],
    add_back=True)
def bsmu_ru(): return make_keyboard(
    [("Об университете", "historybsmur")],
    [("Специальности и стоимость обучения", "https://drive.google.com/file/d/1Z6ocYHCzJfaN3K8c0DAPLZY9ADVK2Jc3/view")],
    add_back=True)
def bsmu_fr(): return make_keyboard(
    [("À propos de l'université", "historybsmuf")],
    [("Spécialisations et frais annuels", "https://drive.google.com/file/d/15CvetGayjHEJecMc4lXKaZqHmdGyB_-5/view")],
    add_back=True)
reg("bsmua", "الجامعة الحكومية البيلاروسية للطب (العاصمة مينسك)", bsmu_ar)
reg("bsmue", "Belarusian State Medical University (capital Minsk)", bsmu_en)
reg("bsmur", "Белорусский государственный медицинский университет", bsmu_ru)
reg("bsmuf", "Université médicale d'État biélorusse (capitale Minsk)", bsmu_fr)

hist_bsmu_ar = ( 'جامعة بيلاروسيا الحكومية الطبية هي المؤسسة الطبية التعليمية الرائدة في جمهورية بيلاروسيا، وتتمتع بسلطة وتقدير مستحقين ليس فقط داخل بيلاروسيا، بل وأيضاً خارج حدودها. في نوفمبر من عام 2021، احتفلت الجامعة بمرور 100 عام على تأسيسها.\n'
                '\n'
                'يعود تاريخ بدايتها إلى عام 1921، عندما أُعلن عن افتتاح جامعة بيلاروسيا الحكومية، والتي كانت تضم كلية الطب ضمن تكوينها. وفي عام 1930، انفصلت كلية الطب لتصبح مؤسسة تعليمية مستقلة. أقيم أول تخرّج للأطباء في عام 1925، حيث حصل 21 شخصاً على دبلوم إتمام الكلية.\n'
                '\n'
                'في عام 2001، تم تغيير اسم معهد مينسك الطبي الحكومي (كما كان يُعرف في ذلك الوقت) إلى جامعة بيلاروسيا الحكومية للطب، وحصلت على لقب الجامعة الطبية الرائدة في جمهورية بيلاروسيا.\n'
                '\n'
                ' تضم آلاف الطلاب الأجانب من مئات الجنسيات المختلفة.')
                # полный текст из оригинала
hist_bsmu_en = ( 'Belarusian State Medical University is the leading medical educational institution of the Republic of Belarus and enjoys well-deserved authority and recognition not only within Belarus, but also far beyond its borders. In November 2021, the University celebrated the 100th anniversary of its founding.\n'
            '\n'
            'Its history dates back to 1921, when the opening of the Belarusian State University was announced, which included a Faculty of Medicine within its structure. In 1930, the Faculty of Medicine was separated into an independent educational institution. The first graduation of doctors took place in 1925, with 21 people receiving diplomas upon completion of the faculty.\n'
            '\n'
            'In 2001, the Minsk State Medical Institute (as it was known at the time) was renamed the Belarusian State Medical University and received the status of the leading medical university of the Republic of Belarus.\n'
            '\n'
            ' The University is home to thousands of international students from hundreds of different nationalities.')
hist_bsmu_ru = ('Белорусский государственный медицинский университет является ведущим медицинским образовательным учреждением Республики Беларусь и пользуется заслуженным авторитетом и признанием не только внутри Беларуси, но и далеко за её пределами. В ноябре 2021 года университет отметил 100-летие со дня своего основания.\n'
            '\n'
            'История университета начинается в 1921 году, когда было объявлено об открытии Белорусского государственного университета, в состав которого входил медицинский факультет. В 1930 году медицинский факультет был выделен в самостоятельное образовательное учреждение. Первый выпуск врачей состоялся в 1925 году — 21 человек получил диплом об окончании факультета.\n'
            '\n'
            'В 2001 году Минский государственный медицинский институт (как он тогда назывался) был переименован в Белорусский государственный медицинский университет и получил статус ведущего медицинского университета Республики Беларусь.\n'
            '\n'
            ' В университете обучаются тысячи иностранных студентов из сотен различных стран.')
hist_bsmu_fr = (
            "L'Université médicale d'État de Biélorussie est l'établissement d'enseignement médical leader de la République de Biélorussie et jouit d'une autorité et d'une reconnaissance méritées non seulement en Biélorussie, mais aussi bien au-delà de ses frontières. En novembre 2021, l'Université a célébré le 100e anniversaire de sa fondation.\n"
            "\n"
            "Son histoire remonte à 1921, lorsque l'ouverture de l'Université d'État de Biélorussie fut annoncée, laquelle comprenait une faculté de médecine dans sa composition. En 1930, la faculté de médecine fut séparée pour devenir un établissement d'enseignement indépendant. La première promotion de médecins eut lieu en 1925, avec 21 personnes ayant reçu un diplôme de fin d'études de la faculté.\n"
            "\n"
            "En 2001, l'Institut médical d'État de Minsk (comme on l'appelait alors) fut renommé Université médicale d'État de Biélorussie et reçut le statut d'université médicale leader de la République de Biélorussie.\n"
            "\n"
            " L'Université accueille des milliers d'étudiants étrangers provenant de centaines de nationalités différentes.")
reg("historybsmua", hist_bsmu_ar, lambda: make_keyboard(add_back=True))
reg("historybsmue", hist_bsmu_en, lambda: make_keyboard(add_back=True))
reg("historybsmur", hist_bsmu_ru, lambda: make_keyboard(add_back=True))
reg("historybsmuf", hist_bsmu_fr, lambda: make_keyboard(add_back=True))

# =============== GrSMU ===============
def grsmu_ar(): return make_keyboard(
    [("نبذة عن الجامعة", "historygrsmua")],
    [("التخصصات و الرسوم الجامعية", "https://drive.google.com/file/d/1R8fDlaq261qTTOMQnYYbWPtdqiHLtWee/view")],
    add_back=True)
def grsmu_en(): return make_keyboard(
    [("About the University", "historygrsmue")],
    [("Majors and annual fees", "https://drive.google.com/file/d/1v924saVQyrGmKXy8fzJQ5aWbUIqQTW6x/view")],
    add_back=True)
def grsmu_ru(): return make_keyboard(
    [("Об университете", "historygrsmur")],
    [("Специальности и стоимость обучения", "https://drive.google.com/file/d/1RU8E4CI8Qw-LE5F6re9RrKxTRK9svTby/view")],
    add_back=True)
def grsmu_fr(): return make_keyboard(
    [("À propos de l'université", "historygrsmuf")],
    [("Spécialisations et frais annuels", "https://drive.google.com/file/d/19j2g1j4IIZEbINYNI9WLDPjlZog1MedB/view")],
    add_back=True)
reg("grsmua", "الجامعة الحكومية للطب في مدينة غرودنا", grsmu_ar)
reg("grsmue", "Grodno State Medical University", grsmu_en)
reg("grsmur", "Гродненский государственный медицинский университет", grsmu_ru)
reg("grsmuf", "Université médicale d'État de Grodno", grsmu_fr)

hist_grsmu_ar = (
            'جامعة غرودنا الطبية: طب عالمي في مدينة الملوك\n'
            '\n'
            'في مدينة غرودنا، جوهرة بيلاروسيا التاريخية، تقع إحدى أعرق كليات الطب. جامعة غرودنا الطبية الحكومية (GrSMU) تجمع بين التقاليد العريقة والتعليم الحديث، وتشتهر عالمياً ببرامجها باللغة الإنجليزية في الطب العام والتمريض. ادرس في مستشفيات جامعية متطورة، وتدرّب على أيدي أطباء خبراء، وتخرّج طبيباً تحمل شهادة معترفاً بها في أوروبا، أمريكا، والهند. مع شركتنا، رحلتك نحو ارتداء المعطف الأبيض تبدأ بثقة وأمان في مدينة التاريخ والجمال.')
hist_grsmu_en = (
            'Grodno Medical University: Global Medicine in the City of Kings\n'
            '\n'
            ' In Grodno, the historical jewel of Belarus, lies one of the most prestigious medical schools. Grodno State Medical University (GrSMU) combines rich traditions with modern education, and is globally renowned for its English-medium programs in General Medicine and Nursing. Study in advanced university hospitals, train under expert physicians, and graduate as a doctor with a degree recognized in Europe, America, and India. With our company, your journey to wearing the white coat begins with confidence and safety in the city of history and beauty.')
hist_grsmu_ru = (
            'Гродненский медицинский университет: Мировая медицина в городе королей\n'
            '\n'
            ' В Гродно, исторической жемчужине Беларуси, находится один из старейших медицинских вузов. Гродненский государственный медицинский университет (ГрГМУ) сочетает богатые традиции с современным образованием и известен во всём мире своими программами на английском языке по лечебному делу и сестринскому делу. Учитесь в современных университетских клиниках, тренируйтесь под руководством опытных врачей и станьте врачом с дипломом, признаваемым в Европе, Америке и Индии. С нашей компанией ваш путь к белому халату начинается с уверенностью и безопасностью в городе истории и красоты.')
hist_grsmu_fr = (
            "Université de Médecine de Grodno : Médecine mondiale dans la ville des rois\n"
            "\n"
            " À Grodno, le joyau historique de la Biélorussie, se trouve l'une des plus prestigieuses facultés de médecine. L'Université Médicale d'État de Grodno (GrSMU) allie riches traditions et éducation moderne, et est mondialement reconnue pour ses programmes en anglais en Médecine Générale et en Soins Infirmiers. Étudiez dans des hôpitaux universitaires de pointe, formez-vous auprès de médecins experts et obtenez un diplôme de docteur reconnu en Europe, en Amérique et en Inde. Avec notre entreprise, votre chemin vers la blouse blanche commence en toute confiance et sécurité dans la ville d'histoire et de beauté.")
reg("historygrsmua", hist_grsmu_ar, lambda: make_keyboard(add_back=True))
reg("historygrsmue", hist_grsmu_en, lambda: make_keyboard(add_back=True))
reg("historygrsmur", hist_grsmu_ru, lambda: make_keyboard(add_back=True))
reg("historygrsmuf", hist_grsmu_fr, lambda: make_keyboard(add_back=True))

# =============== ВЕТЕРИНАРИЯ ===============
def vet_ar(): return make_keyboard(
    [("أكاديمية فيتبسك الحكومية للطب البيطري", "vsavma")],
    add_back=True)
def vet_en(): return make_keyboard(
    [("Vitebsk State Academy of Veterinary Medicine", "vsavme")],
    add_back=True)
def vet_ru(): return make_keyboard(
    [("Витебская государственная академия ветеринарной медицины", "vsavmr")],
    add_back=True)
def vet_fr(): return make_keyboard(
    [("Académie d'État de médecine vétérinaire de Vitebsk", "vsavmf")],
    add_back=True)
reg("Veterinarya", "طب البيطري", vet_ar)
reg("Veterinarye", "Veterinary Medicine", vet_en)
reg("Veterinaryr", "Ветеринарная медицина", vet_ru)
reg("Veterinaryf", "la médecine vétérinaire", vet_fr)

# =============== VSAVM ===============
def vsavm_ar(): return make_keyboard(
    [("نبذة عن الأكاديمة", "historyvsavma")],
    [("التخصصات و الرسوم الجامعية", "https://drive.google.com/file/d/152raxCzvKDb76VmbrXBGvyjB14YDUwqB/view")],
    add_back=True)
def vsavm_en(): return make_keyboard(
    [("About the Academy", "historyvsavme")],
    [("Majors and annual fees", "https://drive.google.com/file/d/1EwU9i2x0Mqwsphq-d90ocTHJQPCC7hek/view")],
    add_back=True)
def vsavm_ru(): return make_keyboard(
    [("Об Академии", "historyvsavmr")],
    [("Специальности и стоимость обучения", "https://drive.google.com/file/d/1inIj2VUoUlj4iUDYKTNt6XCZDZkAgLzr/view")],
    add_back=True)
def vsavm_fr(): return make_keyboard(
    [("À propos de Académie", "historyvsavmf")],
    [("Spécialisations et frais annuels", "https://drive.google.com/file/d/1_zEWFByIPnsRNnB9Jk6LBRFSR4zyH_6h/view")],
    add_back=True)
reg("vsavma", "أكاديمية فيتبسك الحكومية للطب البيطري", vsavm_ar)
reg("vsavme", "Vitebsk State Academy of Veterinary Medicine", vsavm_en)
reg("vsavmr", "Витебская государственная академия ветеринарной медицины", vsavm_ru)
reg("vsavmf", "Académie d'État de médecine vétérinaire de Vitebsk", vsavm_fr)

hist_vsavm_ar = (
                'أكاديمية فيتبسك للطب البيطري: ارعَ الحياة، وابنِ مستقبلاً عالمياً\n'
                '\n'
                ' هل يدفعك شغف رعاية الحيوان نحو مهنة نبيلة ومربحة؟ أكاديمية فيتبسك الحكومية للطب البيطري (VSAVM) هي إحدى أعرق المؤسسات في أوروبا الشرقية وأكثرها احتراماً. هنا، تجتمع الخبرة الأكاديمية الممتدة لعقود مع المختبرات الحديثة والعيادات التدريبية الواقعية. تقدم الأكاديمية تخصصات فريدة تشمل الطب البيطري، الخبرة البيطرية والصيدلة البيطرية. ادرس في مدينة فيتبسك الجميلة والآمنة، وتخرج وأنت طبيب بيطري معتمد في مختلف دول العالم. مع شركتنا، نضمن لك قبولك ودعمك الكامل لتحقيق حلمك في مدينة الثقافة والفنون.')
hist_vsavm_en = (
            'Vitebsk Academy of Veterinary Medicine: Nurture Life, Build a Global Future\n'
            '\n'
            'Does your passion for animal care drive you towards a noble and profitable profession? The Vitebsk State Academy of Veterinary Medicine (VGAVM) is one of the oldest and most respected institutions in Eastern Europe. Here, decades of academic expertise blend with modern laboratories and real-life training clinics. The academy offers unique specializations including Veterinary Medicine, Veterinary Expertise, and Veterinary Pharmacy. Study in the beautiful and safe city of Vitebsk, and graduate as a veterinarian accredited in various countries worldwide. With our company, we guarantee your admission and full support to achieve your dream in the city of culture and arts.')
hist_vsavm_ru = (
            'Витебская академия ветеринарной медицины: Береги жизнь, строй глобальное будущее\n'
            '\n'
            'Ваша страсть к уходу за животными ведёт вас к благородной и прибыльной профессии? Витебская государственная академия ветеринарной медицины (ВГАВМ) — одно из старейших и наиболее уважаемых учебных заведений Восточной Европы. Здесь многолетний академический опыт сочетается с современными лабораториями и реальными учебными клиниками. Академия предлагает уникальные специальности: ветеринарная медицина, ветеринарно-санитарная экспертиза и ветеринарная фармация. Учитесь в прекрасном и безопасном Витебске и станьте ветеринарным врачом, признанным в разных странах мира. С нашей компанией мы гарантируем вам зачисление и полную поддержку для исполнения вашей мечты в городе культуры и искусства.')
hist_vsavm_fr = (
            'Académie vétérinaire de Vitebsk : Prenez soin de la vie, construisez un avenir mondial\n'
            '\n'
            "Votre passion pour le soin des animaux vous guide vers une profession noble et lucrative ? L'Académie d'État de Médecine Vétérinaire de Vitebsk (VGAVM) est l'une des institutions les plus anciennes et les plus respectées d'Europe de l'Est. Ici, des décennies d'expertise académique se mêlent à des laboratoires modernes et à des cliniques de formation en conditions réelles. L'académie propose des spécialisations uniques : Médecine Vétérinaire, Expertise Vétérinaire et Pharmacie Vétérinaire. Étudiez dans la belle et sûre ville de Vitebsk, et obtenez votre diplôme de vétérinaire reconnu dans de nombreux pays du monde. Avec notre entreprise, nous vous garantissons votre admission et un soutien complet pour réaliser votre rêve dans la ville de la culture et des arts.")
reg("historyvsavma", hist_vsavm_ar, lambda: make_keyboard(add_back=True))
reg("historyvsavme", hist_vsavm_en, lambda: make_keyboard(add_back=True))
reg("historyvsavmr", hist_vsavm_ru, lambda: make_keyboard(add_back=True))
reg("historyvsavmf", hist_vsavm_fr, lambda: make_keyboard(add_back=True))

# =============== СПОРТ ===============
def sport_ar(): return make_keyboard(
    [("الجامعة البيلاروسية الحكومية للثقافة البدنية في مينسك", "bsupca")],
    add_back=True)
def sport_en(): return make_keyboard(
    [("Belarusian State University of Physical Culture in Minsk", "bsupce")],
    add_back=True)
def sport_ru(): return make_keyboard(
    [("Белорусский государственный университет физической культуры", "bsupcr")],
    add_back=True)
def sport_fr(): return make_keyboard(
    [("L'Université d'État de Culture Physique de Biélorussie à Minsk", "bsupcf")],
    add_back=True)
reg("Sporta", "تربية الرياضية", sport_ar)
reg("Sporte", "Sports Education", sport_en)
reg("Sportr", "Спортивное образование", sport_ru)
reg("Sportf", "Éducation sportive", sport_fr)

# =============== BSUPC ===============
def bsupc_ar(): return make_keyboard(
    [("نبذة عن الجامعة", "historybsupca")],
    [("التخصصات و الرسوم الجامعية", "https://drive.google.com/file/d/1shu-YFj8-hVenwdDjr0cF3Z56HoQ60KQ/view")],
    add_back=True)
def bsupc_en(): return make_keyboard(
    [("About the University", "historybsupce")],
    [("Majors and annual fees", "https://drive.google.com/file/d/13NTnZH-vS81HBbJKQLHUl2LnoNNBR6EZ/view")],
    add_back=True)
def bsupc_ru(): return make_keyboard(
    [("Об университете", "historybsupcr")],
    [("Специальности и стоимость обучения", "https://drive.google.com/file/d/1oauzdkpWUakcGxDAQLbJvmWfXdEACxAY/view")],
    add_back=True)
def bsupc_fr(): return make_keyboard(
    [("À propos de l'université", "historybsupcf")],
    [("Spécialisations et frais annuels", "https://drive.google.com/file/d/1K3b0yR30i6DYvC-0JuVwhRkKbcNypiD-/view")],
    add_back=True)
reg("bsupca", "الجامعة البيلاروسية الحكومية للثقافة البدنية في مينسك", bsupc_ar)
reg("bsupce", "Belarusian State University of Physical Culture in Minsk", bsupc_en)
reg("bsupcr", "Белорусский государственный университет физической культуры", bsupc_ru)
reg("bsupcf", "L'Université d'État de Culture Physique de Biélorussie à Minsk", bsupc_fr)

hist_bsupc_ar = (
                'جامعة الرياضة في مينسك: ابقِ قوياً، وتخرّج بطلاً\n'
                '\n'
                'هل أنت شغوف بالرياضة وتريد تحويلها إلى مهنة عالمية؟ الجامعة البيلاروسية الحكومية للثقافة البدنية في مينسك هي المكان الذي صَنع الأبطال الأولمبيين. تقدم لك هذه الجامعة الفريدة برامج أكاديمية متخصصة في التدريب الرياضي، والإدارة الرياضية، والعلاج الطبيعي، وإعادة التأهيل. ادرس في منشآت أولمبية المستوى، على أيدي مدربين خبراء، واجمع بين شغفك وشهادتك الجامعية. مع شركتنا، انطلاقتك الاحترافية نحو الذهب تبدأ من هنا.')
hist_bsupc_en =  (
                'Sports University in Minsk: Get Strong, Graduate a Champion\n'
                '\n'
                'Are you passionate about sports and want to turn it into a global career? The Belarusian State University of Physical Culture in Minsk is the place where Olympic champions are forged. This unique university offers specialized academic programs in Sports Coaching, Sports Management, Physiotherapy, and Rehabilitation. Study in Olympic-level facilities under expert coaches, and combine your passion with your degree. With our company, your professional sprint towards gold starts right here.')
hist_bsupc_ru = (
                'Спортивный университет в Минске: Стань сильным, стань чемпионом\n'
                '\n'
                'Вы увлечены спортом и хотите превратить его в международную карьеру? Белорусский государственный университет физической культуры в Минске — это место, где создают олимпийских чемпионов. Этот уникальный университет предлагает специализированные академические программы по спортивной тренировке, спортивному менеджменту, физиотерапии и реабилитации. Учитесь на объектах олимпийского уровня у экспертов-тренеров и объедините свою страсть с высшим образованием. С нашей компанией ваш профессиональный путь к золоту начинается здесь.')
hist_bsupc_fr = (
                "L'Université du Sport à Minsk : Deviens fort, deviens champion\n"
                "\n"
                "Vous êtes passionné de sport et souhaitez en faire une carrière internationale ? L'Université d'État de Culture Physique de Biélorussie à Minsk est l'endroit où se forgent les champions olympiques. Cette université unique propose des programmes académiques spécialisés en Entraînement Sportif, Management du Sport, Physiothérapie et Rééducation. Étudiez dans des installations de niveau olympique auprès d'entraîneurs experts, et alliez votre passion à votre diplôme. Avec notre entreprise, votre sprint professionnel vers l'or commence ici.")
reg("historybsupca", hist_bsupc_ar, lambda: make_keyboard(add_back=True))
reg("historybsupce", hist_bsupc_en, lambda: make_keyboard(add_back=True))
reg("historybsupcr", hist_bsupc_ru, lambda: make_keyboard(add_back=True))
reg("historybsupcf", hist_bsupc_fr, lambda: make_keyboard(add_back=True))

# =============== ИНЖЕНЕРИЯ ===============
def eng_ar(): return make_keyboard(
    [("الجامعة البيلاروسية الحكومية للمعلوماتية والالكترونيات الراديوية (العاصمة مينسك)", "bsuira")],
    [("جامعة غومل الحكومية للتقنيات سوخوي (مدينة غومل)", "gstua")],
    add_back=True)
def eng_en(): return make_keyboard(
    [("Belarusian State University of Informatics and Radioelectronics (capital Minsk)", "bsuire")],
    [("Sukhoi Gomel State Technical University (Gomel)", "gstue")],
    add_back=True)
def eng_ru(): return make_keyboard(
    [("Белорусский государственный университет информатики и радиоэлектроники", "bsuirr")],
    [("Гомельский государственный технический университет имени П.О. Сухого", "gstur")],
    add_back=True)
def eng_fr(): return make_keyboard(
    [("Université d'État biélorusse d'informatique et de radioélectronique (capitale Minsk)", "bsuirf")],
    [("Université technique d'État de Gomel nommée d'après P.O. Soukhoï (Gomel)", "gstuf")],
    add_back=True)
reg("Engineera", "الهندسات", eng_ar)
reg("Engineere", "Engineerings", eng_en)
reg("Engineerr", "Инженерия", eng_ru)
reg("Engineerf", "Ingénieries", eng_fr)

# =============== BSUIR ===============
def bsuir_ar(): return make_keyboard(
    [("نبذة عن الجامعة", "historybsuira")],
    [("التخصصات و الرسوم الجامعية", "https://drive.google.com/file/d/1FvQHVqYOMJwsejxUR15yys3HnF_VyJSv/view")],
    add_back=True)
def bsuir_en(): return make_keyboard(
    [("About the University", "historybsuire")],
    [("Majors and annual fees", "https://drive.google.com/file/d/1TRv3gyJSp_3Y1-_zKVPhY3Y_AyXqSLMl/view")],
    add_back=True)
def bsuir_ru(): return make_keyboard(
    [("Об университете", "historybsuirr")],
    [("Специальности и стоимость обучения", "https://drive.google.com/file/d/1iiw9KG5e75PJSqObb7xfmtjiR9LMJnbe/view")],
    add_back=True)
def bsuir_fr(): return make_keyboard(
    [("À propos de l'université", "historybsuirf")],
    [("Spécialisations et frais annuels", "https://drive.google.com/file/d/1cwa5v8dutdVR8HHqK6LBNU6o4ha32xRO/view")],
    add_back=True)
reg("bsuira", "الجامعة البيلاروسية الحكومية للمعلوماتية والالكترونيات الراديوية", bsuir_ar)
reg("bsuire", "Belarusian State University of Informatics and Radioelectronics", bsuir_en)
reg("bsuirr", "Белорусский государственный университет информатики и радиоэлектроники", bsuir_ru)
reg("bsuirf", "Université d'État biélorusse d'informatique et de radioélectronique", bsuir_fr)

hist_bsuir_ar = (
                'جامعة BSUIR: حيث يولد قادة التكنولوجيا\n'
                '\n'
                'هل تحلم بأن تصبح خبيراً في الذكاء الاصطناعي، أو مهندس برمجيات في كبرى الشركات العالمية؟ جامعة BSUIR هي وجهتك المثالية. إنها القلعة التقنية الأولى في بيلاروسيا، والمتخصصة في تكنولوجيا المعلومات، والإلكترونيات، والاتصالات. هنا، ستدرس على أيدي نخبة من الأساتذة، وتتخرج بشهادة معترف بها عالمياً تفتح لك أبواب شركات التكنولوجيا العملاقة. مع شركتنا، نضمن لك مقعدك في هذه الجامعة الرائدة، لتبدأ رحلتك نحو القمة.')
hist_bsuir_en = (
                'BSUIR: Where Tech Leaders Are Born\n'
                '\n'
                'Do you dream of becoming an expert in Artificial Intelligence or a software engineer at a top global company? BSUIR is your ideal destination. It is the premier tech powerhouse of Belarus, specializing in Information Technology, Electronics, and Communications. Here, you will learn from top-tier professors and graduate with a globally recognized degree that opens doors to tech giants. With our company, we guarantee your place at this leading university, so you can start your journey to the top.')
hist_bsuir_ru = (
                'БГУИР: Где рождаются лидеры технологий\n'
                '\n'
                'Мечтаете стать экспертом в области искусственного интеллекта или инженером-программистом в ведущей мировой компании? БГУИР — это ваш идеальный выбор. Это главная техническая кузница Беларуси, специализирующаяся на информационных технологиях, электронике и связи. Здесь вы будете учиться у лучших профессоров и получите диплом, признаваемый во всём мире, который откроет вам двери в IT-гиганты. С нашей компанией мы гарантируем вам место в этом ведущем университете, чтобы начать ваш путь к вершине.')
hist_bsuir_fr = (
                'BSUIR : Là où naissent les leaders de la technologie\n'
                '\n'
                "Rêvez-vous de devenir un expert en Intelligence Artificielle ou un ingénieur logiciel dans une grande entreprise mondiale ? BSUIR est votre destination idéale. C'est la principale pépinière technologique de Biélorussie, spécialisée dans les Technologies de l'Information, l'Électronique et les Communications. Vous y étudierez auprès des meilleurs professeurs et obtiendrez un diplôme reconnu mondialement, vous ouvrant les portes des géants de la tech. Avec notre entreprise, nous vous garantissons une place dans cette université de premier plan pour commencer votre ascension vers le sommet.")
reg("historybsuira", hist_bsuir_ar, lambda: make_keyboard(add_back=True))
reg("historybsuire", hist_bsuir_en, lambda: make_keyboard(add_back=True))
reg("historybsuirr", hist_bsuir_ru, lambda: make_keyboard(add_back=True))
reg("historybsuirf", hist_bsuir_fr, lambda: make_keyboard(add_back=True))

# =============== GSTU ===============
def gstu_ar(): return make_keyboard(
    [("نبذة عن الجامعة", "historygstua")],
    [("التخصصات و الرسوم الجامعية", "https://drive.google.com/file/d/1HSA0-QyLeVGMe2lFIwC4KJ1bnMvtu09Z/view")],
    add_back=True)
def gstu_en(): return make_keyboard(
    [("About the University", "historygstue")],
    [("Majors and annual fees", "https://drive.google.com/file/d/14D0ePU6rL4NVbzUWNeyaRPi5wgkhyGs6/view")],
    add_back=True)
def gstu_ru(): return make_keyboard(
    [("Об университете", "historygstur")],
    [("Специальности и стоимость обучения", "https://drive.google.com/file/d/1UfzOB_vLoeND2BB3JgHXVd9y6mDQA_ys/view")],
    add_back=True)
def gstu_fr(): return make_keyboard(
    [("À propos de l'université", "historygstuf")],
    [("Spécialisations et frais annuels", "https://drive.google.com/file/d/1A7MnxVewDiWlnb3yxa_v4L_fKvuyIADB/view")],
    add_back=True)
reg("gstua", "جامعة غومل الحكومية للتقنيات سوخوي", gstu_ar)
reg("gstue", "Sukhoi Gomel State Technical University", gstu_en)
reg("gstur", "Гомельский государственный технический университет имени П.О. Сухого", gstu_ru)
reg("gstuf", "Université technique d'État de Gomel nommée d'après P.O. Soukhoï", gstu_fr)

hist_gstu_ar = (
                'جامعة غومل التقنية: مزيج الابتكار والفرص بأسعار تنافسية\n'
                '\n'
                'في مدينة غومل الهادئة والآمنة، تقع جامعة المستقبل. جامعة غومل الحكومية للتقنيات (GSTU) هي خيارك الذكي إذا كنت تبحث عن تعليم هندسي وتقني عالي الجودة بتكاليف اقتصادية جداً. تتميز الجامعة ببرامجها العملية القوية في الهندسة الميكانيكية، وتكنولوجيا المعلومات، والطاقة. هنا، ستتعلم داخل قاعات حديثة، وتتدرب عملياً في مصانع وشركات حقيقية. مع شركتنا، نجعل حلمك الدراسي في غومل واقعاً ميسوراً، بكل سهولة وأمان')
hist_gstu_en = (
                'GSTU: Innovation and Opportunity at an Affordable Price\n'
                '\n'
                'In the quiet and safe city of Gomel lies the university of the future. Gomel State Technical University (GSTU) is your smartest choice if you are looking for high-quality engineering and technical education at a very economical cost. The university is renowned for its strong hands-on programs in Mechanical Engineering, Information Technology, and Energy. Here, you will study in modern classrooms and train practically in real factories and companies. With our company, we make your dream of studying in Gomel an affordable reality, with ease and safety.')
hist_gstu_ru = (
                'ГГТУ: Инновации и возможности по доступной цене\n'
                '\n'
                'В тихом и безопасном городе Гомеле находится университет будущего. Гомельский государственный технический университет (ГГТУ) — ваш разумный выбор, если вы ищете качественное инженерно-техническое образование по очень экономичной стоимости. Университет славится своими сильными практическими программами в области машиностроения, информационных технологий и энергетики. Здесь вы будете учиться в современных аудиториях и проходить практику на реальных заводах и в компаниях. С нашей компанией мы сделаем вашу мечту об учёбе в Гомеле доступной, легко и безопасно.')
hist_gstu_fr = (
                "GSTU : Innovation et opportunités à un prix abordable\n"
                '\n'
                "Dans la ville calme et sûre de Gomel se trouve l'université du futur. L'Université Technique d'État de Gomel (GSTU) est votre choix le plus judicieux si vous recherchez une formation d'ingénieur et technique de haute qualité à un coût très économique. L'université est réputée pour ses solides programmes pratiques en Génie Mécanique, Technologies de l'Information et Énergie. Ici, vous étudierez dans des salles de classe modernes et vous vous entraînerez dans de vraies usines et entreprises. Avec notre société, nous faisons de votre rêve d'étudier à Gomel une réalité abordable, en toute simplicité et sécurité.")
reg("historygstua", hist_gstu_ar, lambda: make_keyboard(add_back=True))
reg("historygstue", hist_gstu_en, lambda: make_keyboard(add_back=True))
reg("historygstur", hist_gstu_ru, lambda: make_keyboard(add_back=True))
reg("historygstuf", hist_gstu_fr, lambda: make_keyboard(add_back=True))

# =============== МАГИСТРАТУРА / ДОКТОРАНТУРА ===============
def postgrad_ar(): return make_keyboard(
    [("WhatsApp", "https://wa.me/message/2552FHKOBKBYH1")],
    [("Telegram", "https://t.me/unihyper")],
    add_back=True)
def postgrad_en(): return make_keyboard(
    [("WhatsApp", "https://wa.me/message/2552FHKOBKBYH1")],
    [("Telegram", "https://t.me/unihyper")],
    add_back=True)
def postgrad_ru(): return make_keyboard(
    [("WhatsApp", "https://wa.me/message/2552FHKOBKBYH1")],
    [("Telegram", "https://t.me/unihyper")],
    add_back=True)
def postgrad_fr(): return make_keyboard(
    [("WhatsApp", "https://wa.me/message/2552FHKOBKBYH1")],
    [("Telegram", "https://t.me/unihyper")],
    add_back=True)
reg("magestra", "للاستعلام عن تخصصات الدراسات العليا (الماجستير و الدكتوراه) الرجاء التواصل بشكل مباشر مع شركة يوني هايبر", postgrad_ar)
reg("magestre", "For inquiries about postgraduate programs (Master's and Doctoral/PhD), please contact UniHyper directly.", postgrad_en)
reg("magestrr", "Для получения информации о специальностях магистратуры и аспирантуры (докторантуры), пожалуйста, свяжитесь напрямую с компанией UniHyper.", postgrad_ru)
reg("magestrf", "Pour toute question concernant les spécialités de master et de doctorat, veuillez contacter directement la société UniHyper.", postgrad_fr)

# =============== ЭКОНОМИКА (заглушка) ===============
reg("Economa", "ادارة أعمال و اقتصاد\n\nلمزيد من المعلومات، يرجى التواصل معنا عبر WhatsApp أو Telegram.", lambda: make_keyboard(
    [("WhatsApp", "https://wa.me/message/2552FHKOBKBYH1")],
    [("Telegram", "https://t.me/unihyper")],
    add_back=True))
reg("Econome", "Management and Economics\n\nFor more information, please contact us via WhatsApp or Telegram.", lambda: make_keyboard(
    [("WhatsApp", "https://wa.me/message/2552FHKOBKBYH1")],
    [("Telegram", "https://t.me/unihyper")],
    add_back=True))
reg("Economr", "Менеджмент и экономика\n\nДля получения дополнительной информации свяжитесь с нами через WhatsApp или Telegram.", lambda: make_keyboard(
    [("WhatsApp", "https://wa.me/message/2552FHKOBKBYH1")],
    [("Telegram", "https://t.me/unihyper")],
    add_back=True))
reg("Economf", "Gestion d'entreprise et économie\n\nPour plus d'informations, veuillez nous contacter via WhatsApp ou Telegram.", lambda: make_keyboard(
    [("WhatsApp", "https://wa.me/message/2552FHKOBKBYH1")],
    [("Telegram", "https://t.me/unihyper")],
    add_back=True))

# =============== ОБРАБОТЧИКИ ===============
@bot.message_handler()
def start_command(message):
    chat_id = message.chat.id
    user_state[chat_id] = {"msg_id": None, "current_callback": None, "history": []}
    text, mk = MENUS["start"]
    markup = mk()
    msg = bot.send_message(chat_id, text, reply_markup=markup)
    user_state[chat_id]["msg_id"] = msg.message_id
    user_state[chat_id]["current_callback"] = "start"

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    chat_id = call.message.chat.id
    data = call.data
    state = user_state.setdefault(chat_id, {"msg_id": None, "current_callback": None, "history": []})

    if data == "back":
        prev = pop_history(chat_id)
        if prev is None:
            prev = "start"
        if prev in MENUS:
            text, mk_fn = MENUS[prev]
            markup = mk_fn()
            try:
                bot.edit_message_text(text, chat_id, state["msg_id"], reply_markup=markup)
            except:
                msg = bot.send_message(chat_id, text, reply_markup=markup)
                state["msg_id"] = msg.message_id
            state["current_callback"] = prev
        return

    #if data == "url_wa":
     #   bot.send_message(chat_id, "Свяжитесь с нами: https://wa.me/message/2552FHKOBKBYH1")
      #  return

    #if data not in MENUS:
     #   bot.answer_callback_query(call.id, "Неизвестная команда")
      #  return

    # Сохраняем текущее меню в историю перед переходом
    cur = state.get("current_callback")
    if cur and cur != data and cur != "back":
        push_history(chat_id, cur)

    text, mk_fn = MENUS[data]
    markup = mk_fn()
    try:
        bot.edit_message_text(text, chat_id, call.message.message_id, reply_markup=markup)
    except:
        msg = bot.send_message(chat_id, text, reply_markup=markup)
        state["msg_id"] = msg.message_id
    else:
        state["msg_id"] = call.message.message_id

    state["current_callback"] = data

if __name__ == "__main__":
    print("Бот запущен...")
    bot.polling(non_stop=True)