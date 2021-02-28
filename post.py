print("hello world!")


class Post:
    def __init__(self, id, text, upvotes, type):
        self.id = id
        self.text = text
        self.upvotes = upvotes
        self.type = type
        self.sentiment = None
        self.title = None
        self.tickers = []
        self.url = None

    def is_thread(self):
        if(self.type == "thread"):
            return True
        else:
            return False
