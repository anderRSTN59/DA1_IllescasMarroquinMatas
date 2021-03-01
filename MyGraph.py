#!/usr/bin/python3
# -*- coding: utf-8 -*-

from xml.dom import minidom
from os import listdir
from MyNode import MyNode
from MyEdge import MyEdge

class MyGraph:
    name = ""
    node_list = ""
    edge_list = ""

    def __init__(self, name, node_list, edge_list):
        self.name = name
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

def read_xmlfile (xmlfile):
    '''lee el archivo .graphml'''
    xmldom = minidom.parse(open(xmlfile))
    graph_nodes_data = xmldom.getElementsByTagName("node")
    graph_edges_data = xmldom.getElementsByTagName("edge")
    graph_keys_data = xmldom.getElementsByTagName("key")
    graph_keys = read_keys (graph_keys_data)
    node_list = read_nodes(xmlfile, graph_keys, graph_nodes_data)
    edge_list = read_edges(xmlfile, graph_keys, graph_edges_data)

    return MyGraph (get_graph_name, node_list, edge_list)

def read_keys (graph_keys_data):
    '''lee las keys del grafo contenidas en el .graphml'''
    keys = []
    for key in graph_keys_data:
        keys.append([key.getAttribute("id"),key.getAttribute("attr.name")])
    return keys

def get_graph_name (xmldom): #revisar
    '''genera el grafo del .graphml'''
    name = ""
    graph_data = xmldom.getElementsByTagName("data")
    graph_data = graph_data[len(graph_data)-4:]
    for data in graph_data:
        if data.getAttribute("key") == "d0":
            name = data.firstChild.data
    
    return name

def read_nodes (xmldom, graph_keys, graph_nodes_data):
    '''lee los nodos del grafo y genera una lista de nodos'''
    nodes = []
    for node in graph_nodes_data:
        new_node = MyNode(node.getAttribute("id"))
        nodes.append(read_object_attr (graph_keys, new_node, node.getElementsByTagName("data")))
    return nodes

def read_edges (xmldom, graph_keys, graph_edges_data):
    '''lee las aristas del grafo y genera una lista de aristas'''
    edges = []
    for edge in graph_edges_data:
        new_edge = MyEdge(
            edge.getAttribute("id"),
            edge.getAttribute("source"),
            edge.getAttribute("target"))
        edges.append(read_object_attr (graph_keys, new_edge, edge.getElementsByTagName("data")))
    return edges

def read_object_attr (graph_keys, element, attribute_list):
    '''lee los atributos/datos de los objetos del grafo'''
    data = {}
    for attr in attribute_list:
        for key in graph_keys:
            if key[0] == attr.getAttribute("key"):
                data[key[1]] = attr.firstChild.data
    element.data = data
    return element
