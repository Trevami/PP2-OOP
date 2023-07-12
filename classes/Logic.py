import pygame
from classes.DrawSurface import DrawSurface
from classes.ArrowSurface import ArrowSurface


class Logic:
    def __init__(self, app):
        self.app = app
        self.screen_surf = None
        self.objs = {}

    def on_screen_init_logic(self):
        self.screen_surf = self.app.screen_surf

        screen_width = self.screen_surf.get_width()
        screen_height = self.screen_surf.get_height()
        new_objs = {
            "arrow_surf": ArrowSurface((screen_width / 2, screen_height)),
            "arrow_surf_x_pos": self.screen_surf.get_width() / 2,
            "draw_surf": DrawSurface((screen_width / 2, screen_height)),
            "draw_mouse_pressed": False,
            "slider_mouse_pressed": False
        }
        self.objs.update(new_objs)

        # Abs boundingbox calculations for arrow slider.
        # Found out too late about pygame.Surface.subsurface => quick fix
        arrow_slider = self.objs["arrow_surf"].arrow_slider
        arrow_slider_x = self.objs["arrow_surf_x_pos"] + \
            arrow_slider.surf.get_abs_offset()[0]
        arrow_slider_y = arrow_slider.surf.get_abs_offset()[1]
        bbox_arrow_slider = arrow_slider.surf.get_rect()
        bbox_arrow_slider = bbox_arrow_slider.move(
            arrow_slider_x, arrow_slider_y)
        self.objs.update({"arrow_slider_bbox": bbox_arrow_slider})

    def on_event_logic(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.app.stopApp()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                bbox_draw_surf = self.objs["draw_surf"].get_rect()
                if bbox_draw_surf.collidepoint(mouse_pos):
                    self.objs["draw_surf"].clear_trace()
                    self.objs["draw_surf"].clear_surf = True
                    self.objs["draw_mouse_pressed"] = True

                if self.objs["arrow_slider_bbox"].collidepoint(mouse_pos):
                    self.objs["arrow_surf"].arrow_slider.pressed = True
                    self.objs["slider_mouse_pressed"] = True

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self.objs["draw_mouse_pressed"]:

                    # Closes Trace after mouse release
                    self.objs["draw_surf"].close_trace()

                    # Create arrows based on shape points
                    self.objs["arrow_surf"].set_shape(
                        self.objs["draw_surf"].trace)
                    self.objs["arrow_surf"].create_arrows()

                    # Refreshes arrow surface
                    self.objs["arrow_surf"].clear_trace()
                    self.objs["arrow_surf"].clear_surf = True
                    self.objs["draw_mouse_pressed"] = False

                if self.objs["slider_mouse_pressed"]:
                    self.objs["arrow_surf"].arrow_slider.pressed = False
                    if self.objs["arrow_surf"].shape_points:
                        self.objs["arrow_surf"].create_arrows()
                        self.objs["arrow_surf"].clear_trace()
                        self.objs["arrow_surf"].clear_surf = True
                    self.objs["slider_mouse_pressed"] = False

        state = pygame.mouse.get_pressed()
        if state[0]:
            mouse_pos = pygame.mouse.get_pos()

            bbox_draw_surf = self.objs["draw_surf"].get_rect()
            if bbox_draw_surf.collidepoint(mouse_pos):
                self.objs["draw_surf"].append_trace_pt(mouse_pos)

            if self.objs["arrow_slider_bbox"].collidepoint(mouse_pos):
                mouse_pos_x = mouse_pos[0] - self.objs["arrow_surf_x_pos"]
                self.objs["arrow_surf"].arrow_slider.update_x_pos(mouse_pos_x)

    def on_loop_logic(self):
        self.objs["arrow_surf"].update_arrows()

    def on_render_logic(self):
        self.objs["arrow_surf"].draw_update()
        self.objs["draw_surf"].draw_update()

        self.screen_surf.blit(self.objs["draw_surf"], (0, 0))
        self.screen_surf.blit(
            self.objs["arrow_surf"], (self.objs["arrow_surf_x_pos"], 0))
