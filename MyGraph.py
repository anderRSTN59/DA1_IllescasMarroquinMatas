#!/usr/bin/python3
# -*- coding: utf-8 -*-

#pylint: disable-msg=c0103
#pylint: disable-msg=c0114

import time
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

    def graph_data_line(self):                                                              #1
        '''población, nº nodos, nº arcos, longitud total, nº X pares, nº Y impares'''
        population = self.name.split(",")                                                   #5
        n_nodes = len(self.node_list)                                                       #4
        n_edges = len(self.edge_list)                                                       #4
        edge_total_len = 0                                                                  #2
        even_x_cosrds = 0                                                                   #2
        odd_y_cosrds = 0                                                                    #2
        for edge in self.edge_list:                                                         #bucle = n = edge_list
            #for (i = 0; i < len(edge_list); i++)                                           #6
            edge_total_len = edge_total_len + float(edge.length)                            #4
        for node in self.node_list:                                                         #bucle = m = node_list
            #for (i = 0; i < len(node_list); i++)                                           #6
            node_coords = node.pass_to_integer_coords()                                     #2
            if (node_coords[0] % 2) == 0:                                                   #3
                even_x_cosrds = even_x_cosrds + 1                                           #2
            if (node_coords[1] % 2) == 1:                                                   #3
                odd_y_cosrds = odd_y_cosrds + 1                                             #2
        return population[0], n_nodes, n_edges, edge_total_len, even_x_cosrds, odd_y_cosrds #8

def read_xmlfile (xmlfile):                                                                 #1
    '''lee el archivo .graphml'''
    xmldom = minidom.parse(open(xmlfile))                                                   #4
    node_list = read_nodes(xmldom)                                                          #4 + read_nodes()
    edge_list = read_edges(xmldom)                                                          #4 + read_edges()
    graph_name = get_graph_name(xmldom)                                                     #4 + get_graph_name()
    return MyGraph (graph_name, node_list, edge_list)                                       #4

def get_graph_name (xmldom):                                                                #1  => T(n)=20 => O(n) = k
    '''genera el grafo del .graphml'''
    name = ""                                                                               #2
    graph_data = xmldom.getElementsByTagName("data")                                        #4
    data = graph_data[len(graph_data)-4]                                                    #4
    name = data.firstChild.data                                                             #5
    return name.split(",")[0]                                                               #4

def read_nodes (xmldom):                                                                    #1
    '''lee los nodos del grafo y genera una lista de nodos'''
    graph_nodes = xmldom.getElementsByTagName("node")                                       #4
    nodes = []                                                                              #2
    for node in graph_nodes:                                                                #bucle = n = graph_nodes
        #for (i = 0; i < len(graph_nodes); i++)                                             #6
        new_node = MyNode(node.getAttribute("id"))                                          #7
        node_data = node.getElementsByTagName("data")                                       #4
        coord_x = float(node_data[1].firstChild.data)                                       #7
        coord_y = float(node_data[0].firstChild.data)                                       #7
        new_node.node_coords = coord_x, coord_y                                             #4
        nodes.append(new_node)                                                              #2
    return nodes                                                                            #1

def read_edges (xmldom):                                                                    #1
    '''lee las aristas del grafo y genera una lista de aristas'''
    graph_edges = xmldom.getElementsByTagName("edge")                                       #4
    osmid_id, length_id, geometry_id = read_edge_keys (xmldom)                              #7 + read_edge_keys ()
    edges = []                                                                              #2
    for edge in graph_edges:                                                                #bucle = n = graph_edges
        #for (i = 0; i < len(graph_edges); i++)                                             #6
        new_edge = MyEdge(                                                                  #3
            edge.getAttribute("id"),                                                        #2
            edge.getAttribute("source"),                                                    #2
            edge.getAttribute("target"))                                                    #2
        edge_attr_list = edge.getElementsByTagName("data")                                  #3
        for attr in edge_attr_list:                                                         #bucle = m = edge_attr_list
            #for (i = 0; i < len(graph_keys); i++)                                          #6
            if osmid_id == attr.getAttribute("key"):                                        #3
                new_edge.edge_id = attr.firstChild.data                                     #4
            elif length_id == attr.getAttribute("key"):                                     #3
                new_edge.length = float(attr.firstChild.data)                               #5
            elif geometry_id == attr.getAttribute("key"):                                   #3
                new_edge.geometry = get_edge_geometry(attr.firstChild.data)                 #5 + get_edge_geometry()
        edges.append(new_edge)                                                              #2
    return edges                                                                            #1

def read_edge_keys (xmldom):                                                                #1
    '''lee las keys del grafo contenidas en el .graphml'''
    graph_keys = xmldom.getElementsByTagName("key")                                         #4
    osmid_id = ""                                                                           #2
    length_id = ""                                                                          #2
    geometry_id = ""                                                                        #2
    for key in graph_keys:                                                                  #bucle = n = graph_keys
        #for (i = 0; i < len(graph_keys); i++)                                              #6
        if key.getAttribute("attr.name") == "osmid" and key.getAttribute("for") == "edge":  #7
            osmid_id = key.getAttribute("id")                                               #3
        if key.getAttribute("attr.name") == "length":                                       #3
            length_id = key.getAttribute("id")                                              #3
        if key.getAttribute("attr.name") == "geometry":                                     #3
            geometry_id = key.getAttribute("id")                                            #3
    return osmid_id, length_id, geometry_id                                                 #3

def get_edge_geometry (str_geometry):                                                       #1
    '''leer la forma de la arista'''
    section_list = str_geometry.split("(")[1].split(")")[0].split(", ")                     #10
    geometry = []                                                                           #2
    for section in section_list:                                                            #bucle = n = section_list
        #for (i = 0; i < len(section_list); i++)                                            #6
        aux = section.split(" ")                                                            #4
        section_coords = float(aux[0]), float(aux[1])                                       #6
        geometry.append(section_coords)                                                     #2
    return geometry                                                                         #1

def create_graphml (graph):
    '''crea un .graphml que contiene una grafo'''
    nodes = graph.node_list
    edges = graph.edge_list
    graphml_file = open ('Graph_Of_Roots.graphml','w')
    graphml_file.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>")
    graphml_file.write("\n<graphmlxmlns=\"http://graphml.graphdrawing.org/xmlns\"" +
                        "xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"" + 
                        "xsi:schemaLocation=\"http://graphml.graphdrawing.org/xmlns\"" +
                        " http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd>")
    graphml_file.write("\n<key attr.name=\"length\" attr.type=\"string\" for=\"edge\" id=\"d7\" />")
    graphml_file.write("\n<key attr.name=\"osmid\" attr.type=\"string\" for=\"node\" id=\"d6\" />")
    graphml_file.write("\n<key attr.name=\"osmid\" attr.type=\"string\" for=\"node\" id=\"d5\" />")
    graphml_file.write("\n<key attr.name=\"x\" attr.type=\"string\" for=\"node\" id=\"d4\" />")
    graphml_file.write("\n<key attr.name=\"y\" attr.type=\"string\" for=\"node\" id=\"d3\" />")
    graphml_file.write("\n<key attr.name=\"simplified\" attr.type=\"string\" for=\"graph\" id=\"d2\" />")
    graphml_file.write("\n<key attr.name=\"crs\" attr.type=\"string\" for=\"graph\" id=\"d1\" />")
    graphml_file.write("\n<key attr.name=\"name\" attr.type=\"string\" for=\"graph\" id=\"d0\" />")
    graphml_file.write("\n<graph edgedefault=\"directed\">")
    for node in nodes:
        graphml_file.write("\n\t<node id=" + str(node.node_id) + ">")
        graphml_file.write("\n\t\t<data key=\"d3\">" + str(node.node_coords[1]) + "</data>")
        graphml_file.write("\n\t\t<data key=\"d4\">" + str(node.node_coords[0]) + "</data>")
        graphml_file.write("\n\t\t<data key=\"d5\">" + str(node.node_id) + "</data>\n\t</node>")
    for edge in edges:
        graphml_file.write("\n\t<edge id=" + str(edge.edge_id) + 
                            " source=" + str(edge.source) +
                            " target=" +  str(edge.target) + ">")
        graphml_file.write("\n\t\t<data key=\"d6\">" + str(int(time.time())) + "</data>")
        graphml_file.write("\n\t\t<data key=\"d7\">" + str(edge.length) + "</data>\n\t</edge>")
    graphml_file.write("\n\t<data key=\"d0\">Provincia de Ciudad Real</data>")
    graphml_file.write("\n\t<data key=\"d1\">{\"init\": \"epsg:4326\"}</data>")
    graphml_file.write("\n\t<data key=\"d2\">True</data>")
    graphml_file.write("\n</graph>\n</graphml>")

    graphml_file.close()
