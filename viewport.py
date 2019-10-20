from point import Point


class Viewport:
    def __init__(self):
        self.__x_min = 0
        self.__y_min = 0
        self.__x_max = 0
        self.__y_max = 0
        self.__display_file = []

    def set_surface(self, surface):
        self.__x_max = surface.get_width()
        self.__y_max = surface.get_height()

    def transform(self, x, y, window):
        transformed_x = (x - window.x_min()) / (window.x_max() - window.y_min()) * (self.__x_max - self.__x_min)
        transformed_y = (1 - (y - window.y_min()) / (window.y_max() - window.y_min())) * (self.__y_max - self.__y_min)

        return Point(transformed_x, transformed_y, 1)

    def get_object(self, index):
        if len(self.__display_file) > index >= 0:
            return self.__display_file[index]

    def add_object(self, object):
        self.__display_file.append(object)

    def display_file(self):
        return self.__display_file
