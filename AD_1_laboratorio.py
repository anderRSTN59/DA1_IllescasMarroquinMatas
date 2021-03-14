#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import numpy as np
import cv2
from os import listdir
from MyGraph import MyGraph, read_xmlfile
from MyNode import MyNode
from MyEdge import MyEdge
from MyQueue import MyQueue

def create_graph_img (graph):
    '''metodo que genera la imagen del grafo'''
    ref_point, size = create_img_label_limits(graph.node_list)
    img = create_blank_label (size)
    img = draw_graph_nodes(img, graph.node_list, ref_point)
    img = draw_graph_edges(img, graph, ref_point)
    cv2.imwrite(graph.name + ".png", img, [int(cv2.IMWRITE_JPEG_QUALITY), 100])

def create_img_label_limits (node_list):
    '''busca el punto el punto mas alejado del origen'''
    max_point = find_far_point (node_list)
    min_point = find_origin_point (node_list)
    size = subs_coods (max_point, min_point, 200)
    return max_point, size

def find_far_point (node_list):
    '''busca el punto el punto mas alejado del origen'''
    x_max = 0
    y_max = 0

    for node in node_list:
        cords = node.node_coords
        if abs(cords[0]) > x_max:
            x_max = abs(cords[0])
        if abs(cords[1]) > y_max:
            y_max = abs(cords[1])

    return x_max, y_max

def find_origin_point (node_list):
    '''busca el punto de referancia sobre el que dibujar'''
    x_min = 1000
    y_min = 1000

    for node in node_list:
        cords = node.node_coords
        if abs(cords[0]) < x_min:
            x_min = abs(cords[0])
        if abs(cords[1]) < y_min:
            y_min = abs(cords[1])

    return x_min, y_min

def create_blank_label (size):
    '''crea el fondo blanco de la imagen'''
    label = np.zeros((size[1], size[0], 3), np.uint8)
    color = tuple(reversed((255, 255, 255)))
    label[:] = color
    return label

def subs_coods (coord_1, coord_2, margin):
    '''resta de dos coordenadad con correccion de margen'''
    coord_1 = abs(coord_1[0]), abs(coord_1[1])
    coord_2 = abs(coord_2[0]), abs(coord_2[1])
    subs = int(abs(coord_1[0] - coord_2[0])*50000)+margin, int(abs(coord_1[1] - coord_2[1])*50000)+margin
    return subs

def draw_graph_nodes(img, node_list, ref_point):
    '''dibuja los nodos del grafo'''
    for node in node_list:
        node_coords = node.node_coords
        center_coords = subs_coods (node_coords, ref_point, 100)
        img = cv2.circle(img, center_coords, 5, (0, 0, 255), -1)
    return img

def draw_graph_edges(img, graph, ref_point):
    '''dibuja las aristas del grafo'''
    node_list = graph.node_list
    edge_list = graph.edge_list
    for edge in edge_list:
        if len(edge.geometry) > 0:
            i = 0
            while i < (len(edge.geometry)-1):
                start_point = edge.geometry[i]
                i = i + 1
                end_point = edge.geometry[i]
                start_coord = subs_coods (start_point, ref_point, 100)
                end_coord = subs_coods (end_point, ref_point, 100)
                img = cv2.line(img, start_coord, end_coord, (0, 0, 0), 3)
        else:
            start_point = found_node_coords (edge.source, node_list)
            end_point = found_node_coords (edge.target, node_list)
            start_coord = subs_coods (start_point, ref_point, 100)
            end_coord = subs_coods (end_point, ref_point, 100)
            img = cv2.line(img, start_coord, end_coord, (0, 0, 0), 3)
    return img

def found_node_coords (node_id, node_list):
    coords = 0, 0
    for node in node_list:
        if node_id == node.node_id:
            coords = node.node_coords
    return coords

def create_txt_solution (rute):
    '''crea un .txt que contiene una linea de datos de cada grafo de un dir'''
    txt_file = open ('GraphLineList.txt','w')
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
                    print (node)
            elif opt == "-edges":
                graph = read_xmlfile(argv[-1])
                lista = MyQueue()
                lista.copy_list(graph.edge_list)
                for edge in lista.element_list:
                    print(edge)
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
