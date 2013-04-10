class MyException(Exception):
    def __init__(self, value="Error"):
        self.value = value

    def __str__(self):
        return repr(self.value)