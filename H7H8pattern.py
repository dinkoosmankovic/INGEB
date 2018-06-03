#!/usr/bin/env python

import sys
import glob
from difflib import get_close_matches, SequenceMatcher
from itertools import tee

H7 = ["GGACCGACTACGTCGGTCC", "GGACCGACTCCTTCGGTCC","GGCCCGACTACGTCGGCGACC"]
H8 = ["GGGATATCCTCTGATATCCC", "GGGATATCCGAGGATATCCC"]
cut_off = 0.9

def get_data_set(path=None):
    return glob.glob(path+"/*.txt")

def read_file(filename):
    f = open(filename, 'r')
    a_string = ""
    for line in f:
        if line[0] == '>':
            continue
        line = line[:-1]
        a_string += line
    f.close()
    a_string = a_string.replace("\r", "")
    return a_string

def get_h7_score(substring):
    ratio = 0
    for h7 in H7:
        ratio = max(ratio, SequenceMatcher(None, substring, h7).ratio())
    return ratio


def get_h8_score(substring):
    ratio = 0
    for h8 in H8:
        ratio = max(ratio, SequenceMatcher(None, substring, h8).ratio())
    return ratio


def get_closest_h7s(a_string):
    h7s = []
    for i in range(len(a_string) - len(H7[0])):
        score1, score2 = 0, 0
        substring1 = a_string[i:i+len(H7[0])]
        substring2 = a_string[i:i+len(H7[2])]
        seq1 = get_close_matches(substring1, H7, cutoff=cut_off)
        if len(seq1) > 0:
            score1 = round(get_h7_score(substring1),3)
        seq2 = get_close_matches(substring2, H7, cutoff=cut_off)
        if len(seq2) > 0:
            score2 = round(get_h7_score(substring2),3)
        seq = seq1 + seq2
        if score1 > cut_off:
            h7s.append((i, score1, substring1, H7))
        elif score2 > cut_off:
            h7s.append((i, score2, substring2, H7))
    return h7s

def get_closest_h8s(a_string):
    h8s = []
    for i in range(len(a_string) - len(H8[0])):
        score1, score2 = 0, 0
        substring1 = a_string[i:i+len(H8[0])]
        seq1 = get_close_matches(substring1, H8, cutoff=cut_off)
        if len(seq1) > 0:
            score1 = round(get_h8_score(substring1),3)
        if score1 > cut_off:
            h8s.append((i, score1, substring1, H8))
    return h8s

def get_positions(hlist):
    l = []
    for h in hlist:
        l.append(h[0])
    return l

def cut_indices(numbers):
    # this function iterate over the indices that need to be 'cut'
    for i in xrange(len(numbers)-1):
        if numbers[i+1] - numbers[i] > 15:
            yield i+1

def splitter(numbers):
    # this function split the original list into sublists.
    px = 0
    for x in cut_indices(numbers):
        yield numbers[px:x]
        px = x
    yield numbers[px:]

def cluster(numbers):
    # using the above result, to form a dict object.
    cluster_ids = xrange(1,len(numbers))
    return dict(zip(cluster_ids, splitter(numbers)))

def get_max_point(hlist, part):
    max_v = 0
    max_i = 0
    for h in hlist:
        if h[0] in part and h[1] > max_v:
            max_v = h[1]
            max_i = h
    return max_i, max_v

def process_hlist(hlist, dict):
    new_hlist = []
    #print dict
    for k in dict:
        new_hlist.append(get_max_point( hlist, dict[k] ))
    return new_hlist

def possible_h7_h8_pairs(h7s, h8s, diff):
    pairs = []
    for h7 in h7s:
        h7_i = h7[0][0]
        h7_s = h7[0][2]
        for h8 in h8s:
            h8_i = h8[0][0]
            h8_s = h8[0][2]
            if h7_i < h8_i:
                if h8_i - h7_i - len(h7_s) <= 10:
                    pairs.append((h7, h8))
            else:
                if h7_i - h8_i - len(h8_s) <= 10:
                    pairs.append((h7, h8))
    return pairs


if __name__ == "__main__":
    path = "./dataset1"
    dataset = list(get_data_set(path))
    print dataset
    for fs in dataset:
        a_string = read_file(fs)
        #print a_string, len(a_string)
        print("Reading file: " + fs)
        print("--------------------- H7 ---------------------")
        print(a_string)
        h7s = get_closest_h7s(a_string)
        h7s = process_hlist(h7s, cluster(get_positions(h7s)))
        for h7 in h7s:
            print h7
        #print get_positions(h7s)

        print("----------------------------------------------")
        print("--------------------- H8 ---------------------")
        h8s = get_closest_h8s(a_string)
        h8s = process_hlist(h8s, cluster(get_positions(h8s)))
        for h8 in h8s:
            print h8
        print("----------------------------------------------\n\n\n")
