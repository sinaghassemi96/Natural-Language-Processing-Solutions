import json
import hazm
from HW2.database.orm import TaskDB

from .patterns import Patterns
import re
from .parser import MixedRegexpParser


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

    def parse_task(self, groups):
        if 'TASK' in groups:
            if self.check_for_tasks(' '.join(word for word, tag in groups['TASK'])):
                return None
            return ' '.join(word for word, tag in groups['TASK'])

    def parse_period(self, groups, task: Task):
        if 'PERIOD' in groups:
            return ' '.join(word for word, tag in groups['PERIOD'])


    def parse_time(self, groups, task: Task):
        if 'TIME' in groups:
            return  ' '.join(word for word, tag in groups['TIME'])

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
                    name = self.parse_task(groups)
                    if not name:
                        continue
                    task = Task()
                    task.name = name
                    period = self.parse_period(groups, task)
                    time = self.parse_time(groups, task)
                    date = self.parse_date(groups, task)
                    done = False
                    cancel = False
                    self.db.create_task(name, time, date, period, done, cancel)
                if not self.tasks:
                    continue
            for pattern in self.patterns['CANCEL'] + self.patterns['UPDATE'] + self.patterns['DONE']:
                result = pattern.parse(tags)
                if result:
                    matches, groups = result
                    self.parse_edition(groups)

            for pattern in self.patterns['FETCH']:
                result = pattern.parse(tags)
                if result:
                    return self.db.find_all()
        # return self.db.find_all()

    def parse_edition(self, groups):
        if len(self.tasks) == 0:
            raise Exception('EMPTY.TASK.ARRAYS')
        if 'CANCEL' in groups:
            pass

    def parse_date(self, groups, task):
        if 'DATE' in groups:
            return ' '.join(word for word, tag in groups['DATE'])