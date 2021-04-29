#!/usr/bin/python3
# -*- coding: utf-8 -*-

#pylint: disable-msg=c0103
#pylint: disable-msg=c0114
#pylint: disable-msg=e1101

import sys
import cv2
import matplotlib.pyplot as pl
from os import listdir
from MyDraw import create_graph_img, create_tree_img, create_root_img
from MyGraph import MyGraph, read_xmlfile, create_graphml
from MyNode import MyNode
from MyEdge import MyEdge
from MyQueue import MyQueue
base = dict()

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

def findParentKruskal(nodeIDstr):
    if base[nodeIDstr] == nodeIDstr :
        return nodeIDstr
    return findParentKruskal(base[nodeIDstr])

def kruskal_algorithm (graph):    
    
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
        
            
            
    
    print("Terminado Kruskal de " + graph.name )
    print("-------------------------------------------------------")
    
    return ARC

def kruskal_algorithm2 (graph):
    '''encuentra el arbol de recubrimiento usando Kruskal'''
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

def create_both_trees (graph, scaled):
    '''crea las ambas imagenes del arbol de recubrimiento'''
    kuscal_tree = kruskal_algorithm (graph)
    prim_tree = prim_algorithm (graph)
    create_tree_img (graph, kuscal_tree, "_Kruskal_", scaled)
    create_tree_img (graph, prim_tree, "_Prim_", scaled)

def found_root(node_list, edge_list):
    '''busca el nodo raiz que divida el grafo en subgrafos de similar peso'''
    longitude = len(node_list)
    weigth = [0]*len(node_list)
    neighbor_matrix = create_neighbor_matrix (node_list, edge_list)
    '''
    print_matrix(neighbor_matrix)
    '''
    link_count = create_link_count (neighbor_matrix)
    '''
    print (link_count)
    print ()
    '''
    weigth = overlap_nodes (weigth, link_count, neighbor_matrix)
    '''
    print (weigth)
    print ()
    '''
    i = 1
    max = weigth[0]
    while i < (longitude/2):
        if max < weigth[i] and weigth[i] < (longitude/2):
            max = weigth[i]
        if max < weigth[longitude-i] and weigth[longitude-i] < (longitude/2):
            max = weigth[longitude-i]
        i = i + 1
    return node_list[weigth.index(max)]

def create_neighbor_matrix(node_list, edge_list):
    '''crea una matriz de adyacencia de los nodos'''
    n = len(node_list)
    matrix = [[0]*n for i in range(n)]
    i = 0
    while i < n:
        node = node_list[i]
        for edge in edge_list:
            if edge.source == node.node_id or edge.target == node.node_id:
                j = 0
                while j < n:
                    newnode = node_list [j]
                    if edge.target == newnode.node_id or edge.source == newnode.node_id:
                        if newnode.node_id != node.node_id:
                            matrix[i][j] = 1
                    j = j + 1
        i = i + 1
    return matrix

def overlap_nodes (weigth, links, matrix):
    '''colapsa los nodos hasta aumentado su peso hasta converger '''
    i = 0
    while i < len(links):
        if links[i] == 1:
            j = 0
            while j < len(matrix[i]):
                if matrix[i][j] == 1:
                    matrix[i][j] = 0
                    matrix[j][i] = 0
                    weigth[j] = weigth[j] + weigth[i] + 1
                    if weigth[j] >= len(weigth)/2:
                        return weigth
                    weigth[i] = 0
                    links[i] = links[i] - 1
                    links[j] = links[j] - 1
                j = j + 1
        i = i + 1
    weigth = overlap_nodes (weigth, links, matrix)
    return weigth

def print_matrix(matrix):
    '''bucle que imprime la matriz'''
    for array in matrix:
        print (array)
    print()

def create_link_count (matrix):
    '''crea un array que contiene el numero de enlaces de cada nodo'''
    longitude = len(matrix)
    links = [0]*longitude
    i = 0
    while i < longitude:
        j = 0
        while j < longitude:
            if matrix[i][j] == 1:
                links[i] = links[i] + 1
            j = j + 1
        i = i + 1
    return links

def create_root_graph (rute):
    '''crea un .txt que contiene una lista de nodos raiz de cada grafo de un dir'''
    root_nodes = create_root_graph_nodes (rute)
    root_edges = create_root_graph_edges (root_nodes)
    root_graph = MyGraph("Roots Graph", root_nodes, root_edges)
    create_graphml(root_graph)
    img = create_graph_img (root_graph, 5000)
    cv2.imwrite(root_graph.name + ".png", img, [int(cv2.IMWRITE_JPEG_QUALITY), 90])

def create_root_graph_nodes (rute):
    nodes = []
    for element in listdir(rute):
        graph = read_xmlfile(rute + element)
        edge_tree = kruskal_algorithm (graph)
        nodes.append(found_root (graph.node_list, edge_tree))
    return nodes

def create_root_graph_edges (nodes):
    edges = []
    size = len(nodes)
    i = 0
    while i < size:
        j = i + 1
        while j < (size - 1):
            new_edge = MyEdge(0, nodes[i].node_id, nodes[j].node_id)
            new_edge.length = calc_edge_len(nodes[i].node_coords, nodes[j].node_coords)
            edges.append(new_edge)
            j = j + 1
        i = i + 1
    return edges

def calc_edge_len (node1_coords, node2_coords):
    x_len = abs(node1_coords[0] - node2_coords[0])
    y_len = abs(node1_coords[1] - node2_coords[1])
    tan = x_len*x_len + y_len*y_len
    return int((tan**.5)*113000)

def create_root_list (rute):
    '''crea una lista de nodos raiz de cada uno de los grafos de un dir'''
    txt_file = open ('GraphRootNodeList.txt','w')
    txt_file.write("<Población>, < nodos>")
    txt_file.write("\n")
    for element in listdir(rute):
        graph = read_xmlfile(rute + element)
        edge_tree = kruskal_algorithm(graph)
        txt_file.write(graph.name + ", " + str(found_root (graph.node_list, edge_tree)))
        txt_file.write("\n")
    txt_file.close()

def parse_command_line (argv):
    '''controla el paso de parametros'''
    scale = 40000
    try:
        opt = argv[1]
        if opt == "-help":
            print("Grupo DA-1.\nUso: python3 AD_1_laboratorio.py [-option] [-rute]",
                "\n\tAnderson Marroquín Rivas",
                "\n\tDavid",
                "\n\tMiguel Ángel\n",
                "\n\t[-help]               Muestra ayuda del programa",
                "\n\t[-line]       [-file] Muestra informacion basica de un grafo dado",
                "\n\t[-nodes]      [-file] Muestra todos los nodos de un grafo dado",
                "\n\t[-edges]      [-file] Muestra todas las aristas de un grafo dado",
                "\n\t[-graphs]     [-dir]  Crea un .txt con la información basica de los grafos",
                "dentro de un directorio"
                "\n\t[-draw]       [-file] Crea la imagen de un grafo dado",
                "\n\t[-drawAll]    [-dir]  Crea las imagenes de todos los grafos dentro",
                "de un directorio",
                "\n\t[-kruskal]    [-file] Crea la imagen de un grafo dado con su arbol de",
                "recubrimiento minimo usando el algoritmo de Kruskal",
                "\n\t[-prim]       [-file] Crea la imagen de un grafo dado con su arbol de",
                "recubrimiento minimo usando el algoritmo de Prim",
                "\n\t[-trees]      [-file] Crea las imagenes de un grafo dado con su arbol",
                "de recubrimiento minimo usando los dos algoritmo",
                "\n\t[-allTrees]   [-dir]  Crea las imagenes de todos los grafo con su arbol",
                "de recubrimiento minimo de un directorio usando los dos algoritmo",
                "\n\t[-root]       [-file] Crea la imagen de grafo dado con su arbol",
                "de recubrimiento minimo con su nodo nodo raiz",
                "\n\t[-rootsGraph] [-dir]  Crea un gafo y un .txt con los nodos raiz de todos",
                "los grafo dentro de un directorio",
                "\n\t[-allRoots]   [-dir]  Crea un .txt con la lista de nodos raiz de cada uno",
                "de los grafos de un dir\n")
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
            create_graph_img (graph, scale)
        elif opt == "-drawAll":
            rute = argv[-1]
            for element in listdir(rute):
                graph = read_xmlfile(rute + element)
                create_graph_img (graph, 30000)
        elif opt == "-kruskal":
            graph = read_xmlfile(argv[-1])
            edge_tree = kruskal_algorithm (graph)
            create_tree_img (graph, edge_tree, "_Kruskal_", scale)
        elif opt == "-prim":
            graph = read_xmlfile(argv[-1])
            edge_tree = prim_algorithm (graph)
            create_tree_img (graph, edge_tree, "_Prim_", scale)
        elif opt == "-trees":
            graph = read_xmlfile(argv[-1])
            create_both_trees (graph, scale)
        elif opt == "-allTrees":
            rute = argv[-1]
            for element in listdir(rute):
                graph = read_xmlfile(rute + element)
                create_both_trees (graph, 30000)
        elif opt == "-root":
            graph = read_xmlfile(argv[-1])
            edge_tree = kruskal_algorithm (graph)
            root = found_root (graph.node_list, edge_tree)
            create_root_img (graph, edge_tree, root, scale)
            print (root)
        elif opt == "-rootsGraph":
            create_root_graph(argv[-1])
        elif opt == "-allRoots":
            create_root_list (argv[-1])
        else: 
            print("Opción no válida, intente de nuevo")
    except IOError:
        print("Error parsing command line options")
        sys.exit(2)

try:
    parse_command_line (sys.argv)
except KeyboardInterrupt:
    pass
