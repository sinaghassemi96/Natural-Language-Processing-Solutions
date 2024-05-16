from opsdroid.skill import Skill
from opsdroid.matchers import match_event
from opsdroid.events import UserInvite, JoinRoom


class AcceptInvite(Skill):
    @match_event(UserInvite)
    async def user_invite(self, invite):
        print("\n --- User Invite --- \n")
        print(f"user invite -> {invite}")
        print(vars(invite))
        if isinstance(invite, UserInvite):
            await invite.respond(JoinRoom())