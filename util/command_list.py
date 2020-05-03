from commands.authorize import authorize
from commands.inspect import inspect
from commands.list import list_command
from commands.rank_suggestions import fetch_suggestions
from commands.send_embed import embed_test
from commands.unauthorize import unauthorize
from objects.command import Command


def initialize_command_list():
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
            name="top",
            documentation="""> top (n)
>    Finds the top n posts in the mentioned text channel based on reactions from unique users. If n is not specified, 
>    it defaults to 10. This was used to vote on the guild name and tabard when we formed.
>    Usage:
>    @LoreBot top 5 #guild-name-suggestions""",
            regex=r'\btop\s*(\d+)*',
            method=fetch_suggestions
        ),
        Command(
            name="embed",
            documentation="",
            regex=r'\bembed',
            method=embed_test,
            hidden=True
        ),
        Command(
            name="inspect",
            documentation="",
            regex=r'\binspect\b',
            method=inspect,
            hidden=True
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
            method=authorize
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
            method=unauthorize
        )
    ]
    return command_list
