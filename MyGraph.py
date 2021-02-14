#!/usr/bin/python3
# -*- coding: utf-8 -*-

class MyGraph:
    streets_per_node = ""
    simplified = False
    crs = ""
    name = ""
    node_list = ""
    edge_list = ""
    def __init__(self, name, crs, simplified, streets_per_node, node_list, edge_list):
        self.name = name
        self.crs = crs
        self.simplified = simplified
        self.streets_per_node = streets_per_node
        self.node_list = node_list
        self.edge_list = edge_list

    def graph_data_line(self):
        '''<Población>,<nº nodos>,<nº arcos>,<Longitud total de los arcos>,<nº coord X pares>,<nº de coord Y impares>'''
        population = self.name.split(",")
        n_nodes = len(self.node_list)
        n_edges = len(self.edge_list)
        edge_total_len = 0
        even_x_cosrds = 0
        odd_y_cosrds = 0
        for edge in self.edge_list:
            edge_total_len = edge_total_len + float(edge.data["length"])
        for node in self.node_list:
            node_coords = node.pass_to_integer_coords()
            if (node_coords[0] % 2) == 0:
                even_x_cosrds = even_x_cosrds + 1
            if (node_coords[1] % 2) == 1:
                odd_y_cosrds = odd_y_cosrds + 1
        return population[0], n_nodes, n_edges, edge_total_len, even_x_cosrds, odd_y_cosrds
