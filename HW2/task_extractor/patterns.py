from .parser import MixedRegexpParser

months = ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند']

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
        CCONJ = f"(?:<{ANY_P},'CCONJ'>)"
        DET = f"(?:<{ANY_P},'DET'>)"
        NP_T = f"(?:<{ANY_P},'NP'>)"
        VP_T = f"(?:<{ANY_P},'VP'>)"
        NUM_GROUP = f"(?:{NUM}(?:{CCONJ}{NUM})*)"
        NP = f"(?:{DET}?{NOUN}(?:{NOUN}|{ADJ}|{NUM_GROUP})*)"
        NP_GROUP = f"(?:{NP}(?:{CCONJ}{NP})*)"
        VP = f"(?:(?:{NOUN}|{ADJ})?{VERB})"
        MONTH = f"""(?:{agg_words('NOUN', months)})"""
        TIME = r"(?:<'\d+:\d+(?::\d+)?','NUM'>)"
        DATE = f"(?:{NUM_GROUP}{MONTH})"
        DATETIME = f"(?:{DATE}{TIME}|{TIME}{DATE}|{DATE}|{TIME})"
        TASK_WORDS = ['وظیفه', 'تسک']
        ASSIGNEE_WORDS = ['مسئول', 'مسئولین', 'مسئولان', 'مسئولیت']
        START_WORDS = ['شروع', 'استارت']
        END_WORDS = ['پایان', 'تمام', 'انجام', 'تحویل', 'تمدید']

        CREATE_TASK_NOUNS = ['یادم',]
        CREATE_TASK_VERBS = ['باشه']

        TASK_PERIODS = ['روزانه', 'هر روز', 'هر دو روز',]
        TASK_TIME = ['ساعت']
        TASK_IDENTIFIER = ['به']

        # TASK = f"(?:{agg_words('NOUN', TASK_WORDS)}(?P<NAME>{NP}))"
        TASK = f"(?P<TASK>{NP})"
        DECLARATIONS = [
            f"(?:{agg_words('NOUN', CREATE_TASK_NOUNS)}{agg_words('VERB', CREATE_TASK_VERBS)}+(?P<PERIOD>{DET}{NOUN})+(?P<TIME>{NP})+({agg_words('ADP', TASK_IDENTIFIER)}{TASK}{VERB}))",
            f"(?:{TASK}?{ANY_T}*{agg_words('NOUN', ['لغو'])}{agg_words('VERB', ['کن'])})"
        ]
        ASSIGNMENTS = [
            f"{AGG_WORDS(ANY, ASSIGNEE_WORDS)}{NP}*(?P<ASSIGNEES>{NP_GROUP}){VERB}",
            f"(?P<ASSIGNEES>{NP_GROUP}){AGG_WORDS(ANY, ASSIGNEE_WORDS)}{NP}*{VERB}",
        ]
        UPDATE_START_DATES = [
            f"(?:{agg_words(ANY, START_WORDS)}{agg_words('NOUN', TASK_WORDS)}{NP}?{ADP}+(?P<START_DATE>{DATETIME}){VP})",
            f"(?:{agg_words(ANY, START_WORDS)}{NP}?{agg_words('NOUN', TASK_WORDS)}{ADP}+(?P<START_DATE>{DATETIME}){VP})",
            f"(?:(?P<START_DATE>{DATETIME}){NP}?{ADP}+{agg_words(ANY, START_WORDS)}{VERB})",
            f"(?:{DET}?{agg_words('NOUN', TASK_WORDS)}{NP}?{ADP}+(?P<START_DATE>{DATETIME}){agg_words(ANY, START_WORDS)}{VERB})"
        ]
        SUBTASK_DECLARATIONS = [

        ]
        UPDATE_DEADLINES = [
            f"(?:{agg_words(ANY, ['مهلت', 'ددلاین'])}{DET}?{agg_words('NOUN', TASK_WORDS)}{NP}?{ADP}*(?P<END_DATE>{DATETIME}){VP})",
            f"(?:{DET}?{agg_words('NOUN', TASK_WORDS)}{NP}?{ADP}+(?P<END_DATE>{DATETIME}){agg_words(ANY, END_WORDS)}{VERB})",
            f"(?:{agg_words(ANY, END_WORDS)}{DET}?{agg_words('NOUN', TASK_WORDS)}{NP}?{ADP}*(?P<END_DATE>{DATETIME}){VERB})",
        ]

        DONES = [
            f"(?:{agg_words('NOUN', TASK_WORDS)}{ADP}?{NP}?{agg_words(ANY, END_WORDS)}{VERB})"
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