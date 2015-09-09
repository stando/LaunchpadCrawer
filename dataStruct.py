__author__ = 'Shawn'

class Project:
    name = None

    def __init__(self, name="undefined"):
        self.name = name

    def list_attributes(self):
        print self.__dict__.keys()

class Bug:
    title = None

    def __init__(self, title="undefined"):
        self.title = title

    def list_attributes(self):
        print self.__dict__.keys()


class Blueprint:
    name = None

    def __init__(self, name="undefined"):
        self.name = name

    def list_attributes(self):
        print self.__dict__.keys()
