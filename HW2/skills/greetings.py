import random

from opsdroid.skill import Skill
from opsdroid.matchers import match_parse


class HelloSkill(Skill):
    @match_parse(r'hi|hello|hey|hallo|سلام|درود|چطوری', case_sensitive=False)
    async def hello(self, message):
        text = random.choice(
            ["سلام {}", "سلام بر {}", "درود {}", "خوش اومدی {}"]).format(message.user)
        await message.respond(text)

    @match_parse(r'bye( bye)?|see y(a|ou)|au revoir|gtg|I(\')?m off|خدافظ|خداحافظ|ما رفتیم|فعلا', case_sensitive=False)
    async def bye(self, message):
        text = random.choice(
            ["به امید دیدار {}", "مخلصم {}", "بای‌بای {}"]).format(message.user)
        await message.respond(text)
