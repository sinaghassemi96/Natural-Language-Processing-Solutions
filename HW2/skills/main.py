from opsdroid.matchers import match_regex, match_parse
from opsdroid.skill import Skill

import sys
import os

#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'task_extractor')))
sys.path.append(os.getcwd())

from task_extractor.extractor import *
import hazm


def __doc__() -> str:
    return '''
    این دستیار برای مدیریت رویدادها و وقایع است. با نوشتن کلمه‌ی دستور و دادن پیغام خود رویدادهای جدید اضافه کنبد،
    لغو کنید، به‌روزرسانی‌ کنید و ...
    '''


def __name__() -> str:
    return '''
    بخش اصلی'''


class BotSkill(Skill):

    def __init__(self, opsdroid, config, *args, **kwargs):
        super().__init__(opsdroid, config, *args, **kwargs)
        self.extractor = TaskExtractor()

    @match_parse(r'command {key}')
    async def add_event(self, message):
        print(message)
        res = self.extractor.run(str(message.entities['key']['value']))
        print(res)
        if res:
            await message.respond(str(res))
        else:
            await message.respond('باشه.')