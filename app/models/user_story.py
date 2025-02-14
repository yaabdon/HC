class UserStory:
    def __init__(self, title, author, content, data_creation):
        self.title = title
        self.author = author
        self.content = content
        self.data_creation = data_creation 

    def to_dict(self):
        return {
            "title": self.title,
            "content": self.content,
            "author": self.author,
            "data_creation": self.data_creation
        }