class PostDTO:
    def __init__(self, id, content):
        self.id = id
        self.content = content
    
    def asdict(self):
        return {'id': self.id, 'content': self.content}


    @staticmethod
    def from_model(post):
        return PostDTO(id = post.id, content=post.content)