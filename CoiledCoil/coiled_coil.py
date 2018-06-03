from Bio.SeqUtils.ProtParam import ProteinAnalysis
from AA import amino_acids
import matplotlib.pyplot as plt
from scipy.signal import find_peaks_cwt
from peakdetect import peakdetect
import numpy as np

def process_file(filename):
    indices = []
    f = open(filename, 'r')
    a_string = f.read()
    a_string = a_string.split('>')
    for i in a_string:
        i = '>' + i
        print(i)
    return a_string

def generate_plot(key, my_seq):
    analysed_seq = ProteinAnalysis(my_seq)
    l = len(my_seq)

    window_size = 21
    
    scale = analysed_seq.protein_scale(param_dict=amino_acids, window=window_size, edge=0.75)

    x = range((window_size+1)/2,len(scale)+(window_size+1)/2)

    lookahead = 7
    minp, maxp = peakdetect(scale, lookahead=(lookahead+1)/2)

    start = min(x)-1

    xpeaks = [xp[0]+(window_size+1)/2 for xp in minp]
    ypeaks = [scale[xpi-(window_size+1)/2] for xpi in xpeaks]

    t_x = np.array(scale)
    added_min = np.where(t_x < 0.9)[0]

    print(added_min)
    

    xdpeaks = [xdp[0]+(window_size+1)/2 for xdp in maxp]
    ydpeaks = [scale[xdpi-(window_size+1)/2] for xdpi in xdpeaks]

    num_pos = np.where(np.array(ydpeaks) < 0.9)[0].size 
    print(num_pos)
    if num_pos == 0 and len(added_min) != 0:
        added_val = [scale[i] for i in list(added_min)]
        minimum = added_val.index(min(added_val))-start+2
        print(added_min[minimum]) 
        print(added_val[minimum]) 
        xdpeaks.append(added_min[minimum])
        ydpeaks.append(added_val[minimum])

    print("maxs:",np.array(xpeaks)+start)
    print("mins:",np.array(xdpeaks)+start)
    #print(scale)
    plt.clf()
    plt.plot(x,scale,'b', xpeaks, ypeaks ,'ro', xdpeaks, ydpeaks ,'go')
    plt.grid(True)
    #plt.axis([0,max(x), min(scale)-0.05*min(scale), max(scale)+0.05*max(scale)])
    #plt.axis([0,max(x), 0.85, max(scale)+0.05*max(scale)])
    plt.legend( ['Scores for '+key])#,'local maxima', 'local minima' ])
    plt.xlabel('Position')
    plt.ylabel('Score')
    plt.savefig('figs/'+key+'.png')
    #plt.show()

f = open("anotirani_zipperi1.txt", 'r')
a_string = f.read()
a_string = a_string.split('>')

sequences = {}

for a in a_string:
    a = a.replace('\r','')
    lines = a.split('\n')
    key = lines[0]
    value = ""
    for i in range(1,len(lines)):
        value += lines[i]
    if key != '':
        sequences[key] = value

for key in sequences:
    print(key)
    #generate_plot(key, sequences[key])

