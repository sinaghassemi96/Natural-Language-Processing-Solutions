from opsdroid.matchers import match_regex
from opsdroid.skill import Skill


class GuideSkill(Skill):
    @match_regex(r"guide|راهنما")
    async def provide_guide(opsdroid, config, message):
        await message.respond(guide)


guide = """
**Event Management Guide**

Welcome to the event management guide for opsdroid! This guide will walk you through the process of managing events using natural language inputs.

**Creating an Event**

To create a new event, simply type a message in the following format:

`"Create event <event_name> on <date> at <time>"`

Example: `"Create event Meeting on Friday at 2pm"`

**Updating an Event**

To update an existing event, type a message in the following format:

`"Update event <event_name> to <new_date> at <new_time>"`

Example: `"Update event Meeting to Thursday at 3pm"`

**Canceling an Event**

To cancel an existing event, type a message in the following format:

`"Cancel event <event_name>"`

Example: `"Cancel event Meeting"`

**Marking an Event as Done**

To mark an event as done, type a message in the following format:

`"Done with event <event_name>"`

Example: `"Done with event Meeting"`

**Available Commands**

Here are the available commands for managing events:

* `Create event <event_name> on <date> at <time>`
* `Update event <event_name> to <new_date> at <new_time>`
* `Cancel event <event_name>`
* `Done with event <event_name>`

**Tips and Tricks**

* You can use natural language to create and manage events. For example, you can say "Create a meeting on Friday" instead of "Create event Meeting on Friday".
* You can use abbreviations for dates and times. For example, "tom" for tomorrow, "next mon" for next Monday, etc.
* You can use the `list events` command to view all upcoming events.

I hope this guide helps you get started with managing events using opsdroid! If you have any questions or need further assistance, feel free to ask.
"""