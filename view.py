import cairo
import gi
import math
import examples
import settings as default

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from world import World
from point import Point
from viewport import Viewport
from window import Window

world = World()

surface = None
viewport = Viewport()
window = Window(100, 100)
gtkBuilder = Gtk.Builder()
gtkBuilder.add_from_file('window.glade')

window_widget = gtkBuilder.get_object('main_window')
new_object_window = gtkBuilder.get_object('new_object_window')
edit_object_window = gtkBuilder.get_object('edit_object_window')
new_point_window = gtkBuilder.get_object('new_point_window')
object_combobox = gtkBuilder.get_object('idObjectCombobox')
points_combobox = gtkBuilder.get_object('idPointsCombobox')
edit_points_combobox = gtkBuilder.get_object('idEditPointsCombobox')

window_widget.connect('destroy', Gtk.main_quit)


class Handler:
    def open_object_window_cb(self, window):
        clear_point_combobox()
        clear_new_object_fields()
        new_object_window.show_all()

    def open_edit_object_window_cb(self, window):
        if get_active_object() is not None:
            name_field = gtkBuilder.get_object('idEditObjectName')
            x_field = gtkBuilder.get_object('idEditObjectX')
            y_field = gtkBuilder.get_object('idEditObjectY')
            z_field = gtkBuilder.get_object('idEditObjectZ')

            active_object = world.get_object(get_index_active_object())
            active_point = get_edit_active_point()

            name_field.set_text(active_object.get_name())
            x_field.set_text(str(active_point.x()))
            y_field.set_text(str(active_point.y()))
            z_field.set_text(str(active_point.z()))

            update_edit_points_combobox(active_object)

            edit_object_window.show_all()

    def close_object_window_cb(self, window):
        window.hide()

    def insert_point_cb(self, window):
        name_field = gtkBuilder.get_object('idObjectName')
        x_field = gtkBuilder.get_object('idObjectX')
        y_field = gtkBuilder.get_object('idObjectY')
        z_field = gtkBuilder.get_object('idObjectZ')

        x = float(x_field.get_text())
        y = float(y_field.get_text())
        z = float(z_field.get_text())

        object = world.builder()
        object.set_name(name_field.get_text())
        object.add_point(x, y, z)

        x_field.set_text("")
        y_field.set_text("")
        z_field.set_text("")

        point = Point(x, y, z)
        add_point_combobox(point)

    def on_translate_right(self, btn):
        active_object = get_active_object()
        active_object.translate(default.TRANSLATE_OFFSET, 0)
        window_widget.queue_draw()

    def on_translate_left(self, btn):
        active_object = get_active_object()
        active_object.translate(-default.TRANSLATE_OFFSET, 0)
        window_widget.queue_draw()

    def on_translate_up(self, btn):
        active_object = get_active_object()
        active_object.translate(0, -default.TRANSLATE_OFFSET)
        window_widget.queue_draw()

    def on_translate_down(self, btn):
        active_object = get_active_object()
        active_object.translate(0, default.TRANSLATE_OFFSET)
        window_widget.queue_draw()

    def on_scale_in(self, btn):
        active_object = get_active_object()
        active_object.scale(default.SCALE_IN, default.SCALE_IN)
        window_widget.queue_draw()

    def on_scale_out(self, btn):
        active_object = get_active_object()
        active_object.scale(default.SCALE_OUT, default.SCALE_OUT)
        window_widget.queue_draw()

    def on_rotate_right(self, btn):
        degree_field = gtkBuilder.get_object('idDegreeField')
        degrees = float(degree_field.get_text())

        active_object = get_active_object()
        active_object.rotate(-degrees)
        window_widget.queue_draw()

    def on_rotate_left(self, btn):
        degree_field = gtkBuilder.get_object('idDegreeField')
        degrees = float(degree_field.get_text())

        active_object = get_active_object()
        active_object.rotate(degrees)
        window_widget.queue_draw()

    def on_insert_point(self, window):
        x_field = gtkBuilder.get_object('idEditObjectX')
        y_field = gtkBuilder.get_object('idEditObjectY')
        z_field = gtkBuilder.get_object('idEditObjectZ')

        x = float(x_field.get_text())
        y = float(y_field.get_text())
        z = float(z_field.get_text())

        active_object = get_active_object()
        active_object.add_point(x, y, z)

        clear_edit_object_fields()
        add_point_edit_combobox(active_object.last_point())

    def on_edit_point(self, window):
        x_field = gtkBuilder.get_object('idEditObjectX')
        y_field = gtkBuilder.get_object('idEditObjectY')
        z_field = gtkBuilder.get_object('idEditObjectZ')

        x = float(x_field.get_text())
        y = float(y_field.get_text())
        z = float(z_field.get_text())

        active_object = get_active_object()
        index_edited_point = get_index_active_edit_point()
        active_object.set_point(index_edited_point, x, y, z)
        update_edit_points_combobox(active_object)

    def on_delete_point(self, window):
        active_object = get_active_object()
        index_deleted_point = get_index_active_edit_point()
        active_object.remove_point(index_deleted_point)
        update_edit_points_combobox(active_object)

    def create_object_cb(self, window):
        window.hide()
        if validate_creation_object():
            object = world.create_object()
            add_object_combobox(object)

    def on_points_combobox_change(self, window):
        active_object = get_active_object()
        if active_object is not None:
            active_point = get_active_point()
            if active_point is not None:
                #     update_point_combobox(active_object)
                x_field = gtkBuilder.get_object('idEditObjectX')
                y_field = gtkBuilder.get_object('idEditObjectY')
                z_field = gtkBuilder.get_object('idEditObjectZ')
                x_field.set_text(str(active_point.x()))
                y_field.set_text(str(active_point.y()))
                z_field.set_text(str(active_point.z()))

    def on_edit_points_combobox_change(self, window):
        if get_active_object() is not None:
            if get_edit_active_point() is not None:
                clear_edit_object_fields()
                set_edit_object_fields(get_active_object(), get_edit_active_point())

    def configure_event_cb(self, wid, evt):
        global surface
        if surface is not None:
            del surface
            surface = None

        win = wid.get_window()
        width = wid.get_allocated_width()
        height = wid.get_allocated_height()

        surface = win.create_similar_surface(
            cairo.CONTENT_COLOR,
            width,
            height
        )
        viewport.set_surface(surface)

        clear_surface()
        return True

    def draw_cb(self, wid, cr):
        clear_surface()
        cr.set_source_surface(surface, 0, 0)

        for object in world.display_file:
            draw(object)

        cr.paint()
        return False


def clear_new_object_fields():
    name_field = gtkBuilder.get_object('idObjectName')
    x_field = gtkBuilder.get_object('idObjectX')
    y_field = gtkBuilder.get_object('idObjectY')
    z_field = gtkBuilder.get_object('idObjectZ')

    name_field.set_text("")
    x_field.set_text("")
    y_field.set_text("")
    z_field.set_text("")


def clear_edit_object_fields():
    x_field = gtkBuilder.get_object('idEditObjectX')
    y_field = gtkBuilder.get_object('idEditObjectY')
    z_field = gtkBuilder.get_object('idEditObjectZ')

    x_field.set_text("")
    y_field.set_text("")
    z_field.set_text("")


def set_edit_object_fields(object, point):
    name_label = gtkBuilder.get_object('idEditObjectName')
    x_field = gtkBuilder.get_object('idEditObjectX')
    y_field = gtkBuilder.get_object('idEditObjectY')
    z_field = gtkBuilder.get_object('idEditObjectZ')

    name_label.set_text(object.get_name())
    x_field.set_text(str(point.x()))
    y_field.set_text(str(point.y()))
    z_field.set_text(str(point.z()))


def update_object_combobox():
    clear_object_combobox()
    for object in world.display_file():
        object_combobox.append_text(object.get_name())


def clear_object_combobox():
    while object_combobox.get_active() > -1:
        object_combobox.remove(0)


def update_point_combobox(object):
    clear_point_combobox()
    for point in object.get_points():
        points_combobox.append_text(point.to_string())
    points_combobox.set_active(0)


def clear_point_combobox():
    while points_combobox.get_active() > -1:
        points_combobox.remove(0)


def update_edit_points_combobox(object):
    clear_edit_points_combobox()
    for point in object.get_points():
        edit_points_combobox.append_text(point.to_string())
    edit_points_combobox.set_active(0)


def clear_edit_points_combobox():
    edit_points_combobox.remove_all()


def add_object_combobox(object):
    object_combobox.append_text(object.get_name())
    object_combobox.set_active(object_combobox.get_active() + 1)


def add_point_combobox(point):
    points_combobox.append_text(point.to_string())
    points_combobox.set_active(points_combobox.get_active() + 1)


def add_point_edit_combobox(point):
    edit_points_combobox.append_text(point.to_string())
    edit_points_combobox.set_active(edit_points_combobox.get_active() + 1)


def get_active_object():
    active_object = world.get_object(object_combobox.get_active())
    return active_object


def get_index_active_object():
    return object_combobox.get_active()


def get_active_point():
    active_object = get_active_object()
    active_point_index = 0
    if points_combobox.get_active() >= 0:
        active_point_index = points_combobox.get_active()

    if active_object is not None:
        active_point = get_active_object().get_point(active_point_index)
        return active_point
    return None


def get_edit_active_point():
    active_object = get_active_object()

    if active_object is not None:
        active_point = get_active_object().get_point(get_index_active_edit_point())
        return active_point
    return None


def get_index_active_edit_point():
    active_point_index = 0
    if edit_points_combobox.get_active() >= 0:
        active_point_index = edit_points_combobox.get_active()
    return active_point_index


def validate_creation_object():
    name_field = gtkBuilder.get_object('idObjectName')
    x_field = gtkBuilder.get_object('idObjectX')
    y_field = gtkBuilder.get_object('idObjectY')
    z_field = gtkBuilder.get_object('idObjectZ')

    if name_field.get_text() == "":
        return False
    if x_field == "":
        return False
    if y_field == "":
        return False
    if z_field == "":
        return False
    if points_combobox.get_active() < 0:
        return False
    return True


def draw(object):
    ctx = cairo.Context(surface)
    ctx.set_line_width(2)

    if object.object_type() == "POINT":
        point = object.first_point()
        transformed_point = viewport.transform(point.x(), point.y(), window)

        ctx.arc(transformed_point.x(), transformed_point.y(), 0.5, 0, 2 * math.pi)
    else:
        if object.object_type() == "WIREFRAME":
            for point in object.draw_points():
                print(point.to_string())
                transformed_point = viewport.transform(point.x(), point.y(), window)
                print(transformed_point.to_string())
                ctx.line_to(point.x(), point.y())

    ctx.stroke()


def clear_surface():
    global surface
    cr = cairo.Context(surface)
    cr.set_source_rgb(1, 1, 1)
    cr.paint()
    del cr


def run():
    gtkBuilder.connect_signals(Handler())
    window_widget.show_all()
    Gtk.main()


world.add_example(examples.square())
world.add_example(examples.line())
add_object_combobox(examples.square())
add_object_combobox(examples.line())
# Redraw the screen from the surface
# def draw_cb(wid, cr):
#     global surface
#     cr.set_source_surface(surface, 0, 0)
#     cr.paint()
#     return False

# class Handler:
#     # Function that will be called when the ok button is pressed
#     def btn_ok_clicked_cb(self, btn):
#         cr = cairo.Context(surface)
#         cr.move_to(200, 100)
#         cr.line_to(300, 50)
#         cr.stroke()
#         window_widget.queue_draw()


# drawing_area = gtkBuilder.get_object('drawing_area')
# drawing_area.connect('draw', draw_cb)
# drawing_area.connect('configure-event', configure_event_cb)
