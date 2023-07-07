from json import JSONEncoder
from dto.post_dto import PostDTO

class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, PostDTO):
            return obj.asdict()
        return super().default(obj)