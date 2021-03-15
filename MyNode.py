#!/usr/bin/python3
# -*- coding: utf-8 -*-

class MyNode:
    '''implementacion de clase nodo grafo'''
    def __init__(self, node_id):
        self.node_id = node_id
        self.node_coords = 0, 0

    def __str__ (self):
        return self.node_id + ", " + str(self.node_coords)

    def pass_to_integer_coords (self):
        '''pasa las coordenatas de srt a una tupla de ints'''
        return int(self.node_coords[0]), int(self.node_coords[1])

    def getID(self):
        return int(self.node_id)