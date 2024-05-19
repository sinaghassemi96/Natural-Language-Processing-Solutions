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
            help_note = self.config.get("help_note", "Hello! Here are some commands you can use:\n- `help`: Show this help message\n- `start`: Start the bot\n- `status`: Check bot status")
            await event.respond(help_note)
