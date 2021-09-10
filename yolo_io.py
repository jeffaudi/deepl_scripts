#!/usr/bin/env python
# -*- coding: utf8 -*-
import sys
import os
from PIL import Image

## inspired from https://github.com/tzutalin/labelImg/blob/master/libs/yolo_io.py

TXT_EXT = '.txt'
JPG_EXT = '.jpg'
DEFAULT_ENCODING = 'utf-8'

class YOLOWriter:

    def __init__(self, folder_name):
        self.folder_name = folder_name
        self.class_list = []
        self.root_name = None
        
    def new_image(self, filename = None, img_size = None):
        # TODO: Manage exceptions
        self.box_list = []
        if filename is not None:
          im = Image.open(filename)
          self.img_size = im.size
          self.root_name = os.path.splitext(os.path.basename(filename))[0]
          im.save(os.path.join(self.folder_name, 'images', self.root_name + JPG_EXT))
        else:
          self.img_size = img_size
        
      
    def add_bnd_box(self, x_min, y_min, x_max, y_max, name):
        bnd_box = {'xmin': x_min, 'ymin': y_min, 'xmax': x_max, 'ymax': y_max}
        bnd_box['name'] = name
        self.box_list.append(bnd_box)

    def bnd_box_to_yolo_line(self, box):
        x_min = box['xmin']
        x_max = box['xmax']
        y_min = box['ymin']
        y_max = box['ymax']

        x_center = float((x_min + x_max)) / 2 / self.img_size[1]
        y_center = float((y_min + y_max)) / 2 / self.img_size[0]

        w = float((x_max - x_min)) / self.img_size[1]
        h = float((y_max - y_min)) / self.img_size[0]

        # PR387
        box_name = box['name']
        if box_name not in self.class_list:
            self.class_list.append(box_name)

        class_index = self.class_list.index(box_name)

        return class_index, x_center, y_center, w, h

    def save_labels(self, target = None):

        if target is None:
            target = os.path.join(self.folder_name, 'labels', self.root_name + TXT_EXT)

        out_file = open(target, 'w', encoding=DEFAULT_ENCODING)
        for box in self.box_list:
            class_index, x_center, y_center, w, h = self.bnd_box_to_yolo_line(box)
            # print (classIndex, x_center, y_center, w, h)
            out_file.write("%d %.6f %.6f %.6f %.6f\n" % (class_index, x_center, y_center, w, h))

        out_file.close()
        
        
    def save_classes(self, target = None):
      
        if target is None:
            target = os.path.join(os.path.dirname(os.path.abspath(self.filename)), "classes.txt")

        out_class_file = open(target, 'w', encoding=DEFAULT_ENCODING)
        for c in self.class_list:
            out_class_file.write(c+'\n')

        out_class_file.close()
