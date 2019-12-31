#import pymc3 as pm
#import theano.tensor as tt
#import theano
import numpy as np
from collections import defaultdict
from numpy.random import multinomial,randint,binomial
from numpy.random import gamma as Gamma
from numpy.random import beta as Beta
from numpy import exp,log
from functools import reduce
#theano.config.gcc.cxxflags = "-fbracket-depth=6000"
#THEANO_FLAGS = "-fbracket-depth=6000"
import pickle as pkl
import itertools
from scipy.stats import entropy


nchains = 4

change_list = []
for line in open('change_list.csv','r'):
    change_list.append(line.strip('\n').split('\t'))



output_list = defaultdict(list)
for l in change_list:
    output_list[(l[1],l[3])].append(l[4])



for k in output_list.keys():
    output_list[k] = set(sorted(output_list[k]))



output_list = {k:output_list[k] for k in output_list.keys() if len(output_list[k]) > 1}
changes_flat = [(k,v) for k in output_list.keys() for v in output_list[k]]

S = len(changes_flat)
X = len(output_list.keys())
R = [len(output_list[k]) for k in output_list.keys()]
assert S == sum(R)


change_list_final = []
for l in change_list:
    change = ((l[1],l[3]),l[4])
    if change in changes_flat and l[0] != 'Middle Persian':
        change_list_final.append(l)



langs = sorted(set([l[0] for l in change_list_final]))
L = len(langs)
lang_binary = []
feat_binary = []
for l in change_list_final:
    change = ((l[1],l[3]),l[4])
    if change in changes_flat:
        lang_string = [0]*L
        lang_string[langs.index(l[0])] = 1
        feat_string = [0]*S
        feat_string[changes_flat.index(change)] = 1
        lang_binary.append(lang_string)
        feat_binary.append(feat_string)



N = len(feat_binary)
lang_binary = np.array(lang_binary)
feat_binary = np.array(feat_binary)

part = [[0,R[0]]]+[[reduce(lambda x,y:x+y,R[:i]),reduce(lambda x,y:x+y,R[:i+1])] for i in range(1,X)]




T = 10

posterior = []
for c in range(nchains):
    f = open('posterior_FINAL_dir_{}.pkl'.format(c),'rb')
    posterior.append(pkl.load(f))
    f.close()




phi = {}
theta = {}
for c in range(len(posterior)):
    phi[c] = np.mean(np.array([np.concatenate([posterior[c]['phi_{}_{}'.format(t,x)] for x in range(X)],axis=1) for t in range(T)]).transpose([1,0,2]),0)
    theta[c] = np.mean(np.array([posterior[c]['theta_{}'.format(l)] for l in range(L)]).transpose([1,0,2]),0)



perms = list(itertools.chain(itertools.permutations(range(T))))
for i in range(1,len(posterior)):
    perm_KL = []
    for p in perms:
        perm_KL.append(sum(entropy(theta[i].T[p,:],theta[0].T))+sum(entropy(phi[i].T[:,p],phi[0].T)))
    perm = perms[perm_KL.index(min(perm_KL))]
    phi[i] = phi[i][perm,:]
    theta[i] = theta[i][:,perm]
    print('{} done'.format(i))



f = open('posteriors_relabeled.pkl','wb')
pkl.dump((theta,phi),f)
f.close()
