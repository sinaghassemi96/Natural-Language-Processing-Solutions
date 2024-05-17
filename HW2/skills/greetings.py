import random

from opsdroid.matchers import match_regex
from opsdroid.skill import Skill


class HelloSkill(Skill):
    @match_regex(r'hi|hello|hey|hallo|سلام|درود|چطوری', case_sensitive=False)
    async def hello(self, message):
        text = random.choice(
            ["سلام {}", "سلام بر {}", "درود {}", "خوش اومدی {}"]).format(message.user)
        await message.respond(text)

    @match_regex(r'bye( bye)?|see y(a|ou)|au revoir|gtg|I(\')?m off|خدافظ|خداحافظ|ما رفتیم|فعلا', case_sensitive=False)
    async def bye(self, message):
        text = random.choice(
            ["به امید دیدار {}", "مخلصم {}", "بای‌بای {}"]).format(message.user)
        await message.respond(text)
