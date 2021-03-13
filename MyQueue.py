#!/usr/bin/python3
# -*- coding: utf-8 -*-

class MyQueue:
    '''implementacion de clase lista ordenada'''
    def __init__(self):
        self.element_list = []

    def copy_list (self, origin_list):
        '''copia una lista de elementos a otra y luego la ordena'''
        for new_element in origin_list:
            self.element_list.append(new_element)
        self.first_quick_sort_call()

    def add_element (self, element):
        '''añade un nuevo elemento a la lista y lo ordena'''
        self.element_list.append(element)
        self.first_quick_sort_call()

    def first_quick_sort_call (self):
        '''primera llamada del quicksort'''
        self.my_quick_sort (0, len(self.element_list)-1)

    def my_quick_sort (self, left, rigth):
        '''implementacion del metodo quicksort'''
        pivote = self.element_list[left]
        i = left
        j = rigth

        while i < j:
            while (self.element_list[i].length <= pivote.length) & (i < j):
                i = i + 1
            while (self.element_list[j].length > pivote.length):
                j = j - 1
            if i < j:
                aux = self.element_list[i]
                self.element_list[i] = self.element_list[j]
                self.element_list[j]= aux

        self.element_list[left] =  self.element_list[j]
        self.element_list[j] = pivote

        if left < (j-1):
            self.my_quick_sort (left, j-1)
        if (j+1) < rigth:
            self.my_quick_sort (j+1, rigth)
