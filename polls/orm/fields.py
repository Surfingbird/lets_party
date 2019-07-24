class Field:
    def __init__(self, f_type, required=True, default=None):
        self.f_type = f_type
        self.required = required
        self.default = default

    def check_type(self, value):
        if not isinstance(value,  self.f_type):
            print(self.f_type, type(value))
            raise TypeError

    def validate(self, value):
        if value is None and self.required:
            raise ValueError 

        self.check_type(value)


class IntField(Field):
    def __init__(self, required=True, default=None):
        super().__init__(int, required, default)


class StringField(Field):
    def __init__(self, required=True, default=None):
        super().__init__(str, required, default)