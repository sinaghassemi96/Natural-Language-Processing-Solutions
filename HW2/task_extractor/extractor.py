import json
import re

import hazm

from HW2.database.orm import TaskDB
from .patterns import Patterns


def reform_chunker_array(text: str) -> list:
    pattern = r'\[([^\]]+)\]'
    tagged_words = re.findall(pattern, text)
    return [(' '.join(p for p in pair.split()[:-1]), pair.split()[-1]) for pair in tagged_words]


class Task:
    def __init__(self):
        self.name = ''
        self.period = ''
        self.time = ''
        self.date = ''
        self.done = False
        self.cancel = False

    def __repr__(self):
        return json.dumps(self.__dict__, indent=4, ensure_ascii=False)


def parse_date(groups):
    if 'DATE' in groups:
        return ' '.join(word for word, tag in groups['DATE'])


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
        self.db = TaskDB()

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
                name = name + ' ' + self.lemmatizer.lemmatize([word for word, tag in groups['ACTION']][0]).split('#')[0] + 'ن'
            if 'ADP' in groups:
                name = self.lemmatizer.lemmatize([word for word, tag in groups['ADP']][0]) + ' ' + name
            return name

    def parse_name(self, groups):
        if 'NAME' in groups:
            if self.check_for_tasks(' '.join(word for word, tag in groups['NAME'])):
                return None
            return ' '.join(word for word, tag in groups['NAME'])

    def run(self, text: str) -> list[Task]:
        text = self.normalizer.normalize(text)
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
                    task = Task()
                    task.name = name
                    period = parse_period(groups)
                    time = parse_time(groups)
                    date = parse_date(groups)
                    done = False
                    cancel = False
                    self.db.create_task(name, time, date, period, done, cancel)
                if not self.tasks:
                    continue
            for pattern in self.patterns['CANCEL'] + self.patterns['UPDATE'] + self.patterns['DONE']:
                result = pattern.parse(tags)
                if result:
                    matches, groups = result
                    name = self.parse_task_name(groups)
                    date = parse_date(groups)
                    time = parse_time(groups)
                    task = self.db.find_task(name, None, None)
                    self.parse_edition(groups, task)

            for pattern in self.patterns['FETCH']:
                result = pattern.parse(tags)
                if result:
                    return self.db.find_all()

    def parse_edition(self, groups, task):
        if self.db.count_tasks() == 0:
            raise Exception('EMPTY.TASK.ARRAYS')
        is_done = False
        is_cancelled = False
        time = task['time']
        if 'CANCEL' in groups:
            is_cancelled = True
        if 'DONE' in groups:
            is_done = True
        if 'UPDATE' in groups:
            time = parse_time(groups)
        self.db.update_task(task['id'], time, task['date'], is_done, is_cancelled)

    def get_tasks(self):
        return self.db.find_all()
