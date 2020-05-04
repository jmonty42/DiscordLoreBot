class Command:

    def __init__(self, name: str, documentation: str, regex: str, method, hidden=False, not_authorized="",
                 check_defer=False):
        self.name = name
        self.documentation = documentation
        self.regex = regex
        self.method = method
        self.hidden = hidden
        self.not_authorized = not_authorized
        self.check_defer = check_defer
