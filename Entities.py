class Event:
    
    def __init__(self, title, description, date, time):
        self.title = title
        self.description = description
        self.date = date
        self.time = time

class Day:
        
    def __init__(self, day, events):
        self.day = day
        self.events = events