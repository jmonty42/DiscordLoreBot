class Command:

    def __init__(self, name: str, documentation: str, regex: str, method, hidden=False):
        self.name = name
        self.documentation = documentation
        self.regex = regex
        self.method = method
        self.hidden = hidden
