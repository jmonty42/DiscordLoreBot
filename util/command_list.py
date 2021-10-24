from commands.authorize import authorize
from commands.clear import clear
from commands.inspect import inspect
from commands.list import list_command
from commands.perms import perms
from commands.rank_suggestions import fetch_suggestions
from commands.send_embed import embed_test
from commands.summon import summon
from commands.unauthorize import unauthorize
from commands.what import what
from commands.who import who
from objects.command import Command


def initialize_command_list():
    # The order of commands in the list is precedence that commands will trigger on a message that contains more than
    # one command keyword. This is important for commands that operate on other commands like authorize.
    command_list = [
        Command(
            name="who",
            documentation="""> who
>    Shows who has permission to run a command.
>    Usage:
>    @LoreBot who (command)""",
            regex=r'\bwho\b',
            method=who
        ),
        Command(
            name="list",
            documentation="""> list
>    Lists the available commands.
>    Usage:
>    @LoreBot list""",
            regex=r'\blist\b',
            method=list_command
        ),
        Command(
            name="authorize",
            documentation="""> authorize @[user|role] (command)
>    Authorizes the mentioned user or role to use the specified command. If no command is given, it authorizes the user
>    with the default level of authorization, which is applied to commands that have not had explicit permissions set.
>    Usage:
>    @LoreBot authorize @MarkSargent top
>    @LoreBot authorize @Officer""",
            regex=r'\bauthorize',
            method=authorize,
            not_authorized="You are not authorized to authorize people.",
            check_defer=True
        ),
        Command(
            name="unauthorize",
            documentation="""> unauthorize @[user|role] (command)
>    Removes authorization for the mentioned user or role for the specified command or from the default level of
>    authorization if no command was specified. This will not take away the user's authorization if that authorization
>    is granted through a role they are a member of.
>    Usage:
>    @LoreBot unauthorize @Melkhior authorize
>    @LoreBot unauthorize @Frauggs""",
            regex=r'\bunauthorize',
            method=unauthorize,
            not_authorized="You are not authorized to unauthorize people."
        ),
        Command(
            name="summon",
            documentation="""> summon @[user|role]
>    Moves the specified users or roles to your voice channel. This will not move someone out of afk.
>    Usage:
>    @LoreBot summon @Member
>    @LoreBot summon @Doragoon356""",
            regex=r'\bsummon\b',
            method=summon,
            not_authorized="Sorry, I can't summon for you."
        ),
        Command(
            name="top",
            documentation="""> top (n) #channel
>    Finds the top n posts in the mentioned text channel based on reactions from unique users. If n is not specified, 
>    it defaults to 10. This was used to vote on the guild name and tabard when we formed.
>    Usage:
>    @LoreBot top 5 #guild-name-suggestions""",
            regex=r'\btop\s*(\d+)*',
            method=fetch_suggestions,
            not_authorized="I don't answer to you!"
        ),
        Command(
            name="clear",
            documentation="""> clear #channel
>    This will delete all messages in the specified text channel.
>    Usage:
>    @LoreBot clear #general""",
            regex=r'\bclear\b',
            method=clear,
            not_authorized="You're not trusted to delete messages."
        ),
        Command(
            name="what",
            documentation="""> what
>    Shows what commands a user or role can use.
>    Usage:
>    @LoreBot what @[user|role]""",
            regex=r'\bwhat\b',
            method=what
        ),
        Command(
            name="embed",
            documentation="",
            regex=r'\bembed',
            method=embed_test,
            hidden=True,
            not_authorized="You can't do that."
        ),
        Command(
            name="inspect",
            documentation="",
            regex=r'\binspect\b',
            method=inspect,
            hidden=True,
            not_authorized="This is a debugging command and you're not authorized to use it."
        ),
        Command(
            name="perms",
            documentation="",
            regex=r'\bperms\b',
            method=perms,
            hidden=True,
            not_authorized="This is a debugging command and you're not authorized to use it."
        )
    ]
    return command_list
