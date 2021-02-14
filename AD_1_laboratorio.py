#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from xml.dom import minidom
from os import listdir
from MyGraph import MyGraph
from MyNode import MyNode
from MyEdge import MyEdge

def create_txt_solution (rute):
    '''crea un .txt que contiene una linea de datos de cada grafo de un dir'''
    txt_file = open ('solution.txt','w')
    txt_file.write("<Población>,<n nodos>,<n arcos>,<Longitud total arcos>,<X pares>,<Y impares>")
    txt_file.write("\n")
    for element in listdir(rute):
        graph_line = read_xmlfile(rute + element).graph_data_line()
        txt_file.write(str(graph_line))
        txt_file.write("\n")
    txt_file.close()

def read_xmlfile (xmlfile):
    '''lee el archivo .graphml'''
    xmldom = minidom.parse(open(xmlfile))
    graph_keys_data = xmldom.getElementsByTagName("key")
    graph_nodes_data = xmldom.getElementsByTagName("node")
    graph_edges_data = xmldom.getElementsByTagName("edge")
    graph_data = xmldom.getElementsByTagName("data")
    graph_data = graph_data[len(graph_data)-4:]
    graph_keys = read_keys (graph_keys_data)
    node_list = read_nodes(graph_nodes_data, graph_keys)
    edge_list = read_edges(graph_edges_data, graph_keys)

    return create_graph (graph_data, node_list, edge_list)

def read_keys (graph_keys_data):
    '''lee las keys del grafo contenidas en el .graphml'''
    keys = []
    for key in graph_keys_data:
        keys.append([key.getAttribute("id"),key.getAttribute("attr.name")])
    return keys

def create_graph (graph_data, node_list, edge_list):
    '''genera el grafo del .graphml'''
    for data in graph_data:
        if data.getAttribute("key") == "d0":
            name = data.firstChild.data
        elif data.getAttribute("key") == "d1":
            crs = data.firstChild.data
        elif data.getAttribute("key") == "d2":
            simplified = data.firstChild.data
        elif data.getAttribute("key") == "d3":
            streets_per_node = data.firstChild.data
    return MyGraph(name, crs, simplified, streets_per_node, node_list, edge_list)

def read_nodes (graph_nodes_data, graph_keys):
    '''lee los nodos del grafo y genera una lista de nodos'''
    nodes = []
    for node in graph_nodes_data:
        new_node = MyNode(node.getAttribute("id"))
        nodes.append(read_object_attr (graph_keys, new_node, node.getElementsByTagName("data")))
    return nodes

def read_edges (graph_edge_data, graph_keys):
    '''lee las aristas del grafo y genera una lista de aristas'''
    edges = []
    for edge in graph_edge_data:
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

def parse_command_line (argv):
    '''controla el paso de parametros'''
    try:
        for opt in argv:
            if opt == "-h":
                print("Grupo DA-1.\nUso: python3 Manager.py",
                    "[-h] [-line inputFile] [-nodes inputFile] [-edges inputFile] [-graphs rute]")
                sys.exit()
            elif opt == "-line":
                graph = read_xmlfile(argv[-1])
                print (graph.graph_data_line())
            elif opt == "-nodes":
                graph = read_xmlfile(argv[-1])
                for node in graph.node_list:
                    print (node.node_id, node.pass_to_integer_coords())
            elif opt == "-edges":
                graph = read_xmlfile(argv[-1])
                for edge in graph.edge_list:
                    print (edge.edge_id, edge.source, edge.target)
            elif opt == "-graphs":
                create_txt_solution(argv[-1])
    except IOError:
        print("Error parsing command line options")
        sys.exit(2)

try:
    parse_command_line (sys.argv)
except KeyboardInterrupt:
    pass
