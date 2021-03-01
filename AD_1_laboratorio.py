#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import cv2
from xml.dom import minidom
from os import listdir
from MyGraph import MyGraph, read_xmlfile
from MyNode import MyNode
from MyEdge import MyEdge

def create_graph_img (graph):
    max_point, min_point, size = create_img_label_limits(graph.node_list)
    img = create_blank_label (size)
    img = draw_graph_nodes(img, graph.node_list, max_point)
    img = draw_graph_edges(img, graph.edge_list, max_point)
    cv2.imwrite("graph.png", img, [int(cv2.IMWRITE_JPEG_QUALITY), 90])

def create_img_label_limits (node_list):
    max_point = find_far_point (node_list)
    min_point = find_origin_point (node_list)
    size = subs_coods (max_point, min_point, 200)
    return max_point, min_point, size

def find_far_point (node_list):
    x_max = 0
    y_max = 0

    for n in node_list:
        cords = n.get_node_coords()
        if abs(cords[0]) > x_max: x_max = abs(cords[0])
        if abs(cords[1]) > y_max: y_max = abs(cords[1])

    return x_max, y_max

def find_origin_point (node_list):
    x_min = 1000
    y_min = 1000

    for n in node_list:
        cords = n.get_node_coords()
        if abs(cords[0]) < x_min: x_min = abs(cords[0])
        if abs(cords[1]) < y_min: y_min = abs(cords[1])

    return x_min, y_min

def create_blank_label (size):
    label = np.zeros((size[1], size[0], 3), np.uint8)
    color = tuple(reversed((255, 255, 255)))
    label[:] = color
    return label

def subs_coods (coord_1, coord_2, margin):
    coord_1 = abs(coord_1[0]), abs(coord_1[1])
    coord_2 = abs(coord_2[0]), abs(coord_2[1])
    subs = int(abs(coord_1[0] - coord_2[0])*100000)+margin, int(abs(coord_1[1] - coord_2[1])*100000)+margin
    return subs

def draw_graph_nodes(img, node_list, max_point):
    for n in node_list:
        node_coords = n.get_node_coords()
        center_coords = subs_coods (node_coords, max_point, 100)
        img = cv2.circle(img, center_coords, 10, (0, 0, 255), -1)
    return img

def draw_graph_edges(img, edge_list, max_point):
    for e in edge_list:
        if "geometry" in e.data:
            edge_geometry = e.get_edge_geometry()
            i = 0
            while i < (len(edge_geometry)-1):
                start_point = edge_geometry[i]
                i = i + 1
                end_point = edge_geometry[i]
                start_coord = subs_coods (start_point, max_point, 100)
                end_coord = subs_coods (end_point, max_point, 100)
                img = cv2.line(img, start_coord, end_coord, (0, 0, 0), 5) 
    return img

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

def parse_command_line (argv):
    '''controla el paso de parametros'''
    try:
        for opt in argv:
            if opt == "-h":
                print("Grupo DA-1.\nUso: python3 Manager.py",
                    "[-h] [-line inputFile] [-draw inputFile] [-nodes inputFile] [-edges inputFile] [-graphs inputFile]")
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
            elif opt == "-draw":
                graph = read_xmlfile(argv[-1])
                create_graph_img (graph)

    except IOError:
        print("Error parsing command line options")
        sys.exit(2)

try:
    parse_command_line (sys.argv)
except KeyboardInterrupt:
    pass
