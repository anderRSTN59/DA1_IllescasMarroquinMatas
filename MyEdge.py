#!/usr/bin/python3
# -*- coding: utf-8 -*-

class MyEdge:
    '''implementacion de clase arista grafo'''
    def __init__(self, edge_id, source, target):
        self.edge_id = edge_id
        self.source = source
        self.target = target
        self.length = 0
        self.geometry = []

    def __str__ (self):
        return self.edge_id + ", " + self.source + ", " + self.target + ", " + str(self.length)
