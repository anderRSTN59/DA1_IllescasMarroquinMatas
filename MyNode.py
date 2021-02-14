#!/usr/bin/python3
# -*- coding: utf-8 -*-

class MyNode:
    def __init__(self, node_id):
        self.node_id = node_id
        self.data = {}

    def pass_to_integer_coords (self):
        '''pasa las coordenatas de srt a una tupla de int'''
        return int(float(self.data["x"])), int(float(self.data["y"]))
