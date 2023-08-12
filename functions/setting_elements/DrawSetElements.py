import pygame
from classes.SettingsOverlay import SettingsOverlay
from classes.Slider import Slider
from classes.Button import Button
from classes.ShapePath import ShapePath


_slider_height = 30

def _create_point_slider(settings_overlay: SettingsOverlay):
    # Sets the margin relative to the ArrowSurface
    slider_margin = settings_overlay.on_surf_item_margin
    # Sets width and height of the Slider.
    slider_width = settings_overlay.surf.get_width() - (2 * slider_margin)
    # Creates a slider.
    point_slider = Slider(
        settings_overlay.surf,
        slider_margin,
        (settings_overlay.surf.get_height() - (slider_margin + _slider_height)),
        slider_width,
        _slider_height,
        min=25,
        max=1000,
        ticks=39,
        start=400,
        text="Points",
        type="int",
        show=False
    )
    settings_overlay.objs.update({"point_slider": point_slider})

def _create_buttons(settings_overlay: SettingsOverlay):
    button_margin = settings_overlay.on_surf_item_margin
    button_space_margin = settings_overlay.on_surf_item_margin / 2
    button_width = 35
    button_height = button_width

    open_svg_button = Button(
        settings_overlay.surf,
        (button_margin + button_width + button_space_margin),
        button_margin,
        button_width,
        button_height,
        pressed=False,
        content_margin=3,
        text="SVG",
        # image=get_image("shape.png")
    )

    close_svg_button = Button(
        settings_overlay.surf,
        (settings_overlay.surf.get_width() - (button_margin + button_width)),
        button_margin,
        button_width,
        button_height,
        pressed=False,
        content_margin=3,
        font_type="Segoe UI Symbol",
        text="✕",
        color_hover=pygame.Color(250, 100, 100),
        color_hover_symbol=pygame.Color(250, 250, 250),
        show=False
    )

    shape_points_button = Button(
        settings_overlay.surf,
        button_margin,
        (button_margin + button_height + button_space_margin),
        button_width,
        button_height,
        pressed=False,
        content_margin=3,
        font_type="Segoe UI Symbol",
        text="∙",
        show=True
    )
    settings_overlay.rs_parent.show_shape_points = shape_points_button.pressed

    settings_overlay.objs.update({
        "open_svg": open_svg_button,
        "close_svg": close_svg_button,
        "shape_points": shape_points_button
    })

def _create_shape_svg_paht(settings_overlay: SettingsOverlay):
    shape_path = ShapePath(
        settings_overlay.surf,
        0, 0,
        settings_overlay.surf.get_width(),
        settings_overlay.surf.get_height(),
        num_shape_points=settings_overlay.objs["point_slider"].value
    )
    settings_overlay.objs.update({"shape_svg_paht": shape_path})

def create_draw_setting_objs(settings_overlay: SettingsOverlay):
    _create_point_slider(settings_overlay)
    _create_shape_svg_paht(settings_overlay)
    _create_buttons(settings_overlay)