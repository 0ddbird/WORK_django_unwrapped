class ClassData:
    def __init__(self, name, fields, methods):
        self.name = name
        self.fields = fields
        self.methods = methods

    def __repr__(self):
        return f"{self.name}, {self.fields}, {self.methods}"

    def __str__(self):
        return f"{self.name}, {self.fields}, {self.methods}"

    def to_dict(self):
        return {
            "name": self.name,
            "fields": self.fields,
            "methods": self.methods,
        }


class Field:
    def __init__(self, name, type_, null, relationship):
        self.name = name
        self.type = type_
        self.null = null
        self.relationship = relationship

    def __repr__(self):
        return f"{self.name}({self.type})"

    def __str__(self):
        return f"{self.name}({self.type})"


class Method:
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def __repr__(self):
        return f"{self.name}({self.args})"
