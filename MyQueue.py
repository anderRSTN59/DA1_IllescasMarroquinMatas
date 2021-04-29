#!/usr/bin/python3
# -*- coding: utf-8 -*-

#pylint: disable-msg=c0103
#pylint: disable-msg=c0114

class MyQueue:
    '''implementacion de clase lista ordenada'''
    def __init__(self):
        self.element_list = []

    def copy_list (self, origin_list):                                      #2
        '''copia una lista de elementos a otra y luego la ordena'''
        for new_element in origin_list:                                     #bucles = n
        # for (i = 0; i<len(origin_list); i++)                               6
            self.element_list.append(new_element)                           #3
        self.first_quick_sort_call()                                        #1

    def add_element (self, element):                                        #2
        '''añade un nuevo elemento a la lista y lo ordena'''
        self.element_list.append(element)                                   #3
        self.first_quick_sort_call()                                        #T(n)

    def first_quick_sort_call (self):                                       #1
        '''primera llamada del quicksort'''
        self.my_quick_sort (0, len(self.element_list)-1)                    #T(n) + 4

    def my_quick_sort (self, left, rigth):                                  #3
        '''implementacion del metodo quicksort'''
        pivote = self.element_list[left]                                    #3
        i = left                                                            #2
        j = rigth                                                           #2

        while i < j:                                                        #2
            while (self.element_list[i].length <= pivote.length) & (i < j): #7
                i = i + 1                                                   #2
            while self.element_list[j].length > pivote.length:              #5
                j = j - 1                                                   #2
            if i < j:                                                       #1
                aux = self.element_list[i]                                  #3
                self.element_list[i] = self.element_list[j]                 #5
                self.element_list[j] = aux                                  #3

        self.element_list[left] = self.element_list[j]                      #5
        self.element_list[j] = pivote                                       #3

        if left < (j-1):                                                    #2
            self.my_quick_sort (left, j-1)                                  #T(n/2) + 3
        if (j+1) < rigth:                                                   #2
            self.my_quick_sort (j+1, rigth)                                 #T(n/2) + 3
