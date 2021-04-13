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
base = dict()

def create_graph_img (graph):
    '''metodo que genera la imagen del grafo'''
    ref_point, size = create_img_label_limits(graph.node_list)
    img = create_blank_label (size)
    img = draw_graph_nodes(img, graph.node_list, ref_point)
    img = draw_graph_edges(img, graph, ref_point)
    cv2.imwrite(graph.name + ".png", img, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
    return img, ref_point

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

def iniciarKruskal (rute):
    for element in listdir(rute):
        
        graph = read_xmlfile(rute + element)
        
        kruskal(graph)

'''Metodo recursivo que devuelve la cabeza del grupo conexo'''
def findParentKruskal(nodeIDstr):
    if base[nodeIDstr] == nodeIDstr :
        return nodeIDstr
    return findParentKruskal(base[nodeIDstr])

def kruskal (graph):    
    
    ARC= []
    base.clear()

    listaAristas = MyQueue()
    listaAristas.copy_list(graph.edge_list)
    listaAristas.element_list.reverse()
    
    '''Inicia el diccionario, indicando que la cabeza de cada grupo conexo es el mismo nodo en si '''
    for i in range(0, len(graph.node_list)):        
        base[str(graph.node_list[i].node_id)] = graph.node_list[i].node_id
    
    '''itera mientras queden aristas sin comprobar'''
    while len(listaAristas.element_list) > 0:

        edge = listaAristas.element_list.pop()
        
        nSource = findParentKruskal(str(edge.source))
        nTarget = findParentKruskal(str(edge.target))
        if nSource != nTarget:
            base[nTarget] = nSource
            
            ARC.append(edge)

    print (graph.name, " ", len(ARC), " ", len(graph.node_list))
    img, ref_point = create_graph_img (graph)
    img = draw_tree (img, graph, ref_point, ARC)
    cv2.imwrite(graph.name + "_Kruskal.png", img, [int(cv2.IMWRITE_JPEG_QUALITY), 100])

    for element in ARC:
        print(element)
    print("-------------------------------------------------------")
    print("                          FIN")

def draw_tree (img, graph, ref_point, ARC):
    '''dibuja las aristas del grafo'''
    node_list = graph.node_list
    edge_list = ARC
    for edge in edge_list:
        if len(edge.geometry) > 0:
            i = 0
            while i < (len(edge.geometry)-1):
                start_point = edge.geometry[i]
                i = i + 1
                end_point = edge.geometry[i]
                start_coord = subs_coods (start_point, ref_point, 100)
                end_coord = subs_coods (end_point, ref_point, 100)
                img = cv2.line(img, start_coord, end_coord, (0, 255, 0), 3)
        else:
            start_point = found_node_coords (edge.source, node_list)
            end_point = found_node_coords (edge.target, node_list)
            start_coord = subs_coods (start_point, ref_point, 100)
            end_coord = subs_coods (end_point, ref_point, 100)
            img = cv2.line(img, start_coord, end_coord, (0, 255, 0), 3)
    return img

'''
def kruskal_algorithm (graph):
    solution = []
    connected_components = create_connected_components(graph.node_list)
    edge_list = MyQueue()
    edge_list.copy_list(graph.edge_list)
    solution.append(edge_list.element_list[0])
    update_connected_components(connected_components, solution[0].source, solution[0].target)
    i = 1
    while len(connected_components) > 1:
        edge = edge_list.element_list[i]
        edge_source = edge.source
        edge_target = edge.target
        if not detect_void(connected_components, edge_source, edge_target):
            solution.append(edge)
            update_connected_components (connected_components, edge_source, edge_target)
        i = i + 1
    return solution

def update_connected_components (connected_components, node_source, node_target):
    source = []
    target = []
    i = 0
    while i < len(connected_components) or len(source) < 0:
        for element in connected_components[i]:
            if node_source == element:
                source = connected_components.pop(i)
        i = i + 1
    i = 0
    while i < len(connected_components) or len(target) < 0:
        for element in connected_components[i]:
            if node_target == element:
                target = connected_components.pop(i)
        i = i + 1
    for element in target:
        source.append(element)
    connected_components.append(source)
    return connected_components

def create_connected_components (node_list):
    components = []
    for node in node_list:
        components.append([node.node_id])
    return components

def detect_void (connected_components, source, target):
    for component in connected_components:
        first = False
        second = False
        for element in component:
            if element == source:
                first = True
            if element == target:
                second = True
            if first == True and second == True:
                return True
    return False

def search_in_component (connected_components, actual_node):
    for component in connected_components:
        for node in component:
            if node == actual_node:
                return True
            else:
                return False
'''

def prim_algorithm (graph):
    visited_nodes = []
    solution = []
    fringe = MyQueue()
    total_nodes = len(graph.node_list)
    edge_list = graph.edge_list
    solution.append(find_short_edge (edge_list))

    edge_source = solution[0].source
    edge_target = solution[0].target
    visited_nodes.append(edge_source)
    visited_nodes.append(edge_target)
    fringe = update_fringe (fringe, get_node_edges (edge_list, edge_source))
    fringe = update_fringe (fringe, get_node_edges (edge_list, edge_target))

    while len(visited_nodes) < total_nodes:
        edge = fringe.element_list.pop(0)
        edge_source = edge.source
        edge_target = edge.target
        if edge_source not in visited_nodes or edge_target not in visited_nodes:
            solution.append(edge)
            if edge_source not in visited_nodes:
                visited_nodes.append(edge_source)
                fringe = update_fringe (fringe, get_node_edges (edge_list, edge_source))
            if edge_target not in visited_nodes:
                visited_nodes.append(edge_target)
                fringe = update_fringe (fringe, get_node_edges (edge_list, edge_target))

    return solution

def update_fringe (fringe, edges):
    for edge in edges:
        fringe.add_element(edge)
    return fringe

def get_node_edges (edge_list, node_id):
    edges = []
    for edge in edge_list:
        if edge.source == node_id or edge.target == node_id:
            edges.append(edge)
    return edges

def find_short_edge (edge_list):
    short = edge_list[0]
    for edge in edge_list:
        if edge.length < short.length:
            short = edge
    return short

def draw_tree(img, ref_point, edge_tree, node_list, graph_name):
    j = 0
    while j < len(edge_tree):
        edge = edge_tree[j]
        if len(edge.geometry) > 0:
            i = 0
            while i < (len(edge.geometry)-1):
                start_point = edge.geometry[i]
                i = i + 1
                end_point = edge.geometry[i]
                start_coord = subs_coods (start_point, ref_point, 100)
                end_coord = subs_coods (end_point, ref_point, 100)
                img = cv2.line(img, start_coord, end_coord, (0, 255, 0), 2)
        else:
            start_point = found_node_coords (edge.source, node_list)
            end_point = found_node_coords (edge.target, node_list)
            start_coord = subs_coods (start_point, ref_point, 100)
            end_coord = subs_coods (end_point, ref_point, 100)
            img = cv2.line(img, start_coord, end_coord, (0, 255, 0), 2)
        j = j + 1
    return img

def create_both_trees (graph):
    img, ref_point = create_graph_img (graph)
    edge_tree = kruskal_algorithm (graph)
    img_1 = draw_tree(img, ref_point, edge_tree, graph.node_list, graph.name)
    cv2.imwrite(graph.name + "_Kruskal_Tree.png", img_1, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
    edge_tree = prim_algorithm (graph)
    img_2 = draw_tree(img, ref_point, edge_tree, graph.node_list, graph.name)
    cv2.imwrite(graph.name + "_Prim_Tree.png", img_2, [int(cv2.IMWRITE_JPEG_QUALITY), 90])

def found_root (edge_tree, nodes, call):
    node_weight = [0]*len(nodes)
    external_nodes = []
    while len(external_nodes) < len(nodes):
    print(node_weight)
    external_nodes = found_external_nodes (nodes, edge_tree, external_nodes)
    node_weight = copalse_node (nodes, edge_tree, external_nodes, node_weight)
    print(node_weight)
    return call

def found_external_nodes (node_list, edge_list, external_nodes):
    for node in node_list:
        if not in_node_list (node, external_nodes):
            count = 0
            for edge in edge_list:
                if (node.node_id == edge.source) or (node.node_id == edge.target):
                    count = count + 1
            if count == 1:
                external_nodes.append(node)
    return external_nodes

def in_node_list (actual_node, external_nodes):
    
    if len(external_nodes) > 0:
        for node in external_nodes:
            if actual_node.node_id == node.node_id:
                return True
    
    return False

def copalse_node (node_list, edge_list, external_nodes, node_weight):
    for external in external_nodes:
        for edge in edge_list:
            if external.node_id == edge.source:
                for node in node_list:
                    if node.node_id == edge.source:
                        node_weight [node_list.index(node)] = node_weight [node_list.index(node)] + 1
            elif external.node_id == edge.target:
                for node in node_list:
                    if node.node_id == edge.target:
                        node_weight [node_list.index(node)] = node_weight [node_list.index(node)] + 1
    return node_weight
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
                img, ref_point = create_graph_img (graph)
                cv2.imwrite(graph.name + ".png", img, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
            elif opt == "-kruskal":
                graph = read_xmlfile(argv[-1])
                img, ref_point = create_graph_img (graph)
                edge_tree = kruskal_algorithm (graph)
                img = draw_tree(img, ref_point, edge_tree, graph.node_list, graph.name)
                cv2.imwrite(graph.name + "_Kruskal_Tree.png", img, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
            elif opt == "-prim":
                graph = read_xmlfile(argv[-1])
                img, ref_point = create_graph_img (graph)
                edge_tree = prim_algorithm (graph)
                img = draw_tree(img, ref_point, edge_tree, graph.node_list, graph.name)
                cv2.imwrite(graph.name + "_Prim_Tree.png", img, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
            elif opt == "-trees":
                graph = read_xmlfile(argv[-1])
                create_both_trees (graph)
            elif opt == "-alltrees":
                rute = argv[-1]
                for element in listdir(rute):
                    graph = read_xmlfile(rute + element)
                    create_both_trees (graph)
            elif opt == "-root":
                graph = read_xmlfile(argv[-1])
                img, ref_point = create_graph_img (graph)
                edge_tree = prim_algorithm (graph)
                print (found_root (edge_tree, graph.node_list, 1))
                img = draw_tree(img, ref_point, edge_tree, graph.node_list, graph.name)
                cv2.imwrite(graph.name + "_Prim_Tree.png", img, [int(cv2.IMWRITE_JPEG_QUALITY), 90])

    except IOError:
        print("Error parsing command line options")
        sys.exit(2)

try:
    parse_command_line (sys.argv)
except KeyboardInterrupt:
    pass
