import cairo
import gi
from examples import examples
import settings as default
from utils import obj_module
from objects.surface import SurfaceBezier

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from objects.point import Point
from viewport import Viewport
from window import Window

window = Window(default.WINDOW_WIDTH, default.WINDOW_HEIGHT)

surface = None
viewport = Viewport()
gtkBuilder = Gtk.Builder()
gtkBuilder.add_from_file('window.glade')

window_widget = gtkBuilder.get_object('main_window')
new_object_window = gtkBuilder.get_object('new_object_window')
edit_object_window = gtkBuilder.get_object('edit_object_window')
bezier_bicubic_surface_window = gtkBuilder.get_object('idBezierBicubicSurface')
new_curve_window = gtkBuilder.get_object('new_curve_window')
new_point_window = gtkBuilder.get_object('new_point_window')
object_combobox = gtkBuilder.get_object('idObjectCombobox')
points_combobox = gtkBuilder.get_object('idPointsCombobox')
edit_points_combobox = gtkBuilder.get_object('idEditPointsCombobox')
curve_points_combobox = gtkBuilder.get_object('idCurvePointsCombobox')
temporary_points = []

window_widget.connect('destroy', Gtk.main_quit)


class Handler:
    def open_object_window_cb(self, component):
        clear_point_combobox()
        clear_new_object_fields()
        new_object_window.show_all()

    def open_edit_object_window_cb(self, component):
        if get_active_object() is not None:
            name_field = gtkBuilder.get_object('idEditObjectName')
            x_field = gtkBuilder.get_object('idEditObjectX')
            y_field = gtkBuilder.get_object('idEditObjectY')
            z_field = gtkBuilder.get_object('idEditObjectZ')

            active_object = viewport.get_object(get_index_active_object())
            active_point = get_edit_active_point()

            name_field.set_text(active_object.get_name())
            x_field.set_text(str(active_point.x()))
            y_field.set_text(str(active_point.y()))
            z_field.set_text(str(active_point.z()))

            update_edit_points_combobox(active_object)

            edit_object_window.show_all()

    def open_curve_window_cb(self, component):
        new_curve_window.show_all()

    def on_open_window(self, window):
        window.show_all()

    def close_object_window_cb(self, component):
        component.hide()
        temporary_points.clear()

    def insert_point_cb(self, component):
        name_field = gtkBuilder.get_object('idObjectName')
        x_field = gtkBuilder.get_object('idObjectX')
        y_field = gtkBuilder.get_object('idObjectY')
        z_field = gtkBuilder.get_object('idObjectZ')

        x = float(x_field.get_text())
        y = float(y_field.get_text())
        z = float(z_field.get_text())

        object = window.builder()
        object.set_name(name_field.get_text())
        object.add_point(x, y, z)

        x_field.set_text("")
        y_field.set_text("")
        z_field.set_text("")

        point = Point(x, y, z)
        add_point_combobox(point)

    def insert_curve_point_cb(self, component):
        x_field = gtkBuilder.get_object('idCurveX')
        y_field = gtkBuilder.get_object('idCurveY')
        z_field = gtkBuilder.get_object('idCurveZ')

        x = float(x_field.get_text())
        y = float(y_field.get_text())
        z = float(z_field.get_text())

        temporary_points.append(Point(x, y, z))

        x_field.set_text("")
        y_field.set_text("")
        z_field.set_text("")

        point = Point(x, y, z)
        add_point_curve_combobox(point)

        points_counter = gtkBuilder.get_object('idCounterPoints')
        points_counter.set_text(str(len(temporary_points)) + " points")

    def on_create_bezier_bicubic_surface(self, window):
        window.hide()
        self.create_bezier_bicubic_surface()

    def create_bezier_bicubic_surface(self):
        name = gtkBuilder.get_object('idBezierBicubicSurfaceName').get_text()
        # points = []
        # for i in range(16):
        #     cellX = gtkBuilder.get_object('idBezierBicubicSurfaceCell' + str(i + 1) + 'X')
        #     cellY = gtkBuilder.get_object('idBezierBicubicSurfaceCell' + str(i + 1) + 'Y')
        #     cellZ = gtkBuilder.get_object('idBezierBicubicSurfaceCell' + str(i + 1) + 'Z')
        #     points.append(Point(float(cellX.get_text()), float(cellY.get_text()), float(cellZ.get_text())))

        object = SurfaceBezier(name, temporary_points).to_object()
        viewport.add_object(object)
        add_object_combobox(object)
        temporary_points.clear()

    def on_add_matrix_surface_bezier(self, component):
        for i in range(16):
            cellX = gtkBuilder.get_object('idBezierBicubicSurfaceCell' + str(i + 1) + 'X')
            cellY = gtkBuilder.get_object('idBezierBicubicSurfaceCell' + str(i + 1) + 'Y')
            cellZ = gtkBuilder.get_object('idBezierBicubicSurfaceCell' + str(i + 1) + 'Z')
            temporary_points.append(Point(float(cellX.get_text()), float(cellY.get_text()), float(cellZ.get_text())))

            cellX.set_text('0')
            cellY.set_text('0')
            cellZ.set_text('0')

    def on_translate_right(self, component):
        get_active_object().translate(default.TRANSLATE_OFFSET, 0, 0)
        window_widget.queue_draw()

    def on_translate_left(self, component):
        get_active_object().translate(-default.TRANSLATE_OFFSET, 0, 0)
        window_widget.queue_draw()

    def on_translate_up(self, component):
        get_active_object().translate(0, default.TRANSLATE_OFFSET, 0)
        window_widget.queue_draw()

    def on_translate_down(self, component):
        get_active_object().translate(0, -default.TRANSLATE_OFFSET, 0)
        window_widget.queue_draw()

    def on_translate_forward(self, component):
        get_active_object().translate(0, 0, default.TRANSLATE_OFFSET)
        window_widget.queue_draw()

    def on_translate_back(self, component):
        get_active_object().translate(0, 0, -default.TRANSLATE_OFFSET)
        window_widget.queue_draw()

    def on_scale_in(self, component):
        get_active_object().scale(default.SCALE_IN, default.SCALE_IN, default.SCALE_IN)
        window_widget.queue_draw()

    def on_scale_out(self, component):
        get_active_object().scale(default.SCALE_OUT, default.SCALE_OUT, default.SCALE_OUT)
        window_widget.queue_draw()

    def on_rotate_x_left(self, degree_field):
        degrees = float(degree_field.get_text())
        get_active_object().rotate_x(degrees, get_center_rotate())
        window_widget.queue_draw()

    def on_rotate_x_right(self, degree_field):
        degrees = float(degree_field.get_text())
        get_active_object().rotate_x(-degrees, get_center_rotate())
        window_widget.queue_draw()

    def on_rotate_y_left(self, degree_field):
        degrees = float(degree_field.get_text())
        get_active_object().rotate_y(degrees, get_center_rotate())
        window_widget.queue_draw()

    def on_rotate_y_right(self, degree_field):
        degrees = float(degree_field.get_text())
        get_active_object().rotate_y(-degrees, get_center_rotate())
        window_widget.queue_draw()

    def on_rotate_z_left(self, degree_field):
        degrees = float(degree_field.get_text())
        get_active_object().rotate_z(degrees, get_center_rotate())
        window_widget.queue_draw()

    def on_rotate_z_right(self, degree_field):
        degrees = float(degree_field.get_text())
        get_active_object().rotate_z(-degrees, get_center_rotate())
        window_widget.queue_draw()

    def on_panning_up(self, component):
        window.panning_up(get_step())
        window_widget.queue_draw()

    def on_panning_down(self, component):
        window.panning_down(get_step())
        window_widget.queue_draw()

    def on_panning_right(self, component):
        window.panning_right(get_step())
        window_widget.queue_draw()

    def on_panning_left(self, component):
        window.panning_left(get_step())
        window_widget.queue_draw()

    def on_panning_forward(self, component):
        window.panning_forward(get_step())
        window_widget.queue_draw()

    def on_panning_back(self, component):
        window.panning_back(get_step())
        window_widget.queue_draw()

    def on_zoom_in(self, component):
        window.zoom(get_step())
        window_widget.queue_draw()

    def on_zoom_out(self, component):
        window.zoom(-get_step())
        window_widget.queue_draw()

    def on_window_rotate_x_left(self, degree_field):
        degrees = float(degree_field.get_text())
        window.rotate_x(degrees)
        window_widget.queue_draw()

    def on_window_rotate_x_right(self, degree_field):
        degrees = float(degree_field.get_text())
        window.rotate_x(-degrees)
        window_widget.queue_draw()

    def on_window_rotate_y_left(self, degree_field):
        degrees = float(degree_field.get_text())
        window.rotate_y(degrees)
        window_widget.queue_draw()

    def on_window_rotate_y_right(self, degree_field):
        degrees = float(degree_field.get_text())
        window.rotate_y(-degrees)
        window_widget.queue_draw()

    def on_window_rotate_z_left(self, degree_field):
        degrees = float(degree_field.get_text())
        window.rotate_z(degrees)
        window_widget.queue_draw()

    def on_window_rotate_z_right(self, degree_field):
        degrees = float(degree_field.get_text())
        window.rotate_z(-degrees)
        window_widget.queue_draw()

    def on_insert_point(self, component):
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

    def on_edit_point(self, component):
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

    def on_delete_point(self, component):
        active_object = get_active_object()
        index_deleted_point = get_index_active_edit_point()
        active_object.remove_point(index_deleted_point)
        update_edit_points_combobox(active_object)

    def create_object_cb(self, component):
        component.hide()
        if validate_creation_object():
            object = window.create_object()
            viewport.add_object(object)
            add_object_combobox(object)

    def create_curve_cb(self, component):
        component.hide()
        if validate_creation_curve():
            name = gtkBuilder.get_object('idCurveName').get_text()
            object = window.create_curve(name, temporary_points, get_curve_type())
            viewport.add_object(object)
            add_object_combobox(object)

    def on_points_combobox_change(self, component):
        active_object = get_active_object()
        if active_object is not None:
            active_point = get_active_point()
            if active_point is not None:
                x_field = gtkBuilder.get_object('idEditObjectX')
                y_field = gtkBuilder.get_object('idEditObjectY')
                z_field = gtkBuilder.get_object('idEditObjectZ')
                x_field.set_text(str(active_point.x()))
                y_field.set_text(str(active_point.y()))
                z_field.set_text(str(active_point.z()))

    def on_open_file(self, component):
        file_chooser = gtkBuilder.get_object('idFileChooser')
        file_chooser.show()

    def on_choosen_file(self, chooser):
        chooser.hide()
        object = obj_module.read(chooser.get_filename())
        window.add_object(object)
        viewport.add_object(object)
        add_object_combobox(object)

    def on_open_save_chooser(self, chooser):
        chooser.show()

    def on_save_file(self, chooser):
        obj_module.write(chooser.get_filename(), get_active_object())
        chooser.hide()

    def on_edit_points_combobox_change(self, component):
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

        for object in viewport.display_file():
            draw(window.transform(object))
            # draw(object)

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
    for object in viewport.display_file():
        object_combobox.append_text(object.get_name())


def clear_object_combobox():
    while object_combobox.get_active() > -1:
        object_combobox.remove(0)


def update_point_combobox(object):
    clear_point_combobox()
    for segment in object.get_segments():
        for point in segment:
            points_combobox.append_text(point.str())
    points_combobox.set_active(0)


def clear_point_combobox():
    while points_combobox.get_active() > -1:
        points_combobox.remove(0)


def update_edit_points_combobox(object):
    clear_edit_points_combobox()
    for segment in object.get_segments():
        for point in segment:
            edit_points_combobox.append_text(point.str())

    edit_points_combobox.set_active(0)


def clear_edit_points_combobox():
    edit_points_combobox.remove_all()


def add_object_combobox(object):
    object_combobox.append_text(object.name())
    object_combobox.set_active(object_combobox.get_active() + 1)


def add_point_combobox(point):
    points_combobox.append_text(point.str())
    points_combobox.set_active(points_combobox.get_active() + 1)


def add_point_curve_combobox(point):
    curve_points_combobox.append_text(point.str())
    curve_points_combobox.set_active(curve_points_combobox.get_active() + 1)


def add_point_edit_combobox(point):
    edit_points_combobox.append_text(point.str())
    edit_points_combobox.set_active(edit_points_combobox.get_active() + 1)


def get_active_object():
    active_object = viewport.get_object(object_combobox.get_active())
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


def validate_creation_curve():
    name_field = gtkBuilder.get_object('idCurveName')
    x_field = gtkBuilder.get_object('idCurveX')
    y_field = gtkBuilder.get_object('idCurveY')
    z_field = gtkBuilder.get_object('idCurveZ')

    if name_field.get_text() == "":
        return False
    elif x_field == "":
        return False
    elif y_field == "":
        return False
    elif z_field == "":
        return False
    return True


def get_curve_type():
    radioButtonHermite = gtkBuilder.get_object('idRadioHermite')
    radioButtonBezier = gtkBuilder.get_object('idRadioBezier')
    radioButtonBSpline = gtkBuilder.get_object('idRadioBSpline')

    if radioButtonHermite.get_active():
        return "HERMITE"
    elif radioButtonBezier.get_active():
        return "BEZIER"
    else:
        return "BSPLINE"


def get_center_rotate():
    radioButtonRotationWorld = gtkBuilder.get_object('idRotationWorld')
    radioButtonRotationObject = gtkBuilder.get_object('idRotationObject')
    radioButtonRotationPoint = gtkBuilder.get_object('idRotationPoint')

    if radioButtonRotationWorld.get_active():
        return rotation_center_world()
    if radioButtonRotationObject.get_active():
        return rotation_center_object()
    if radioButtonRotationPoint.get_active():
        return rotation_center_point()
    return None


def rotation_center_world():
    return Point(0, 0, 0)


def rotation_center_object():
    active_object = get_active_object()
    return active_object.center()


def rotation_center_point():
    x_field = gtkBuilder.get_object('idRotationPointX')
    y_field = gtkBuilder.get_object('idRotationPointY')
    z_field = gtkBuilder.get_object('idRotationPointZ')

    x = float(x_field.get_text())
    y = float(y_field.get_text())
    z = float(z_field.get_text())

    return Point(x, y, z)


def get_step():
    step_field = gtkBuilder.get_object('idStepField')
    return float(step_field.get_text())


def draw(object):
    ctx = cairo.Context(surface)
    ctx.set_line_width(1)
    ctx.set_source_rgba(1, 1, 1, 0.3)

    for wireframe in object.wireframes():
        for line in wireframe.lines():
            p1 = viewport.transform(line.p1().x(), line.p1().y(), window)
            p2 = viewport.transform(line.p2().x(), line.p2().y(), window)

            ctx.move_to(p1.x(), p1.y())
            ctx.line_to(p2.x(), p2.y())
            ctx.stroke()

        ctx.new_path()

def init_examples():
    # hermite = examples.curve_hermite()
    # bezier = examples.curve_bezier()
    bezier_surface = examples.bezier_surface()
    # bspline_surface = examples.bspline_surface()
    # bspline_surace_25pts = examples.bspline_surface_25pts()
    # window.add_object(hermite)
    window.add_object(bezier_surface)
    # window.add_object(bspline_surface)
    # window.add_object(bspline_surace_25pts)
    # window.add_object(bezier)
    # viewport.add_object(hermite)
    viewport.add_object(bezier_surface)
    # viewport.add_object(bspline_surface)
    # viewport.add_object(bspline_surace_25pts)
    # viewport.add_object(bezier)
    # add_object_combobox(hermite)
    add_object_combobox(bezier_surface)
    # add_object_combobox(bspline_surface)
    # add_object_combobox(bspline_surace_25pts)
    # add_object_combobox(bezier)

def clear_surface():
    global surface
    cr = cairo.Context(surface)
    cr.paint()
    del cr


def run():
    gtkBuilder.connect_signals(Handler())
    window_widget.show_all()
    Gtk.main()

init_examples()