#!/usr/bin/env python

import sys


def check_substring(sub, test):
    for ch in sub:
        if ch in test:
            return True
    return False


def split_by_n(seq, n):
    """A generator to divide a sequence into chunks of n units."""
    while seq:
        yield seq[:n]
        seq = seq[n:]


def get_numbering(size, ticks=11):
    string = [str(i + i // 10 + 1) if i % 9 == 0 else '-' for i in range(size)]
    string[0] = '1'
    string = ''.join(string)
    return string


def output_to_file(filename, sequence, numbering, indices):
    f = open(filename, 'w')
    div = 75
    lseq = ""
    for i in range(len(sequence)):
        lseq += " "
    list_sequence = list(split_by_n(sequence, div))
    list_numbering = list(split_by_n(numbering, div))
    new_line_indices = []
    new_line_indices1 = []
    lseq_new = str(lseq)
    lseq_new1 = str(lseq)

    for i in indices:
        if (indices.index(i) > 0) and (i[0] - indices[indices.index(i)-1][0] > 14):
            ind, templ = i[0], i[1]
            temp = lseq[0:ind] + templ + lseq[ind + 22:]
            lseq = temp
        elif indices.index(i) == 0:
            ind, templ = i[0], i[1]
            temp = lseq[0:ind] + templ + lseq[ind + 22:]
            lseq = temp
        else:
            new_line_indices.append(i)

    if len(new_line_indices) != 0:
        for i in new_line_indices:
            if (new_line_indices.index(i) > 0) and (i[0] - new_line_indices[new_line_indices.index(i)-1][0] > 14):
                ind, templ = i[0], i[1]
                temp = lseq_new[0:ind] + templ + lseq_new[ind + 22:]
                lseq_new = temp
            elif new_line_indices.index(i) == 0:
                ind, templ = i[0], i[1]
                temp = lseq_new[0:ind] + templ + lseq_new[ind + 22:]
                lseq_new = temp
            else:
                new_line_indices1.append(i)
        if len(new_line_indices1) != 0:
            ind, templ = i[0], i[1]
            temp = lseq[0:ind] + templ + lseq[ind + 22:]
            lseq = temp

    list_lseq = list(split_by_n(lseq, div))
    list_lseq_new = list(split_by_n(lseq_new, div))
    for i in range(len(list_sequence)):
        f.write(list_numbering[i] + "\n")
        f.write(list_sequence[i] + "\n")
        f.write(list_lseq[i] + "\n")
        if len(new_line_indices) != 0:
            f.write(list_lseq_new[i] + "\n")
        f.write("\n")
    f.close()


def run_coiled_coils(filename):
    from subprocess import Popen, PIPE
    p = Popen('ncoils -f <' + filename, shell=True, stdout=PIPE)
    out, err = p.communicate()
    ind = 0
    if out != "":
        ind = out.index('\n')
    out = out[ind:]
    return out


def check_seq(coiled_coils, index):
    return True
    if coiled_coils == "":
        return True
    for i in range(index, index + 14):
        if coiled_coils[i] != "x":
            return False
    return True


def process_file(filename, test=['I', 'L', 'M', 'V']):
    indices = []
    f = open(filename, 'r')
    a_string = ""
    for line in f:
        if line[0] == '>':
            continue
        line = line[:-1]
        a_string += line
    f.close()

    coiled_coils = run_coiled_coils(filename)
    #print(coiled_coils)

    for index in range(len(a_string) - 22):
        if a_string[index] in test and a_string[index + 7] in test and \
                a_string[index + 14] in test and a_string[index + 21] in test and \
                check_seq(coiled_coils, index):
            template = a_string[index] + '------' + a_string[index + 7] + '------' + \
                a_string[index + 14] + '------' + a_string[index + 21]
            indices.append((index, template))
    return a_string, indices


output, indices = process_file(sys.argv[1])
for ind in indices:
    print(ind)
# print(get_numbering(len(output)))
# print(output)
size = get_numbering(len(output))
output_to_file(sys.argv[2], output, size, indices)
