import json
import hazm
from task_extractor.patterns import Patterns
import re
from task_extractor.parser import MixedRegexpParser

class Task:
    def __init__(self):
        self.name = ''
        self.subtasks = []
        self.assignees = []
        self.start_date = ''
        self.end_date = ''
        self.is_done = False

    def __repr__(self):
        return json.dumps(self.__dict__, indent=4, ensure_ascii=False)

class TaskExtractor:
    normalizer = hazm.Normalizer()
    sent_tokenizer = hazm.SentenceTokenizer()
    word_tokenizer = hazm.WordTokenizer()
    POS_tagger = hazm.POSTagger(model='models/pos_tagger.model')
    lemmatizer = hazm.Lemmatizer()
    patterns = Patterns()

    def __init__(self):
        self.tasks = []
    
    def check_for_tasks(self, name):
        for task in self.tasks:
            if task.name.startswith(name) or name.startswith(task.name):
                return True
        return False
    
    def parse_name(self, groups):
        if 'NAME' in groups:
            if self.check_for_tasks(' '.join(word for word, tag in groups['NAME'])):
                return None
            return ' '.join(word for word, tag in groups['NAME'])
    
    def parse_start_date(self, task, groups):
        if 'START_DATE' in groups:
            task.start_date = ' '.join(word for word, tag in groups['START_DATE'])
    
    def parse_end_date(self, task, groups):
        if 'END_DATE' in groups:
            task.end_date = ' '.join(word for word, tag in groups['END_DATE'])
    
    def parse_assignees(self, task, groups):
        if 'ASSIGNEES' in groups:
            task.assignees = ['']
            for i, (word, tag) in enumerate(groups['ASSIGNEES']):
                if word in self.patterns.TASK_WORDS:
                    groups['ASSIGNEES'] = groups['ASSIGNEES'][i+1:]
                    break
            for word, tag in groups['ASSIGNEES']:
                if tag == 'CCONJ':
                    task.assignees[-1] = task.assignees[-1][:-1]
                    task.assignees.append('')
                else:
                    task.assignees[-1] += word + ' '
            task.assignees[-1] = task.assignees[-1][:-1]
    
    def parse_subtasks(self, task, groups):
        if 'SUBTASKS' in groups:
            task.subtasks = ['']
            for i, (word, tag) in enumerate(groups['SUBTASKS']):
                if re.match(r"ابتدا|اول", word):
                    continue
                elif re.match(r"سپس|بعد", word):
                    if i > 1 and re.match(r'CCONJ', groups['SUBTASKS'][i - 1][1]):
                        task.subtasks[-1] = task.subtasks[-1][:-len(groups['SUBTASKS'][i - 1][0]) - 1]
                    task.subtasks[-1] = task.subtasks[-1][:-1]
                    task.subtasks.append('')
                else:
                    task.subtasks[-1] += word + ' '
            task.subtasks[-1] = task.subtasks[-1][:-1]

    def run(self, text: str) -> list[Task]:
        text = self.normalizer.normalize(text)
        for sent in self.sent_tokenizer.tokenize(text):
            words = self.word_tokenizer.tokenize(sent)
            tags = self.POS_tagger.tag(words)
            tags = [tag for tag in tags if tag[1] != 'PUNCT']
            for pattern in self.patterns['DECLARATIONS']:
                result = pattern.parse(tags)
                if result:
                    matches, groups = result
                    name = self.parse_name(groups)
                    if not name:
                        continue
                    task = Task()
                    task.name = name
                    self.parse_start_date(task, groups)
                    self.parse_end_date(task, groups)
                    self.parse_assignees(task, groups)
                    self.parse_subtasks(task, groups)
                    self.tasks.append(task)
            if not self.tasks:
                continue
            for pattern in self.patterns['ASSIGNMENTS'] + self.patterns['UPDATE_START_DATES'] + self.patterns['UPDATE_DEADLINES'] + self.patterns['SUBTASK_DECLARATIONS']:
                result = pattern.parse(tags)
                if result:
                    matches, groups = result
                    self.parse_assignees(self.tasks[-1], groups)
                    self.parse_subtasks(self.tasks[-1], groups)
                    self.parse_start_date(self.tasks[-1], groups)
                    self.parse_end_date(self.tasks[-1], groups)
            for pattern in self.patterns.DONES:
                result = MixedRegexpParser(pattern).parse(tags)
                if result:
                    matches, groups = result
                    self.tasks[-1].is_done = True
        return self.tasks