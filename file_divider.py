#!/usr/bin/env python

import sys
import ntpath

def path_leaf(path):
    head, tail = ntpath.split(path)
    return head, tail or ntpath.basename(head)

def process_file(filename):
    indices = []
    f = open(filename, 'r')
    a_string = f.read()
    a_string = a_string.split('>')
    for i in a_string:
        i = '>' + i
        print(i)
    return a_string

def write_files(filename, a_string):
    head, filename = path_leaf(filename)
    filename = filename.split('.')[0]
    for i in a_string:
        new_filename = head + "/" + filename + str(a_string.index(i) + 1) + ".txt"
        f = open(new_filename, "w")
        f.write(">" + i)
        f.close()


a_string = process_file(sys.argv[1])
a_string = [a_s for a_s in a_string if len(a_s) != 0]
write_files(sys.argv[1], a_string)
