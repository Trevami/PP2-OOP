import pygame
from classes.DrawSubsurface import DrawSubsurface
from classes.ArrowSubsurface import ArrowSubsurface


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
            "arrow_surf": ArrowSubsurface(self.screen_surf, screen_width / 2, 0, screen_width / 2, screen_height),
            "draw_surf": DrawSubsurface(self.screen_surf, 0, 0, screen_width / 2, screen_height),
            "draw_mouse_pressed": False,
            "slider_mouse_pressed": False
        }
        self.objs.update(new_objs)

    def on_event_logic(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.app.stopApp()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if self.objs["draw_surf"].get_abs_bbox().collidepoint(mouse_pos):
                    self.objs["draw_surf"].clear_trace()
                    self.objs["draw_surf"].clear_surf = True
                    self.objs["draw_mouse_pressed"] = True

                if self.objs["arrow_surf"].arrow_slider.get_abs_bbox().collidepoint(mouse_pos):
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
                    if self.objs["arrow_surf"].shape_points:
                        self.objs["arrow_surf"].create_arrows()
                        self.objs["arrow_surf"].clear_trace()
                        self.objs["arrow_surf"].clear_surf = True
                    self.objs["arrow_surf"].arrow_slider.pressed = False
                    self.objs["slider_mouse_pressed"] = False

        state = pygame.mouse.get_pressed()
        if state[0]:
            mouse_pos = pygame.mouse.get_pos()

            if self.objs["draw_surf"].get_abs_bbox().collidepoint(mouse_pos):
                self.objs["draw_surf"].append_trace_pt(mouse_pos)

            if self.objs["arrow_surf"].arrow_slider.get_abs_bbox().collidepoint(mouse_pos):
                self.objs["arrow_surf"].arrow_slider.update_x_pos(mouse_pos[0])

    def on_loop_logic(self):
        self.objs["arrow_surf"].update_arrows()

    def on_render_logic(self):
        self.objs["arrow_surf"].draw_update()
        self.objs["draw_surf"].draw_update()
