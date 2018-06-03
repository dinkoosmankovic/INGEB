#!/usr/bin/env python

#!/usr/bin/env python

import sys
import ntpath
import numpy as np
import matplotlib
matplotlib.use('GTKAgg')
import matplotlib.pyplot as plt


def get_hydrophobic_value(amino):
    hpValues = {
        'F': 100,
        'I': 99,
        'W': 97,
        'L': 97,
        'V': 76,
        'M': 74,
        'Y': 63,
        'C': 49,
        'A': 41,
        'T': 13,
        'H': 8,
        'G': 0,
        'S': -5,
        'Q': -10,
        'R': -14,
        'K': -23,
        'N': -28,
        'E': -31,
        'P': -46,
        'D': -55
    }
    return hpValues.get(amino)


def path_leaf(path):
    head, tail = ntpath.split(path)
    return head, tail or ntpath.basename(head)


def process_file(filename):
    indices = []
    f = open(filename, 'r')
    a_string = ""
    for line in f:
        if line[0] == '>' or line[0] == "\n":
            continue
        line = line[:-1]
        a_string += line
    f.close()
    a_string = list(a_string.split("\r"))
    return a_string


def write_files(filename, a_string):
    head, filename = path_leaf(filename)
    filename = filename.split('.')[0]
    for i in a_string:
        new_filename = head + "/" + filename + \
            str(a_string.index(i) + 1) + ".txt"
        f = open(new_filename, "w")
        f.write(">" + i)
        f.close()


def get_sequences(filename, start, stop):
    a_string = process_file(filename)
    a_string = [a_s for a_s in a_string if len(a_s) > 1 and a_s[0] != " "]
    values = [0 for i in range(start, stop + 1)]
    rep = [0 for i in range(start, stop + 1)]
    for a_s in a_string:
        a_s = a_s[start:stop + 1]
        # print(a_s)
        for k, amino in enumerate(a_s):
            val = get_hydrophobic_value(amino)
            if val is None:
                rep[k] += 1
            else:
                values[k] += val

    number_of_aminos = len(a_string)
    values = [v / float(number_of_aminos-r) for v, r in zip(values, rep)]
    return values


def plot_values(values, start, stop, plotfile):
    x = np.arange(start, stop + 1, 1)
    y = values
    plt.plot(x, y, 'b-')
    plt.plot(x, y, 'r^')
    plt.grid(True)
    plt.xlabel("Residue Number")
    plt.ylabel("Hydrophobicity")
    plt.axis([start - 1, stop + 1, min(y) - 5, max(y) + 5])
    plt.savefig(plotfile,dpi=600,format="png")
    plt.show()

start = 10
stop = 42

values = get_sequences(sys.argv[1], start, stop)
path, filename = path_leaf(sys.argv[1])
plotfile = "./" + path + "/" + filename[:filename.index(".txt")]+".png"
plot_values(values, start, stop, plotfile)
