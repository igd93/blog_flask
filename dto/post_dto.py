class PostDTO:
    def __init__(self, id, content):
        self.id = id
        self.content = content

    @staticmethod
    def from_model(post):
        return PostDTO(id = post.id, content=post.content)