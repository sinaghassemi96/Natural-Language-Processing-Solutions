import datetime
import json
import re

import hazm
from persiantools.jdatetime import JalaliDate

# from ..database.orm import TaskDB
from .patterns import Patterns

calendar_limit = 60  # no. of days the planner works


def jalali_date_to_str(date: JalaliDate) -> str:
    return '-'.join([str(i) for i in [date.year, date.month, date.day]])


def reform_chunker_array(text: str) -> list:
    pattern = r'\[([^\]]+)\]'
    tagged_words = re.findall(pattern, text)
    return [(' '.join(p for p in pair.split()[:-1]), pair.split()[-1]) for pair in tagged_words]


class Task:
    def __init__(self, name, period, time, date):
        self.name = name
        self.period = period
        self.time = time
        self.date = date
        self.done = False
        self.cancel = False

    def __repr__(self):
        return json.dumps(self.__dict__, indent=4, ensure_ascii=False)


def detect_date(groups):
    if 'DATE' in groups:
        return ' '.join(word for word, tag in groups['DATE'])
    elif 'PERIOD' in groups:
        period = ' '.join(word for word, tag in groups['PERIOD'])
        if period in ['امروز'] or period is None:
            date = JalaliDate.today()
            return jalali_date_to_str(date)
        elif period in ['فردا']:
            date = JalaliDate.today() + datetime.timedelta(days=1)
            return jalali_date_to_str(date)
    return None


def parse_period(groups):
    if 'PERIOD' in groups:
        return ' '.join(word for word, tag in groups['PERIOD'])


def parse_time(groups):
    if 'TIME' in groups:
        return ' '.join(word for word, tag in groups['TIME'])


class TaskExtractor:
    normalizer = hazm.Normalizer()
    sent_tokenizer = hazm.SentenceTokenizer()
    word_tokenizer = hazm.WordTokenizer()
    POS_tagger = hazm.POSTagger(model='models/pos_tagger.model')
    chunker = hazm.Chunker(model='models/chunker.model')
    stemmer = hazm.Stemmer()
    lemmatizer = hazm.Lemmatizer()
    patterns = Patterns()

    def __init__(self):
        self.tasks = []
        # self.db = TaskDB()

    def check_for_tasks(self, name):
        for task in self.tasks:
            if task.name.startswith(name) or name.startswith(task.name):
                return True
        return False

    def parse_task_name(self, groups):
        if 'TASK' in groups:
            if self.check_for_tasks(' '.join(word for word, tag in groups['TASK'])):
                return None
            name = ' '.join(word for word, tag in groups['TASK'])
            if 'ACTION' in groups:
                name = name + ' ' + self.lemmatizer.lemmatize([word for word, tag in groups['ACTION']][0]).split('#')[
                    0] + 'ن'
            if 'ADP' in groups:
                name = self.lemmatizer.lemmatize([word for word, tag in groups['ADP']][0]) + ' ' + name
            return name

    def parse_name(self, groups):
        if 'NAME' in groups:
            if self.check_for_tasks(' '.join(word for word, tag in groups['NAME'])):
                return None
            return ' '.join(word for word, tag in groups['NAME'])

    def run(self, command: str) -> list[Task]:
        command = self.normalizer.normalize(command)
        for text in command.split('.'):
            if text is not None or text != '':
                for sent in self.sent_tokenizer.tokenize(text):
                    words = self.word_tokenizer.tokenize(sent)
                    # tags = reform_chunker_array(tree2brackets(self.chunker.parse(self.POS_tagger.tag(words))))
                    words = [self.stemmer.stem(word) if '\u200C' in word else word for word in words]
                    tags = self.POS_tagger.tag(words)
                    tags = [tag for tag in tags if tag[1] != 'PUNCT']
                    for pattern in self.patterns['DECLARATION']:
                        result = pattern.parse(tags)
                        if result:
                            matches, groups = result
                            name = self.parse_task_name(groups)
                            if not name:
                                continue
                            period = parse_period(groups)
                            time = parse_time(groups)
                            date = detect_date(groups)
                            task = Task(name, period, time, date)
                            self.create_task(task)
                        if not self.tasks:
                            continue
                    for pattern in self.patterns['CANCEL'] + self.patterns['UPDATE'] + self.patterns['DONE']:
                        result = pattern.parse(tags)
                        if result:
                            matches, groups = result
                            name = self.parse_task_name(groups)
                            date = detect_date(groups)
                            time = parse_time(groups)
                            task = self.find_task(name, date, time)
                            self.edit_task(groups, task)

                    for pattern in self.patterns['FETCH']:
                        result = pattern.parse(tags)
                        if result:
                            return self.find_all()

    def edit_task(self, groups, task, database=False):
        if database:
            if self.db.count_tasks() == 0:
                raise Exception('EMPTY.TASK.ARRAYS')
        else:
            if len(self.tasks) == 0:
                raise Exception('EMPTY.TASK.ARRAYS')
        is_done = False
        is_cancelled = False
        time = parse_time(groups)
        date = detect_date(groups)
        time = task.time if time is not None else time
        date = task.date if date is not None else date
        if 'CANCEL' in groups:
            is_cancelled = True
        if 'DONE' in groups:
            is_done = True
        if 'UPDATE' in groups:
            time = parse_time(groups)
            date = detect_date(groups)
        if database:
            self.db.update_task(task['id'], time, date, is_done, is_cancelled)
        else:
            for t in self.tasks:
                if t.name == task.name:
                    t.date = date
                    t.time = time
                    t.done = is_done
                    t.cancel = is_cancelled

    def get_tasks(self):
        return self.db.find_all()

    def create_task(self, task, database=False):
        global calendar_limit
        period_to_delta = {
            'هر روز': 1, 'روزانه': 1,
            'هر دو روز': 2, 'هر 2 روز': 2, 'دو روز در میان': 2, '2 روز در میان': 2, 'دو روز یکبار': 2,
            'هر سه روز': 3, 'هر 3 روز': 3, 'سه روز در میان': 3, '3 روز در میان': 3, 'سه روز یکبار': 3,
            'هفتگی': 7, 'هفته‌ای یکبار': 7,
            'دو هفته یکبار': 14, 'هر دو هفته': 14,
            'ماهانه': 30, 'هر ماه': 30
        }

        delta = 1
        today = 0
        if task.period is None or task.period == '' or task.period in ['امروز']:
            calendar_limit = 1
        if task.period in ['فردا']:
            today = 1
            calendar_limit = 2
        else:
            delta = period_to_delta.get(task.period, 1)
            if delta is None:
                delta = 1
        for i in range(today, calendar_limit, delta):
            cur_date = JalaliDate.today() + datetime.timedelta(days=i)
            task.date = jalali_date_to_str(cur_date)
            if database:
                self.db.create_task(task.name, task.time, task.date, task.period, task.done, task.cancel)
            else:
                self.tasks.append(Task(task.name, task.period, task.time, task.date))

    def find_all(self, database=False):
        if database:
            return self.db.find_all()
        else:
            return self.tasks

    def find_task(self, name, date, time, database=False):
        if database:
            self.db.find_task(name, None, None)
        else:
            for t in self.tasks:
                if t.name == name:
                    return t
