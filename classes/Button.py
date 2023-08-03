import pygame
import os
from classes.RectSubsurface import RectSubsurface


class Button(RectSubsurface):
    def __init__(self, surf: pygame.Surface, left: float, top: float, width: float, height: float, **kwargs):
        super().__init__(surf, left, top, width, height)
        defaultKwargs = {
            "pressed": False,
            "color": pygame.Color(85, 85, 85),
            "color_pressed": pygame.Color(155, 155, 155),
            "image": None,
            "text": "",
            "font_type": "",
            "font_size": 24,
            "content_margin": 10
        }
        kwargs = defaultKwargs | kwargs
        self.pressed = kwargs["pressed"]
        self.color = kwargs["color"]
        self.color_pressed = kwargs["color_pressed"]
        self.image = kwargs["image"]
        self.text = kwargs["text"]
        self.font_type = kwargs["font_type"]
        self.font_size = kwargs["font_size"]
        self.content_margin = kwargs["content_margin"]
        self._adjust_image_size()
        self._update_image_color()
        self._adjust_text_size()

    def _set_image_color(self, color):
        for x_pix in range(self.image.get_width()):
            for y_pix in range(self.image.get_height()):
                color.a = self.image.get_at((x_pix, y_pix)).a  # Preserve the alpha value.
                self.image.set_at((x_pix, y_pix), color)  # Set the color of the pixel.

    def get_font(self):
        if self.font_type != "":
            return pygame.font.SysFont(self.font_type, self.font_size)
        else:
            font_name = "FantasqueSansMono-Regular.ttf"
            font_folder_name = "FantasqueSansMono"
            font_path = os.path.join(
                os.path.abspath(os.getcwd()),
                "resources",
                "fonts",
                font_folder_name,
                font_name
            )
            return pygame.font.Font(font_path, self.font_size)

    def get_font_size(self):
        # Returns the dimensions of the button text.
        return self.get_font().size(self.text)
    
    def _adjust_image_size(self):
        if self.image:
            # Rescales image with aspect ratio preservation.
            image_aspect_ratio = self.image.get_width() / self.image.get_height()
            # Calculates temporary new width and new height.
            temp_width = self.width - 2 * self.content_margin
            temp_height = self.height - 2 * self.content_margin
            # Checks if the new height calculated form temp_width fits inside the margin area.
            # If not assigns new rescale parameters according to temp_height.
            if temp_width / image_aspect_ratio <= temp_height:
                # Assigns temp_width to width and calculates new height form temp_width.
                image_new_width = temp_width
                image_new_height = temp_width / image_aspect_ratio
            else:
                # Assigns temp_height to height and calculates new width form temp_height.
                image_new_height = temp_height
                image_new_width = temp_height * image_aspect_ratio
            self.image = pygame.transform.scale(self.image, (image_new_width, image_new_height))
    
    def _adjust_text_size(self):
        if self.text:
            for size in range(self.font_size, 1, -1):
                font_size = self.get_font_size()
                surf_size = self.surf.get_size()

                width_match = font_size[0] <= (surf_size[0] - 2 * self.content_margin)
                height_match = font_size[1] <= (surf_size[1] - 2 * self.content_margin) 

                if not width_match and not height_match:
                    self.font_size = size
                else:
                    break

    def _update_image_color(self):
        if self.image:
            if self.pressed:
                self._set_image_color(self.color)
            else:
                self._set_image_color(self.color_pressed)

    def update_toggle(self):
        if self.pressed:
            self.pressed = False
            self._update_image_color()
        else:
            self.pressed = True
            self._update_image_color()

    def _draw_image(self):
        if self.image:
            button_center = (self.surf.get_width() / 2, self.surf.get_height() / 2)
            image_center = (self.image.get_width() / 2, self.image.get_height() / 2)
            delta_centers = (button_center[0] - image_center[0], button_center[1] - image_center[1])
            self.surf.blit(self.image, (delta_centers[0], delta_centers[1]))

    def _draw_text(self, color):
        if self.text:
            button_center = (self.surf.get_width() / 2, self.surf.get_height() / 2)
            text_center = (self.get_font_size()[0] / 2, self.get_font_size()[1] / 2)
            delta_centers = (button_center[0] - text_center[0], button_center[1] - text_center[1])
            # Draw text:
            text = self.get_font().render(f"{self.text}", True, color)
            self.surf.blit(text, (delta_centers[0], delta_centers[1]))

    def _draw_unpressed(self):
        self.surf.fill(self.color)
        self._draw_text(self.color_pressed)
        self._draw_image()

    def _draw_pressed(self):
        self.surf.fill(self.color_pressed)
        self._draw_text(self.color)
        self._draw_image()
    
    def draw_update(self):
        if self.pressed:
            self._draw_pressed()
        else:
            self._draw_unpressed()