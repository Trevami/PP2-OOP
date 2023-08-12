import pygame
import numpy as np
import os
from svg.path import parse_path
from xml.dom import minidom
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from classes.RectSubsurface import RectSubsurface

class ShapePath(RectSubsurface):
    def __init__(self, surf: pygame.Surface, left: float, top: float, width: float, height: float, **kwargs):
        super().__init__(surf, left, top, width, height)
        defaultKwargs = {
            "on_surf_margin": 50,
            "num_shape_points": 2000,
            "show": True,
            "show_center": False
        }
        kwargs = defaultKwargs | kwargs
        self.on_surf_margin = kwargs["on_surf_margin"]
        self._doc_shape_path = None
        self.num_shape_points = kwargs["num_shape_points"]
        self.shape_points = []
        self.show = kwargs["show"]
        self.show_center = kwargs["show_center"]

    def _get_shape_br_point(self):
        x_max = max((point.real for point in self.shape_points))
        y_max = max((point.imag for point in self.shape_points))
        return x_max + y_max * 1j

    def _get_shape_tl_point(self):
        x_min = min((point.real for point in self.shape_points))
        y_min = min((point.imag for point in self.shape_points))
        return x_min + y_min * 1j

    def _get_shape_center(self):
        br_point = self._get_shape_br_point()
        tl_poin = self._get_shape_tl_point()
        return (br_point - tl_poin) / 2 + tl_poin

    def _get_shape_size(self):
        br_point = self._get_shape_br_point()
        tl_poin = self._get_shape_tl_point()
        width = br_point.real - tl_poin.real
        heigth = br_point.imag - tl_poin.imag
        return width, heigth
    
    def get_doc_loaded(self):
        if self._doc_shape_path:
            return True
        else:
            return False
        
    def get_shape_points(self):
        return [(point.real, point.imag) for point in self.shape_points]

    def _path_from_doc(self):
        Tk().withdraw()
        path = askopenfilename(
            initialdir= os.getcwd(),
            title= "Please select a SVG file:",
            filetypes=[("SVG files", ".svg")]
        )
        self._doc_shape_path = minidom.parse(path)

    def _points_from_doc(self):
        if self._doc_shape_path:
            if self.shape_points:
                self._clear_points()
            for element in self._doc_shape_path.getElementsByTagName("path"):
                path = parse_path(element.getAttribute("d"))
                self.shape_points.extend((path.point(pos) for pos in np.linspace(0, 1, self.num_shape_points, endpoint=True)))
            self._offset_shape_center(self._get_shape_center())
        else:
            self._path_from_doc()
            self._points_from_doc()

    def close_doc(self):
        # self._doc_shape_path.unlink()
        self._doc_shape_path = None
        self._clear_points()

    def _clear_points(self):
        self.shape_points.clear()

    def _offset_shape_center(self, offset: complex):
        for i in range(len(self.shape_points)):
            self.shape_points[i] -= offset

    def _transform_points(self, scale: int, offset=(0, 0)):
        shape_center = self._get_shape_center()
        self._offset_shape_center(shape_center)
        for i in range(len(self.shape_points)):
            self.shape_points[i] *= scale
            self.shape_points[i] += offset[0] + offset[1] * 1j + shape_center

    def _adjust_shape_size(self):
        # Rescales shape with aspect ratio preservation.
        shape_size = self._get_shape_size()
        shape_aspect_ratio = shape_size[0] / shape_size[1]
        # Calculates temporary new width and new height.
        temp_width = self.surf.get_width() - 2 * self.on_surf_margin
        temp_height = self.surf.get_height() - 2 * self.on_surf_margin
        scale_factor = 1
        if temp_width / shape_aspect_ratio <= temp_height:
            scale_factor = temp_width / shape_size[0]
        else:
            scale_factor = temp_height / shape_size[1]
        self._transform_points(scale_factor)

    def generate_shape(self):
        self._points_from_doc()
        surf_center = (self.surf.get_width() / 2, self.surf.get_height() / 2)
        self._transform_points(1, surf_center)
        self._adjust_shape_size()
        
    def load_shape(self):
        if self._doc_shape_path:
            self.close_doc()
        self.generate_shape()
