#!/usr/bin/python3
# -*- coding: utf-8 -*-

#pylint: disable-msg=c0103
#pylint: disable-msg=c0114
#pylint: disable-msg=e1101

import cv2
import numpy as np
from MyGraph import MyGraph

def create_graph_img (graph, scale):
    '''metodo que genera la imagen del grafo'''
    ref_point, size = create_img_label_limits(graph.node_list, scale)
    img = create_blank_label (size)
    img = draw_graph_edges(img, graph.edge_list, graph.node_list, ref_point, (0,0,0), scale)
    img = draw_graph_nodes(img, graph.node_list, ref_point, scale)
    cv2.imwrite(graph.name + ".png", img, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
    return img

def create_tree_img (graph, tree, type, scale):
    '''metodo que genera la imagen del grafo'''
    ref_point, size = create_img_label_limits(graph.node_list, scale)
    img = create_blank_label (size)
    img = draw_graph_edges(img, graph.edge_list, graph.node_list, ref_point, (0,0,0), scale)
    img = draw_graph_edges(img, tree, graph.node_list, ref_point, (0,255,0), scale)
    img = draw_graph_nodes(img, graph.node_list, ref_point, scale)
    cv2.imwrite(graph.name + type + "Tree.png", img, [int(cv2.IMWRITE_JPEG_QUALITY), 90])

def create_root_img (graph, tree, node, scale):
    '''metodo que genera la imagen del grafo'''
    ref_point, size = create_img_label_limits(graph.node_list, scale)
    img = create_blank_label (size)
    img = draw_graph_edges(img, graph.edge_list, graph.node_list, ref_point, (0,0,0), scale)
    img = draw_graph_edges(img, tree, graph.node_list, ref_point, (0,255,0), scale)
    img = draw_graph_nodes(img, graph.node_list, ref_point, scale)
    center_coords = subs_coods (node.node_coords, ref_point, 100, scale)
    img = cv2.circle(img, center_coords, 3, (255, 0, 0), -1)
    cv2.imwrite(graph.name + "_Root.png", img, [int(cv2.IMWRITE_JPEG_QUALITY), 90])

def create_img_label_limits (node_list, scale):
    '''busca el punto el punto mas alejado del origen'''
    max_point = find_far_point (node_list)
    min_point = find_origin_point (node_list)
    size = subs_coods (max_point, min_point, 200, scale)
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

def subs_coods (coord_1, coord_2, margin, scale):
    '''resta de dos coordenadad con correccion de margen'''
    coord_1 = abs(coord_1[0]), abs(coord_1[1])
    coord_2 = abs(coord_2[0]), abs(coord_2[1])
    subs_x = int(abs(coord_1[0] - coord_2[0])*scale)+margin
    subs_y = int(abs(coord_1[1] - coord_2[1])*scale)+margin
    return subs_x, subs_y

def draw_graph_nodes(img, node_list, ref_point, scale):
    '''dibuja los nodos del grafo'''
    for node in node_list:
        node_coords = node.node_coords
        center_coords = subs_coods (node_coords, ref_point, 100, scale)
        img = cv2.circle(img, center_coords, 2, (0, 0, 255), -1)
    return img

def draw_graph_edges(img, edge_list, node_list, ref_point, colour, scale):
    '''dibuja las aristas del grafo'''
    for edge in edge_list:
        if len(edge.geometry) > 0:
            i = 0
            while i < (len(edge.geometry)-1):
                start_point = edge.geometry[i]
                i = i + 1
                end_point = edge.geometry[i]
                start_coord = subs_coods (start_point, ref_point, 100, scale)
                end_coord = subs_coods (end_point, ref_point, 100, scale)
                img = cv2.line(img, start_coord, end_coord, colour, 2)
        else:
            start_point = found_node_coords (edge.source, node_list)
            end_point = found_node_coords (edge.target, node_list)
            start_coord = subs_coods (start_point, ref_point, 100, scale)
            end_coord = subs_coods (end_point, ref_point, 100, scale)
            img = cv2.line(img, start_coord, end_coord, colour, 2)
    return img

def found_node_coords (node_id, node_list):
    coords = 0, 0
    for node in node_list:
        if node_id == node.node_id:
            coords = node.node_coords
    return coords