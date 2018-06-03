import csv
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from fitter import Fitter
import scipy.stats

def normalize(v):
    norm=np.linalg.norm(v)
    if norm==0:
       return v
    return v/norm

def generate_histogram(name, freqs, dist, xmin, xmax, error):
    fig,ax = plt.subplots()
    ax.cla()
    X = np.linspace(xmin, xmax, len(dist))
    ax.hist(freqs, normed=1)
    ax.hold(True)
    ax.plot(X, dist)
    #ylabel('Probability')
    #plt.axis([0, len(freqs), 0, max(freqs)])
    #plt.show();
    fig.savefig("img/"+name+".png")

rows = []
allele_variants = {}
with open('database.csv', 'rb') as csvfile:
    filereader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in filereader:
        rows.append(row)
    header = rows[0]
    print(header)
    for h in header[1:]:
        allele_variants[h] = []
    for row in rows[1:]:
        for i in range(1,len(row)):
            allele_variants[header[i]].append(int(float(row[i])))

#print(allele_variants)
output = {}

for av in allele_variants:
    allele_variants[av] = np.array(allele_variants[av])
    print("Now working with %s" % (av))
    f = Fitter(allele_variants[av],bins=max(allele_variants[av])-min(allele_variants[av]))
    #f.distributions = f.distributions[0:10] + ['gamma']
    f.fit()
    #array = f.fitted_pdf[f.get_best().keys()[0]]
    #print(f.get_best())
    #generate_histogram(av, allele_variants[av], array, f._get_xmin(), f._get_xmax(), )
    f.summary(Nbest=1)
    output[av] = f.get_best()
    plt.savefig("img/"+av+".png")
    print("Finished!")
    #exit()

print(output)
