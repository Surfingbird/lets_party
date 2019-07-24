class Field:
    def __init__(self, f_type, required=True, default=None):
        self.f_type = f_type
        self.required = required
        self.value = default

    def validate(self):
        if self.value is None and self.required:
            raise ValueError 

        if not isinstance(self.value,  self.f_type):
            raise TypeError

    def get(self):
        return self.value

    def set_val(self, value):
        self.value = value


class IntField(Field):
    def __init__(self, required=True, default=None):
        super().__init__(int, required, default)


class StringField(Field):
    def __init__(self, required=True, default=None):
        super().__init__(str, required, default)