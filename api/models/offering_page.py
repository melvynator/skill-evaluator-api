class OfferingPage:

    def __init__(self, link, date):
        self.link = link
        self.date = date

    def __str__(self):
        return str(self.date) + ": " + self.link

    def __repr__(self):
        return str(self.date) + ": " + self.link