from commands.authorize import authorize
from commands.inspect import inspect
from commands.list import list_command
from commands.rank_suggestions import fetch_suggestions
from commands.send_embed import embed_test
from commands.unauthorize import unauthorize
from objects.command import Command


def initialize_command_list():
    # The order of commands in the list is precedence that commands will trigger on a message that contains more than
    # one command keyword. This is important for commands that operate on other commands like authorize.
    command_list = [
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
            documentation="""> authorize [@user|@role] (command)
>    Authorizes the mentioned user or role to use the specified command. If no command is given, it authorizes the user
>    for with the default level of authorization, which is applied to commands that have not had explicit permissions
>    set.
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
            documentation="""> unauthorize [@user|@role] (command)
>    Removes authorization for the mentioned user or role for the specified command or from the default level of
>    authorization if no command was specified.
>    Usage:
>    @LoreBot unauthorize @Melkhior authorize
>    @LoreBot unauthorize @Frauggs""",
            regex=r'\bunauthorize',
            method=unauthorize,
            not_authorized="You are not authorized to unauthorize people."
        ),
        Command(
            name="top",
            documentation="""> top (n)
>    Finds the top n posts in the mentioned text channel based on reactions from unique users. If n is not specified, 
>    it defaults to 10. This was used to vote on the guild name and tabard when we formed.
>    Usage:
>    @LoreBot top 5 #guild-name-suggestions""",
            regex=r'\btop\s*(\d+)*',
            method=fetch_suggestions,
            not_authorized="I don't answer to you!"
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
        )
    ]
    return command_list
