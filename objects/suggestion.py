class Suggestion:
    def __init__(self, votes, name, url="", author=None):
        self.votes = votes
        self.name = name
        self.url = url
        self.author = author

    def __str__(self):
        return self.name + ": " + str(self.votes) + " votes " + self.url + " by " + str(self.author)
