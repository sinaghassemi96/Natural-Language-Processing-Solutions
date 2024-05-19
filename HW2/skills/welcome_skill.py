from opsdroid.skill import Skill
from opsdroid.events import Message
from opsdroid.matchers import match_event
import logging

_LOGGER = logging.getLogger(__name__)

class WelcomeSkill(Skill):
    def __init__(self, opsdroid, config):
        super(WelcomeSkill, self).__init__(opsdroid, config)
        _LOGGER.info("Welcome skill initialized")

    @match_event(Message)
    async def on_startup(self, event):
        # Ensure this only runs once on startup
        if event.text == "opsdroid startup":
            note = self.config.get("note", 'سلام! به دستیار مدیریت وقایع خوش آمدید. \n برای مشاهده‌ی راهنما، help و برای افزودن یک واقعه به تقویم، ابتدا command نوشته و کار خود را اعلام کنید.')
            await event.respond(note)
