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

def seq_in_line(line, seq):
    ind, templ = seq[0], seq[1]
    line = [' ' for c in range(len(line))]
    for i in range(len(templ)):
        line[i+ind] = templ[i]
    return line

def mergeable_sequences(sequence1, sequence2):
    result = ""
    if (sequence1 is None or sequence2 is None):
        return False, None
    test = False
    for c1, c2 in zip(sequence1, sequence2):
        if c1 != ' ' and c2 != ' ':
            test = True
            break

    if test == True:
        return False, None
    else:
        for c1, c2 in zip(sequence1, sequence2):
            if (c1 == ' ' and c2 == ' '):
                result += ' '
            elif (c1 != ' '):
                result += c1
            else:
                result += c2
        return True, result

def merge_sequences(sequences):
    for i in range(len(sequences) - 1):
        for j in range(i+1, len(sequences)):
            test, seq = mergeable_sequences(sequences[i], sequences[j])
            if test == True:
                sequences[i] = seq
                sequences[j] = None
    return sequences

def output_to_file(filename, sequence, numbering, indices):
    f = open(filename, 'w')
    div = 75
    lseq = ""
    for i in range(len(sequence)):
        lseq += " "
    list_sequence = list(split_by_n(sequence, div))
    list_numbering = list(split_by_n(numbering, div))

    sequences = [ sequence for i in range(len(indices)) ]
    str_sequences = []

    for i, seq in zip(indices, sequences):
        print(i)
        line = seq_in_line(seq, i)
        str_sequences.append(''.join(line))

    merged = merge_sequences(str_sequences)
    merged = [x for x in merged if x is not None]
    merged_new = [ list(split_by_n(i, div)) for i in merged]

    for i in range(len(list_sequence)):
        f.write(list_numbering[i] + "\n")
        f.write(list_sequence[i] + "\n")
        for j in merged_new:
            f.write(j[i] + "\n")
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
# print(get_numbering(len(output)))
# print(output)
size = get_numbering(len(output))
output_to_file(sys.argv[2], output, size, indices)
