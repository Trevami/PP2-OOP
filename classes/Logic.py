import pygame
from classes.DrawSubsurface import DrawSubsurface
from classes.ArrowSubsurface import ArrowSubsurface
from classes.Slider import Slider

class Logic:
    def __init__(self, app):
        self.app = app
        self.screen_surf = None
        self.objs = {}
        self.mouse_pos = None

    def get_settigs_overlay(self, surface: str):
        return self.objs[surface].settigs_overlay

    def get_setting_obj(self, surface: str, obj: str):
        return self.get_settigs_overlay(surface).objs[obj]
    
    def get_allow_obj_action(self, surface: str, obj_name: str, check_collidepoint=True):
        settigs_overlay = self.get_settigs_overlay(surface)
        obj = self.get_setting_obj(surface, obj_name)
        mouse_on_obj = obj.get_abs_bbox().collidepoint(self.mouse_pos)
        if obj_name == "settings_toggle":
            return mouse_on_obj and obj.show
        elif not check_collidepoint:
            return settigs_overlay.show and obj.show
        else:
            return mouse_on_obj and settigs_overlay.show and obj.show
        
    def set_button_active(self, surface: str, button: str):
        if self.get_allow_obj_action(surface, button):
            self.get_setting_obj(surface, button).mouse_active = True

    def toggle_button_pressed(self, surface: str, button: str):
        button_obj = self.get_setting_obj(surface, button)
        if self.get_allow_obj_action(surface, button) and button_obj.mouse_active:
            button_obj.update_toggle()
        button_obj.mouse_active = False

    def toggle_slider_pressed(self, surface: str, slider: str):
        slider_obj = self.get_setting_obj(surface, slider)
        if self.get_allow_obj_action(surface, slider):
            slider_obj.pressed = True


    def on_screen_init_logic(self):
        self.screen_surf = self.app.screen_surf
        screen_width = self.screen_surf.get_width()
        screen_height = self.screen_surf.get_height()

        self.objs.update({
            "arrow_surf": ArrowSubsurface(self.screen_surf, screen_width / 2, 0, screen_width / 2, screen_height),
            "draw_surf": DrawSubsurface(self.screen_surf, 0, 0, screen_width / 2, screen_height),
            "draw_mouse_pressed": False,
        })

    def on_event_logic(self, event):
        # Gets mouse postion.
        self.mouse_pos = pygame.mouse.get_pos()

        # Allow draw action check:
        # - Check for mouse on draw screen.
        on_draw_surf = self.objs["draw_surf"].get_abs_bbox().collidepoint(self.mouse_pos)
        allow_draw_action = on_draw_surf

        # - Check for not settings screen active.
        draw_settings_button = self.get_setting_obj("draw_surf", "settings_toggle")
        allow_draw_action = allow_draw_action and not draw_settings_button.pressed

        # - Check for mouse not on settings button.
        on_draw_settings_button = draw_settings_button.get_abs_bbox().collidepoint(self.mouse_pos)
        allow_draw_action = allow_draw_action and not on_draw_settings_button

        # - Check for not SVG shape loaded.
        svg_loaded = self.get_setting_obj("draw_surf", "shape_svg_paht").get_doc_loaded()
        allow_draw_action = allow_draw_action and not svg_loaded

        # Close on Esc key press.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.app.stop_App()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if allow_draw_action:
                    self.objs["draw_surf"].clear_trace()
                    self.objs["draw_mouse_pressed"] = True

                # Draw surface settings:
                self.set_button_active("draw_surf", "settings_toggle")
                if self.objs["draw_surf"].settigs_overlay.show:
                    # Buttons:
                    self.set_button_active("draw_surf", "open_svg")
                    self.set_button_active("draw_surf", "shape_points")
                    self.set_button_active("draw_surf", "close_svg")
                    # Slider:
                    self.toggle_slider_pressed("draw_surf", "point_slider")

                # Arrow surface settings:
                self.set_button_active("arrow_surf", "settings_toggle")
                if self.objs["arrow_surf"].settigs_overlay.show:
                    # Buttons:
                    self.set_button_active("arrow_surf", "shape_toggle")
                    self.set_button_active("arrow_surf", "shape_points")
                    self.set_button_active("arrow_surf", "circle_toggle")
                    # Sliders:
                    self.toggle_slider_pressed("arrow_surf", "speed_slider")
                    self.toggle_slider_pressed("arrow_surf", "arrow_slider")

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:

                # Draw surface logic:
                # - Draw on draw surface logic.
                if self.objs["draw_mouse_pressed"] and len(self.objs["draw_surf"].trace) >= 3:
                    # Closes Trace after mouse release
                    self.objs["draw_surf"].close_trace()

                    # Create arrows based on shape points.
                    self.objs["arrow_surf"].set_shape(self.objs["draw_surf"].trace)
                    num_arrows = self.get_setting_obj("arrow_surf", "arrow_slider").value
                    self.objs["arrow_surf"].create_arrows(num_arrows)

                    # Refreshes arrow surface
                    self.objs["arrow_surf"].clear_trace()
                    self.objs["draw_mouse_pressed"] = False
                
                # Draw surface button logic:
                # - Settings button logic.
                self.toggle_button_pressed("draw_surf", "settings_toggle")
                self.get_settigs_overlay("draw_surf").show = self.get_setting_obj("draw_surf", "settings_toggle").pressed

                # - Shape points button logic.
                self.toggle_button_pressed("draw_surf", "shape_points")
                self.objs["draw_surf"].show_shape_points = self.get_setting_obj("draw_surf", "shape_points").pressed

                # - Load SVG button logic.
                self.toggle_button_pressed("draw_surf", "open_svg")
                open_svg_button = self.get_setting_obj("draw_surf", "open_svg")
                if open_svg_button.pressed:
                    open_svg_button.update_toggle()
                    self.objs["draw_surf"].clear_trace()
                    self.objs["arrow_surf"].clear_trace()
                    self.objs["arrow_surf"].shape_points.clear()
                    self.objs["arrow_surf"].clear_arrows()
                    try:
                        # Load shape from file to trace of draw surface:
                        shape_svg_paht = self.get_setting_obj("draw_surf", "shape_svg_paht")
                        shape_svg_paht.load_shape()
                        self.objs["draw_surf"].trace = shape_svg_paht.get_shape_points()
                        self.objs["draw_surf"].close_trace()
                        # Show additional settings objects:
                        self.get_setting_obj("draw_surf", "close_svg").show = True
                        self.get_setting_obj("draw_surf", "point_slider").show = True
                        # Create arrows based on shape points:
                        self.objs["arrow_surf"].set_shape(self.objs["draw_surf"].trace)
                        num_arrows = self.get_setting_obj("arrow_surf", "arrow_slider").value
                        self.objs["arrow_surf"].create_arrows(num_arrows)
                    except FileNotFoundError as exception:
                        self.get_setting_obj("draw_surf", "close_svg").show = False
                        self.get_setting_obj("draw_surf", "point_slider").show = False
                        print(str(exception))

                # - Close SVG button logic.
                self.toggle_button_pressed("draw_surf", "close_svg")
                close_svg_button = self.get_setting_obj("draw_surf", "close_svg")
                if close_svg_button.pressed:
                    close_svg_button.update_toggle()
                    shape_svg_paht = self.get_setting_obj("draw_surf", "shape_svg_paht")
                    shape_svg_paht.close_doc()
                    self.objs["draw_surf"].clear_trace()
                    self.objs["arrow_surf"].clear_trace()
                    self.objs["arrow_surf"].shape_points.clear()
                    self.objs["arrow_surf"].clear_arrows()
                    close_svg_button.show = False
                    self.get_setting_obj("draw_surf", "point_slider").show = False

                # Draw surface slider logic:
                # - Point slider logic.
                point_slider = self.get_setting_obj("draw_surf", "point_slider")
                if point_slider.pressed and point_slider.show:
                    try:
                        shape_svg_paht = self.get_setting_obj("draw_surf", "shape_svg_paht")
                        shape_svg_paht.num_shape_points = point_slider.value
                        shape_svg_paht.generate_shape()
                        self.objs["draw_surf"].trace = shape_svg_paht.get_shape_points()
                        self.objs["draw_surf"].close_trace()
                        # Create arrows based on shape points
                        self.objs["arrow_surf"].set_shape(self.objs["draw_surf"].trace)
                        num_arrows = self.get_setting_obj("arrow_surf", "arrow_slider").value
                        self.objs["arrow_surf"].create_arrows(num_arrows)
                        # Refreshes arrow surface
                        self.objs["arrow_surf"].clear_trace()
                    except FileNotFoundError as exception:
                        self.get_setting_obj("draw_surf", "close_svg").show = False
                        point_slider.show = False
                        print(str(exception))
                    point_slider.pressed = False

                # Arrow surface button logic:
                # - Settings button logic.
                self.toggle_button_pressed("arrow_surf", "settings_toggle")
                self.objs["arrow_surf"].settigs_overlay.show = self.get_setting_obj("arrow_surf", "settings_toggle").pressed

                # - Shape button logic.
                self.toggle_button_pressed("arrow_surf", "shape_toggle")
                self.objs["arrow_surf"].shape = self.get_setting_obj("arrow_surf", "shape_toggle").pressed

                # - Shape points button logic.
                self.toggle_button_pressed("arrow_surf", "shape_points")
                self.objs["arrow_surf"].show_shape_points = self.get_setting_obj("arrow_surf", "shape_points").pressed

                # - Circle button logic.
                self.toggle_button_pressed("arrow_surf", "circle_toggle")
                self.objs["arrow_surf"].set_arrow_circles(self.get_setting_obj("arrow_surf", "circle_toggle").pressed)

                # Arrow surface slider logic:
                # - Speed slider logic.
                speed_slider = self.get_setting_obj("arrow_surf", "speed_slider")
                if speed_slider.pressed:
                    self.objs["arrow_surf"].update_arrow_speed(speed_slider.value)
                    self.objs["arrow_surf"].clear_trace()
                    speed_slider.pressed = False

                # - Arrow slider logic.
                arrow_slider = self.get_setting_obj("arrow_surf", "arrow_slider")
                if arrow_slider.pressed:
                    if self.objs["arrow_surf"].shape_points:
                        self.objs["arrow_surf"].create_arrows(arrow_slider.value)
                        self.objs["arrow_surf"].clear_trace()
                    arrow_slider.pressed = False

        # Checks if mouse is pressed.
        state = pygame.mouse.get_pressed()
        if state[0]:
            if allow_draw_action and self.objs["draw_mouse_pressed"]:
                self.objs["draw_surf"].append_trace_pt(self.mouse_pos)
            
            point_slider = self.get_setting_obj("draw_surf", "point_slider")
            if self.get_allow_obj_action("draw_surf", "point_slider", False) and point_slider.pressed:
                point_slider.update_x_pos(self.mouse_pos[0])

            speed_slider = self.get_setting_obj("arrow_surf", "speed_slider")
            if self.get_allow_obj_action("arrow_surf", "speed_slider", False) and speed_slider.pressed:
                speed_slider.update_x_pos(self.mouse_pos[0])

            arrow_slider = self.get_setting_obj("arrow_surf", "arrow_slider")
            if self.get_allow_obj_action("arrow_surf", "arrow_slider", False) and arrow_slider.pressed:
                arrow_slider.update_x_pos(self.mouse_pos[0])

    def on_loop_logic(self):
        self.objs["arrow_surf"].update_arrows()

    def on_render_logic(self):
        self.objs["arrow_surf"].draw_update()
        self.objs["draw_surf"].draw_update()
