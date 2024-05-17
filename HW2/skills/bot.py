from opsdroid.matchers import match_regex
from opsdroid.skill import Skill

from ..task_extractor.extractor import TaskExtractor


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

    @match_regex(r'command {key}|دستور {key}', case_sensitive=False)
    async def add_event(self, text):
        await text.repond(self.extractor.run(text.entities['key']['value']))
