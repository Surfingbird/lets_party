class QuerySet:
    def __init__(self, selector):
        self.selector = selector
        print(self.selector)

    def filter(self, **selector):
        self.selector = {**self.selector, **selector}
        print(self.selector)

    def __getitem__(self, key):
        print(type(key), key)