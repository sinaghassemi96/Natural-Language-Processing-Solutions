from opsdroid.skill import Skill
from opsdroid.matchers import match_event
from opsdroid.events import UserInvite, JoinRoom, Message


class AcceptInvite(Skill):
    @match_event(UserInvite)
    async def user_invite(self, invite):
        print("\n --- User Invite --- \n")
        print(f"user invite -> {invite}")
        print(vars(invite))
        if isinstance(invite, UserInvite):
            await invite.respond(JoinRoom())
            welcome_note = 'سلام! به دستیار مدیریت وقایع خوش آمدید. برای افزودن یک واقعه به تقویم، ابتدا command نوشته و کار خود را اعلام کنید.'
            await invite.respond(Message(text=welcome_note))