import json

from models import ClassData, Field, Method


class ClassDataEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ClassData):
            return obj.to_dict()
        if isinstance(obj, Field):
            return {
                "name": obj.name,
                "type": obj.type,
                "null": obj.null,
                "relationship": obj.relationship,
            }
        if isinstance(obj, Method):
            return {
                "name": obj.name,
                "args": obj.args,
            }
        return super().default(obj)
