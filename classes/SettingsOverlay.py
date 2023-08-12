from classes.RectSubsurface import RectSubsurface
from classes.Button import Button
from functions.images import get_image

class SettingsOverlay(RectSubsurface):
    def __init__(self, rs_parent: RectSubsurface, left: float, top: float, width: float, height: float, **kwargs):
        super().__init__(rs_parent.surf, left, top, width, height)
        defaultKwargs = {
            "show": False,
            "on_surf_item_margin": 20,
            "elements": None
        }
        kwargs = defaultKwargs | kwargs
        self.show = kwargs["show"]
        self.rs_parent = rs_parent
        self.on_surf_item_margin = kwargs["on_surf_item_margin"]
        self._slider_height = 30
        self.objs = {}
        self._create_button()

    def _create_button(self):
        button_width = 35
        button_height = button_width

        settings_toggle_button = Button(
            self.surf,
            self.on_surf_item_margin,
            self.on_surf_item_margin,
            button_width,
            button_height,
            pressed=self.show,
            content_margin=6,
            # font_type="Segoe UI Symbol",
            # text="☰",
            image=get_image("burger_menu.png")
        )
        self.objs.update({"settings_toggle": settings_toggle_button})

    def draw_update(self):
        if self.show:
            for obj in self.objs.values():
                if callable(getattr(obj, "draw_update", None)):
                    obj.draw_update()
        else:
            self.objs["settings_toggle"].draw_update()
