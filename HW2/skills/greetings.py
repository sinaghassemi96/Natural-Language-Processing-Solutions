import random

from opsdroid.matchers import match_parse, match_regex
from opsdroid.skill import Skill


class HelloSkill(Skill):
    @match_regex(r'hi')
    async def hello(self, message):
        text = random.choice(
            ["سلام {}", "سلام بر {}", "درود {}", "خوش اومدی {}"]).format(message.user)
        await message.respond(text)

    @match_parse(r'خدافظ')
    async def bye(self, message):
        text = random.choice(
            ["به امید دیدار {}", "مخلصم {}", "بای‌بای {}"]).format(message.user)
        await message.respond(text)
