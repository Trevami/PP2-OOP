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

        self.objs.update({
            "arrow_surf": ArrowSubsurface(self.screen_surf, screen_width / 2, 0, screen_width / 2, screen_height),
            "draw_surf": DrawSubsurface(self.screen_surf, 0, 0, screen_width / 2, screen_height),
            "draw_mouse_pressed": False,
            "slider1_mouse_pressed": False,
            "slider2_mouse_pressed": False
        })

    def on_event_logic(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.app.stop_App()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()

                if self.objs["draw_surf"].get_abs_bbox().collidepoint(mouse_pos):
                    self.objs["draw_surf"].clear_trace()
                    self.objs["draw_mouse_pressed"] = True

                settings_toggle_button = self.objs["arrow_surf"].setting_button
                if settings_toggle_button.get_abs_bbox().collidepoint(mouse_pos):
                    settings_toggle_button.update_toggle()
                    self.objs["arrow_surf"].settigs_overlay.show = settings_toggle_button.pressed

                if self.objs["arrow_surf"].settigs_overlay.show:
                    speed_slider = self.objs["arrow_surf"].settigs_overlay.speed_slider
                    if speed_slider.get_abs_bbox().collidepoint(mouse_pos):
                        speed_slider.pressed = True
                        self.objs["slider1_mouse_pressed"] = True
                    
                    arrow_slider = self.objs["arrow_surf"].settigs_overlay.arrow_slider
                    if arrow_slider.get_abs_bbox().collidepoint(mouse_pos):
                        arrow_slider.pressed = True
                        self.objs["slider2_mouse_pressed"] = True

                    shape_toggle_button = self.objs["arrow_surf"].settigs_overlay.buttons["shape_toggle"]
                    if shape_toggle_button.get_abs_bbox().collidepoint(mouse_pos):
                        shape_toggle_button.update_toggle()
                        self.objs["arrow_surf"].shape = shape_toggle_button.pressed

                    circle_toggle_button = self.objs["arrow_surf"].settigs_overlay.buttons["circle_toggle"]
                    if circle_toggle_button.get_abs_bbox().collidepoint(mouse_pos):
                        circle_toggle_button.update_toggle()
                        self.objs["arrow_surf"].set_arrow_circles(circle_toggle_button.pressed)

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self.objs["draw_mouse_pressed"] and len(self.objs["draw_surf"].trace) >= 3:
                    # Closes Trace after mouse release
                    self.objs["draw_surf"].close_trace()

                    # Create arrows based on shape points
                    self.objs["arrow_surf"].set_shape(
                        self.objs["draw_surf"].trace)
                    self.objs["arrow_surf"].create_arrows()

                    # Refreshes arrow surface
                    self.objs["arrow_surf"].clear_trace()
                    self.objs["draw_mouse_pressed"] = False

                if self.objs["slider1_mouse_pressed"]:
                    self.objs["arrow_surf"].update_arrow_speed()
                    self.objs["arrow_surf"].clear_trace()
                    self.objs["arrow_surf"].settigs_overlay.speed_slider.pressed = False
                    self.objs["slider1_mouse_pressed"] = False

                if self.objs["slider2_mouse_pressed"]:
                    if self.objs["arrow_surf"].shape_points:
                        self.objs["arrow_surf"].create_arrows()
                        self.objs["arrow_surf"].clear_trace()
                    self.objs["arrow_surf"].settigs_overlay.arrow_slider.pressed = False
                    self.objs["slider2_mouse_pressed"] = False

        state = pygame.mouse.get_pressed()
        if state[0]:
            mouse_pos = pygame.mouse.get_pos()

            if self.objs["draw_surf"].get_abs_bbox().collidepoint(mouse_pos) and self.objs["draw_mouse_pressed"]:
                self.objs["draw_surf"].append_trace_pt(mouse_pos)

            if self.objs["arrow_surf"].settigs_overlay.speed_slider.get_abs_bbox().collidepoint(mouse_pos):
                self.objs["arrow_surf"].settigs_overlay.speed_slider.update_x_pos(mouse_pos[0])

            if self.objs["arrow_surf"].settigs_overlay.arrow_slider.get_abs_bbox().collidepoint(mouse_pos):
                self.objs["arrow_surf"].settigs_overlay.arrow_slider.update_x_pos(mouse_pos[0])

    def on_loop_logic(self):
        self.objs["arrow_surf"].update_arrows()

    def on_render_logic(self):
        self.objs["arrow_surf"].draw_update()
        self.objs["draw_surf"].draw_update()
