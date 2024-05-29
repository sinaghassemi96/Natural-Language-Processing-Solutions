import logging

from opsdroid.events import JoinRoom, Message
from opsdroid.matchers import match_regex, match_event
from opsdroid.skill import Skill


class Helper(Skill):

    def __init__(self, opsdroid, config):
        super(Helper, self).__init__(opsdroid, config)
        self.opsdroid = opsdroid

    @match_regex(r"help$|کمک|راهنما")
    @match_event(JoinRoom)
    async def help(self, message):

        response = ('سلام، به دستیار ثبت رویدادها و وقایع خوش آمدید. برای فرستادن دستور، ابتدا یک command نوشته و '
                    'سپس فرمان خود را وارد کنید. مثلاً \n'
                    'command یادم باشه فردا ساعت 8 به حل تمرین بپردازم -> یک تسک به وظایف شما اضافه می‌کند.'
                    'command برنامه هفتگی‌ام را نشان بده. -> برنامه‌ی شما را باز می‌گرداند.'
                    'command پرداختن به حل تمرین فردا را به ساعت 9 تغییر بده. -> زمان را تغییر می‌دهد.'
                    'command کار تماس با دوستم انجام شد -> کار را به وضعیت انجام‌شده می‌برد.')

        # """help - Displays this help message"""
        # response = []
        # for skill in self.opsdroid.skills:
        #     if skill.__doc__:
        #         response.append("{}: {}".format(skill.__name__, skill.__doc__))
        #     else:
        #         doc_string_not_found = "doc string not found for {}".format(
        #             skill.__name__
        #         )
        #         logging.debug(doc_string_not_found)
        #         response.append(skill.__name__)
        await self.opsdroid.default_connector.send(Message(text=response, target=message.target))
        await message.respond(response)

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
