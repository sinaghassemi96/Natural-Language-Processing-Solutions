import logging

from opsdroid.matchers import match_regex
from opsdroid.skill import Skill


class Helper(Skill):
    @match_regex(r"help$|کمک|راهنما")
    async def help(self, message):
        """help - Displays this help message"""
        await message.respond('سلام! به دستیار مدیریت وقایع خوش آمدید. برای افزودن یک واقعه به تقویم، ابتدا command نوشته و کار خود را اعلام کنید.')

    @match_regex(r"help (.*)")
    async def help_skill(self, message):
        """help <skill_name> - Displays usage for provided skill"""
        logging.debug("searching for {}".format(message.regex))
        found_skill = next(
            (
                skill
                for skill in self.opsdroid.skills
                if skill.__name__ == message.regex.group(1)
            ),
            False,
        )
        if not found_skill:
            response = "{} skill not found".format(message.regex.group(1))
        elif not found_skill.__doc__:
            response = "No usage found for {}".format(found_skill.__name__)
        else:
            response = found_skill.__doc__
        await message.respond(response)
