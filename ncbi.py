#!/usr/bin/env python

import sys
from Bio import Entrez
import H7H8pattern as processing
from dataset import *

def get_data_from_ncbi(id, term):
    Entrez.email = "Your.Name.Here@example.org"
    handle = Entrez.esearch(db="nucleotide", retmax=10, term=term)
    record = Entrez.read(handle)
    #id = record["IdList"][0]

    handle = Entrez.efetch(db="nucleotide", id=str(id), rettype="gb", retmode="xml")
    #print(handle.read())
    records = Entrez.read(handle)
    handle.close()
    print len(records)
    sequence = records[0]["GBSeq_sequence"]
    sequence = sequence.upper()
    features = list(records[0]["GBSeq_feature-table"])
    #print features[0]
    for feature in list(features):
        #print feature["GBFeature_key"]
        if feature["GBFeature_key"] not in ["CDS"]:
            features.remove(feature)

    #print features
    ftrs = []
    for feature in features:
        ftr = (feature["GBFeature_key"], \
              feature["GBFeature_intervals"][0]["GBInterval_from"], \
              feature["GBFeature_intervals"][0]["GBInterval_to"])
        ftrs.append(ftr)
    return (term, sequence, ftrs)

def check_in_intergene_space(hlist, ftrs):
    new_hlist = []
    for h in hlist:
        check = False
        for ftr in ftrs:
            #print h[0][0], int(ftr[1]), int(ftr[2])
            if h[0][0] >= int(ftr[1])-1 and h[0][0] <= int(ftr[2])-1:
                check = True
                break
        if check == False:
            new_hlist.append(h)
    return new_hlist

def get_seq_l_u(seq, pairs):
    result = []
    for p in pairs:
        h7_i = p[0][0][0]
        h7_s = p[0][0][2]
        h8_i = p[1][0][0]
        h8_s = p[1][0][2]
        if h7_i < h8_i:
            pivot = h7_i + len(h7_s)
            inter_s = seq[pivot:h8_i]
            subseq = h7_s + " " + inter_s + " " + h8_s
            result.append((h7_i, "H7-<intr>-H8", subseq))
        else:
            pivot = h8_i + len(h8_s)
            inter_s = seq[pivot:h7_i]
            subseq = h8_s + " " + inter_s + " " + h7_s
            result.append((h8_i,"H8-<intr>-H7", subseq))
    return result

def get_incomplete_with_st(hlist, indices, st, sequence):
    new_hlist = []
    for h in hlist:
        h_i = h[0][0]
        if h_i not in indices:
            h_s = h[0][2]
            if sequence[h_i + len(h_s)+1:h_i + len(h_s)+1+len(st)] == st:
                subseq = h_s + " " + st
                new_hlist.append( (hi_i, "HX-"+st, subseq) )
            if sequence[h_i - len(st): h_i] == st:
                subseq = st + " " + h_s
                new_hlist.append( (h_i-len(st), st+"-HX", subseq) )
    return new_hlist


for i in range(len(dataset)):
    (term, sequence, ftrs) = get_data_from_ncbi(dataset[i][0], dataset[i][1])
    print(term)
    print("----------------------H7------------------------------")
    h7s = processing.get_closest_h7s(sequence)
    h7s = processing.process_hlist(h7s, processing.cluster(processing.get_positions(h7s)))
    h7s = check_in_intergene_space(h7s, ftrs)
    for h7 in h7s:
        print h7
    print("------------------------------------------------------")
    print("----------------------H8------------------------------")
    h8s = processing.get_closest_h8s(sequence)
    h8s = processing.process_hlist(h8s, processing.cluster(processing.get_positions(h8s)))
    h8s = check_in_intergene_space(h8s, ftrs)
    for h8 in h8s:
        print h8
    print("------------------------------------------------------")
    pairs = processing.possible_h7_h8_pairs(h7s, h8s, 10)
    result_pairs = get_seq_l_u(sequence, pairs)
    #print len(pairs), len(result)
    indices = [p[0][0][0] for p in pairs] + [p[1][0][0] for p in pairs]
    print("-----------------------PAIRS-------------------------------")
    for r in result_pairs:
        print r
    print("-----------------------------------------------------------")
    print("-----------------------H7INC-------------------------------")
    result_h7s_incomplete = get_incomplete_with_st(h7s, indices, "TATATA", sequence)
    for r in result_h7s_incomplete:
        print r
    print("-----------------------------------------------------------")
    print("-----------------------H8INC-------------------------------")
    result_h8s_incomplete = get_incomplete_with_st(h8s, indices, "TATATA", sequence)
    for r in result_h8s_incomplete:
        print r
#for ftr in ftrs:
#    print ftr
#print(len(h7s))
#print(len(h8s))
