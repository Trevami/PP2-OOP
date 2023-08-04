import os
import pygame


def get_image(image_name):
    path = os.path.join(
        os.path.abspath(os.getcwd()),
        "resources",
        "images",
        image_name
    )
    return pygame.image.load(path).convert_alpha()