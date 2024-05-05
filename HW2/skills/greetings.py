from opsdroid.skill import Skill
from opsdroid.matchers import match_parse


class HelloSkill(Skill):
    @match_parse(r'repeat {key}')
    async def hello(self, message):
        await message.respond(message.entities['key']['value'])
