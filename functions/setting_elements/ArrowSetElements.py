from classes.SettingsOverlay import SettingsOverlay
from classes.Slider import Slider
from classes.Button import Button
from functions.images import get_image


_slider_height = 30

def _create_arrow_slider(settings_overlay: SettingsOverlay):
    # Sets the margin relative to the ArrowSurface
    slider_margin = settings_overlay.on_surf_item_margin
    # Sets width and height of the Slider.
    slider_width = settings_overlay.surf.get_width() - (2 * slider_margin)
    # Creates a slider.
    arrow_slider = Slider(
        settings_overlay.surf,
        slider_margin,
        (settings_overlay.surf.get_height() - (slider_margin + _slider_height)),
        slider_width,
        _slider_height,
        min=2,
        max=200,
        ticks=198,
        start=40,
        text="Arrows",
        type="int"
    )
    settings_overlay.objs.update({"arrow_slider": arrow_slider})

def _create_speed_slider(settings_overlay: SettingsOverlay):
    # Sets the margin relative to the ArrowSurface
    slider_margin = settings_overlay.on_surf_item_margin
    # Sets width and height of the Slider.
    slider_width = settings_overlay.surf.get_width() - (2 * slider_margin)
    # Creates a slider.
    speed_slider = Slider(
        settings_overlay.surf,
        slider_margin,
        (settings_overlay.surf.get_height() - (slider_margin +
            slider_margin / 2 + _slider_height * 2)),
        slider_width,
        _slider_height,
        min=1,
        max=100,
        ticks=20,
        start=50,
        text="Speed ",
        type="int"
    )
    settings_overlay.rs_parent.arrow_speed = speed_slider.value
    settings_overlay.objs.update({"speed_slider": speed_slider})

def _create_buttons(settings_overlay: SettingsOverlay):
    button_margin = settings_overlay.on_surf_item_margin
    button_space_margin = settings_overlay.on_surf_item_margin / 2
    button_width = 35
    button_height = button_width

    shape_toggle_button = Button(
        settings_overlay.surf,
        button_margin,
        (button_margin + button_height + button_space_margin),
        button_width,
        button_height,
        pressed=False,
        content_margin=3,
        # text="S",
        image=get_image("shape.png")
    )
    settings_overlay.rs_parent.shape = shape_toggle_button.pressed

    shape_points_button = Button(
        settings_overlay.surf,
        button_margin,
        (button_margin + 2 * (button_height + button_space_margin)),
        button_width,
        button_height,
        pressed=False,
        content_margin=3,
        font_type="Segoe UI Symbol",
        text="∙",
        show=True
    )
    settings_overlay.rs_parent.show_shape_points = shape_points_button.pressed

    circle_toggle_button = Button(
        settings_overlay.surf,
        button_margin,
        (button_margin + 3 * (button_height + button_space_margin)),
        button_width,
        button_height,
        pressed=True,
        content_margin=3,
        # text="C",
        image=get_image("arrow_circle.png")
    )
    settings_overlay.rs_parent.set_arrow_circles(circle_toggle_button.pressed)

    settings_overlay.objs.update({
        "shape_toggle": shape_toggle_button,
        "circle_toggle": circle_toggle_button,
        "shape_points": shape_points_button
    })

def create_arrow_setting_objs(settings_overlay: SettingsOverlay):
    _create_arrow_slider(settings_overlay)
    _create_speed_slider(settings_overlay)
    _create_buttons(settings_overlay)