from wireframe import Wireframe

class World:
    def __init__(self):
        self.display_file = []
        self.object_builder = Wireframe()

    def builder(self):
        return self.object_builder

    def get_object(self, index):
        if len(self.display_file) > index >= 0:
            return self.display_file[index]

    def wireframe_builder(self):
        return self.object_builder

    def create_object(self):
        self.display_file.append(self.object_builder)
        del self.object_builder
        self.object_builder = Wireframe()
        return self.display_file[-1]

    def display_file(self):
        return self.display_file

    def add_example(self, example):
        self.display_file.append(example)

