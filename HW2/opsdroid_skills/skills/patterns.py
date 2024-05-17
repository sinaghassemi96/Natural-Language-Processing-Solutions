from .parser import MixedRegexpParser

months = ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند']
time_of_day = ['ظهر', 'صبح', 'عصر', 'شب', 'بامداد', 'فردا', 'بعدازظهر', ]


def agg_words(tag, words):
    return f"(?:<'(?:{'|'.join(words)})','{tag}'>)"


class Patterns:
    ANY = r"[^']+"
    ANY_P = r"'[^']+'"
    ANY_T = f"(?:<{ANY_P},{ANY_P}>)"
    AGG_WORDS = lambda tag, words: f"(?:<'(?:{'|'.join(words)})','{tag}'>)"
    AGG_P = lambda patterns: f"(?:{'|'.join(patterns)})"
    NOUN = f"(?:<{ANY_P},'NOUN'>)"
    ADJ = f"(?:<{ANY_P},'ADJ'>)"
    NUM = f"(?:<{ANY_P},'NUM'>)"
    VERB = f"(?:<{ANY_P},'VERB'>)"
    ADP = f"(?:<{ANY_P},'ADP'>)"
    ADVP = f"(?:<{ANY_P},'ADVP'>)"
    ADV = f"(?:<{ANY_P},'ADV'>)"
    CCONJ = f"(?:<{ANY_P},'CCONJ'>)"
    DET = f"(?:<{ANY_P},'DET'>)"
    NP_T = f"(?:<{ANY_P},'NP'>)"
    VP_T = f"(?:<{ANY_P},'VP'>)"
    NUM_GROUP = f"(?:{NUM}(?:{CCONJ}{NUM})*)"
    NP = f"(?:{DET}*{NOUN}(?:{NOUN}|{ADJ}|{NUM_GROUP})*)"
    NP_GROUP = f"(?:{NP}(?:{CCONJ}|{ADP}{NP})*)"
    VP = f"(?:(?:{NOUN}|{ADJ})?{VERB})"
    MONTH = f"(?:{agg_words('NOUN', months)})"
    TIME_OF_DAY = f"(?:{agg_words('NOUN', time_of_day)})"
    TIME = f"(?:<'\d+(?::\d+){{1, 2}}?','NUM'>{TIME_OF_DAY}*)"
    DATE = f"(?:{NUM_GROUP}{MONTH})"
    DATETIME = f"(?:{DATE}{TIME}|{TIME}{DATE}|{DATE}|{TIME})"
    TASK_WORDS = ['وظیفه', 'تسک', 'کار', ]
    ASSIGNEE_WORDS = ['مسئول', 'مسئولین', 'مسئولان', 'مسئولیت']
    START_WORDS = ['شروع', 'استارت']
    END_WORDS = ['پایان', 'تمام', 'انجام', 'تحویل', 'تمدید', 'دان', 'مختوم']

    CREATE_TASK_NOUNS = ['یادم', 'حواسم', 'نیاز', 'یادآوری', 'یاداوری', 'فراموش',
                         'حواسم', 'خاطرم', ]
    UPDATE_TASK_WORDS = ['تغییر', 'آپدیت', 'بروزرسانی', 'به‌روزرسانی', 'جابجا']
    FINISH_TASK_WORDS = ['انجام', 'تمام', 'پایان']
    CANCEL_TASK_WORDS = ['لغو', 'کنسل', 'منتفی', 'کنکل']
    FETCH_TASK_WORDS = ['نشان']
    TASK_VERBS = ['باشه', 'شد', 'بده', 'دارم', 'نکنم', 'نشه', 'بکن', 'یافت', 'کند']

    TASK_PERIODS = ['روزانه', 'هر روز', 'هر دو روز', 'هفتگی', 'ماهانه', 'امروز', 'فردا']
    PLAN_WORDS = ['برنامه', 'پلن']
    TASK_TIME = ['ساعت', 'زمان']
    TASK_IDENTIFIER = ['به']

    TASK = f"(?P<TASK>{NP})"

    DECLARATION = [
        f"(?:{agg_words('NOUN', CREATE_TASK_NOUNS)}{agg_words('VERB', TASK_VERBS)}"
        f"+(?P<PERIOD>{DET}*{NOUN}|{ADV})*(?P<DATE>{DATE})*(?P<TIME>{DATETIME}|{NP}{NUM}*)*"
        f"+(?P<ADP>{agg_words('ADP', TASK_IDENTIFIER)}){TASK}(?P<ACTION>{VERB}))",
        f"(?:{agg_words('NOUN', CREATE_TASK_NOUNS)}{agg_words('ADP', TASK_IDENTIFIER)}"
        f"{agg_words('NOUN', CREATE_TASK_NOUNS)}{agg_words('VERB', TASK_VERBS)}{ANY_T}*"
        f"(?P<PERIOD>({DET}*{NOUN})|{ADV})(?P<TIME>{DATETIME}|{NP}{NUM}*)"
        f"(?P<ADP>{agg_words('ADP', TASK_IDENTIFIER)}){TASK}(?P<ACTION>{VERB}))",
    ]

    CANCEL = [
        f"(?:{agg_words('NOUN', TASK_WORDS)}+(?P<ADP>{agg_words('ADP', TASK_IDENTIFIER)})*{TASK}"
        f"{ANY_T}*(?P<DATE>{DATETIME})*{ANY_T}*(?P<TIME>{DATETIME})*"
        f"(?P<CANCEL>{agg_words('NOUN', CANCEL_TASK_WORDS)}{agg_words('VERB', TASK_VERBS)}))",
        f"(?P<DATE>{DATE})"
    ]

    UPDATE = [
        f"(?:{agg_words('NOUN', TASK_WORDS)}(?P<ADP>{agg_words('ADP', TASK_IDENTIFIER)})*{TASK}"
        f"{ANY_T}*(?P<DATE>{DATE})?{ANY_T}*(?P<TIME>{DATETIME})*"
        f"(?P<UPDATE>{agg_words('NOUN', UPDATE_TASK_WORDS)}{agg_words('VERB', TASK_VERBS)}))",
    ]

    DONE = [
        f"(?:{agg_words('NOUN', TASK_WORDS)}(?P<ADP>{agg_words('ADP', TASK_IDENTIFIER)})*{TASK}"
        f"+{ANY_T}*(?P<DONE>{agg_words('NOUN', FINISH_TASK_WORDS)}{agg_words('VERB', TASK_VERBS)}))"
    ]

    FETCH = [
        f"(?:{agg_words('NOUN', PLAN_WORDS)}(?P<PERIOD>{agg_words('ADJ', TASK_PERIODS)}){ANY_T}"
        f"*(?P<SHOW>{agg_words('NOUN', FETCH_TASK_WORDS)}{agg_words('VERB', TASK_VERBS)})+)",
        f"(?:{agg_words('NOUN', PLAN_WORDS)}(?P<DATE>{DATE})(?P<SHOW>{agg_words('NOUN', FETCH_TASK_WORDS)}"
        f"{agg_words('VERB', TASK_VERBS)})+)"
    ]

    def __init__(self):
        self.compiled = {}

    def __getitem__(self, key):
        if key not in self.compiled:
            if isinstance(self.__class__.__dict__[key], str):
                self.compiled[key] = MixedRegexpParser(self.__class__.__dict__[key])
            else:
                self.compiled[key] = [MixedRegexpParser(pattern) for pattern in self.__class__.__dict__[key]]
        return self.compiled[key]
