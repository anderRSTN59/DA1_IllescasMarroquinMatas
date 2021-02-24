#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from xml.dom import minidom
from os import listdir
from MyGraph import MyGraph, read_xmlfile
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
