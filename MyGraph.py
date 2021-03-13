#!/usr/bin/python3
# -*- coding: utf-8 -*-

from xml.dom import minidom
#import networkx as nx
#import matplotlib.pyplot as plt
from MyNode import MyNode
from MyEdge import MyEdge

class MyGraph:
    '''implementacion de clase grafo'''
    name = ""
    node_list = ""
    edge_list = ""

    def __init__(self, name, node_list, edge_list):
        self.name = name
        self.node_list = node_list
        self.edge_list = edge_list

    def graph_data_line(self):
        '''población, nº nodos, nº arcos, longitud total, nº X pares, nº Y impares'''
        population = self.name.split(",")
        n_nodes = len(self.node_list)
        n_edges = len(self.edge_list)
        edge_total_len = 0
        even_x_cosrds = 0
        odd_y_cosrds = 0
        for edge in self.edge_list:
            edge_total_len = edge_total_len + float(edge.length)
        for node in self.node_list:
            node_coords = node.pass_to_integer_coords()
            if (node_coords[0] % 2) == 0:
                even_x_cosrds = even_x_cosrds + 1
            if (node_coords[1] % 2) == 1:
                odd_y_cosrds = odd_y_cosrds + 1
        return population[0], n_nodes, n_edges, edge_total_len, even_x_cosrds, odd_y_cosrds

def read_xmlfile (xmlfile):
    '''lee el archivo .graphml'''
    xmldom = minidom.parse(open(xmlfile))
    node_list = read_nodes(xmldom)
    edge_list = read_edges(xmldom)
    graph_name = get_graph_name(xmldom)
    return MyGraph (graph_name, node_list, edge_list)

def get_graph_name (xmldom): #revisar
    '''genera el grafo del .graphml'''
    name = ""
    graph_data = xmldom.getElementsByTagName("data")
    data = graph_data[len(graph_data)-4]
    name = data.firstChild.data
    return name.split(",")[0]

def read_nodes (xmldom):
    '''lee los nodos del grafo y genera una lista de nodos'''
    graph_nodes = xmldom.getElementsByTagName("node")
    nodes = []
    for node in graph_nodes:
        new_node = MyNode(node.getAttribute("id"))
        node_data = node.getElementsByTagName("data")
        coord_x = float(node_data[1].firstChild.data)
        coord_y = float(node_data[0].firstChild.data)
        new_node.node_coords = coord_x, coord_y
        nodes.append(new_node)
    return nodes

def read_edges (xmldom):
    '''lee las aristas del grafo y genera una lista de aristas'''
    graph_edges = xmldom.getElementsByTagName("edge")
    length_id, geometry_id = read_edge_keys (xmldom)
    edges = []
    for edge in graph_edges:
        new_edge = MyEdge(
            edge.getAttribute("id"),
            edge.getAttribute("source"),
            edge.getAttribute("target"))
        edge_attr_list = edge.getElementsByTagName("data")
        for attr in edge_attr_list:
            if length_id == attr.getAttribute("key"):
                new_edge.length = float(attr.firstChild.data)
            elif geometry_id == attr.getAttribute("key"):
                new_edge.geometry = get_edge_geometry(attr.firstChild.data)
        edges.append(new_edge)
    return edges

def read_edge_keys (xmldom):
    '''lee las keys del grafo contenidas en el .graphml'''
    graph_keys = xmldom.getElementsByTagName("key")
    length_id = ""
    geometry_id = ""
    for key in graph_keys:
        if key.getAttribute("attr.name") == "length":
            length_id = key.getAttribute("id")
        if key.getAttribute("attr.name") == "geometry":
            geometry_id = key.getAttribute("id")
    return length_id, geometry_id

def get_edge_geometry (str_geometry):
    '''leer la forma de la arista'''
    section_list = str_geometry.split("(")[1].split(")")[0].split(", ")
    geometry = []
    for section in section_list:
        aux = section.split(" ")
        section_coords = float(aux[0]), float(aux[1])
        geometry.append(section_coords)
    return geometry
