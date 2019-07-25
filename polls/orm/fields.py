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

class BoolField(Field):
    def __init__(self, required=True, default=False):
        super().__init__(bool, required, default)


class InnerObject:
    def __init__(self, f_type):
        self.f_type = f_type 

        for key, value in self.__class__.__dict__.items():
            if issubclass(type(value), Field) or issubclass(type(value), InnerObject):
                self.__dict__[key] = value  

        # for key, value in kwargs.items():
        #     self.__class__.__dict__[key].validate(value)
        #     self.__dict__[key] = value

        # for key, value in self.__dict__.items():
        #     self.__dict__[key].validate(value)

    # def check_type(self, value):
    #     if not isinstance(value, self.__class__):
    #         raise TypeError 

    # def validate(self, value):
    #     self.check_type(value)

    #     for key, value in value.__dict__.items():
    #         self.__dict__[key].validate(value)


#     def __str__(self):
#         return str(self.__dict__)


class Wish(InnerObject):
    reserved = BoolField(required=True, default=False)
    sponsor_id = StringField(required=False, default='')
    product_id = StringField(required=True, default='')

    def __init__(self):
        super().__init__(self.__class__)


class Intention(InnerObject):
    product_id = StringField(required=True, default='')
    dest_id = StringField(required=False, default='')

    def __init__(self):
        super().__init__(self.__class__)
    

class ListField():
    item_type = None
    
    def __init__(self):
        self.default = []

    def check_type(self, value):
        if not isinstance(value,  list):
            raise TypeError

    def validate(self, value):
        self.check_type(value)

        for item in value:
            self.f_type.validate(item)


class WishListField(ListField):
    item_type = Wish()

class IntentionListField(ListField):
    item_type = Intention()