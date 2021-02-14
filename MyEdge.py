#!/usr/bin/python3
# -*- coding: utf-8 -*-

class MyEdge:
    def __init__(self, edge_id, source, target):
        self.edge_id = edge_id
        self.source = source
        self.target = target
        self.data = {}
