import pygame
from classes.Logic import Logic


class App:
    def __init__(self, display_name: str):
        self._running = True
        self.screen_surf = None
        self._screen_surf_name = display_name
        self.size = self.width, self.height = 1500, 750
        self._clock = None
        self.fps = 60
        self._logic = Logic(self)

    def _init_screen_surf(self):
        # Calls pygame.init() that initialize all PyGame modules.
        # At the end this routine sets _running to True.
        pygame.init()
        # Creates main display window and tries to use hardware acceleration.
        self.screen_surf = pygame.display.set_mode(
            self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        # Creates clock for framerate handling.
        self._clock = pygame.time.Clock()
        # Sets window name.
        pygame.display.set_caption(self._screen_surf_name)
        # Executes init logic:
        self._logic.on_screen_init_logic()
        self._running = True

    def stop_App(self):
        self._running = False

    def _on_event(self, event: pygame.event):
        # Checks if Quit event happened. If so, sets _running to False which will break game loop.
        if event.type == pygame.QUIT:
            self.stop_App()
        # Executes event logic:
        self._logic.on_event_logic(event)

    def _on_loop(self):
        # Executes loop logic:
        self._logic.on_loop_logic()

    def _on_render(self):
        # Executes render logic:
        self._logic.on_render_logic()
        # Updates the full display Surface to screen:
        pygame.display.update()

    def _on_cleanup(self):
        # Calls pygame.quit() that quits all PyGame modules. Anything else will be cleaned up by Python:
        pygame.quit()

    def run(self):
        # Initializes PyGame and then enters main loop.
        # Will run until quit event.
        # Before quitting a cleanup will occur.

        self._init_screen_surf()

        while (self._running):
            self._clock.tick(self.fps)
            events = pygame.event.get()
            for event in events:
                self._on_event(event)
            self._on_loop()
            self._on_render()
        self._on_cleanup()
