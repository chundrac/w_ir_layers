import numpy as np
from collections import defaultdict
from numpy import exp,log
from functools import reduce
import pickle as pkl
import itertools
from scipy.stats import entropy
from scipy.spatial.distance import jensenshannon


np.random.seed(0)


change_list = []
for line in open('change_list.csv','r'):
    change_list.append(line.strip('\n').split('\t'))



output_list = defaultdict(list)
for l in change_list:
    output_list[(l[1],l[3])].append(l[4])



for k in output_list.keys():
    output_list[k] = sorted(set(output_list[k]))



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


f = open('posteriors_relabeled.pkl','rb')
post = pkl.load(f)
f.close()



thetas = post[0]
phis = post[1]


theta = np.mean(np.stack([v for v in thetas.values()]),0)
phi = np.mean(np.stack([v for v in phis.values()]),0)


Z = np.exp(np.dot(lang_binary,np.log(theta)) + np.dot(feat_binary,np.log(phi.T)))
Z /= np.expand_dims(np.sum(Z,1),-1)


change_type = defaultdict(list)
f = open('p_z_all.tex','w')
for i,l in enumerate(change_list_final):
    change_type[tuple(l[3:])].append(Z[i,])
    prob_vector = l+['{0:.2f}'.format(p) for p in (Z[i,])]
    print(' & '.join(prob_vector)+'\\\\',file=f)


f.close()

for k in change_type.keys():
    change_type[k] = np.mean(np.array(change_type[k]),0,dtype=np.float64)



change_post = defaultdict(list)
for i,l in enumerate(change_list_final):
    change_post[(l[1],l[3],l[4])].append(Z[i,])


for k in change_post.keys():
    change_post[k] = np.mean(np.array(change_post[k]),0)


etyma = sorted(set([k[0] for k in change_post.keys()]))



f = open('p_z_averaged.tex','w')
for e in etyma:
    print('\\hline',file=f)
    for k in sorted(list(change_post.keys())):
        if k[0] == e:
            ll = list(k)+['{0:.2f}'.format(p) for p in change_post[k]]
            #print(ll)
            print(' & '.join(ll)+'\\\\',file=f)


f.close()



change_type[('no pro',)] = change_type[('pro', 'no pro')]
change_type[('pro',)] = change_type[('pro', 'pro')]

change_type[('no meta',)] = change_type[('meta', 'no meta')]
change_type[('meta',)] = change_type[('meta', 'meta')]
change_type[('meta unclear',)] = change_type[('meta', 'unclear')]

change_type.pop(('pro', 'no pro'))
change_type.pop(('pro', 'pro'))
change_type.pop(('meta', 'no meta'))
change_type.pop(('meta', 'meta'))
change_type.pop(('meta', 'unclear'))


f = open('change_dists.txt','w')
for i in range(len(change_type.keys())):
    ll = ['>'.join(list(change_type.keys())[i]).replace('\\textsubarch{u}','w').replace('\\textsubarch{i}','y')]
    x = np.round(change_type[list(change_type.keys())[i]],5)
    for j in range(len(change_type.keys())):
        y = np.round(change_type[list(change_type.keys())[j]],5)
        #print(x,y)
        #print(jensenshannon(x,y))
        ll.append(str(jensenshannon(x,y)))
        #ll.append(str(jensenshannon(np.round(phi_[i],5),np.round(phi_[j],5))))
    print('\t'.join(ll),file=f)


f.close()


lonlat = {}
glotto = {}
for l in open('language_locations.txt','r'):
    l = l.strip().split('\t')
    lonlat[l[0].replace('_',' ')]=(l[-2],l[-1])
    glotto[l[0].replace('_',' ')]=l[1]
    

lonlat['Bakhtiyari'] = lonlat['Bakhtiyari_A'.replace('_',' ')]
lonlat['Middle Persian'] = lonlat['Pahlavi']
lonlat['Talysh'] = lonlat['Talysh_Paul'.replace('_',' ')]
glotto['Bakhtiyari'] = glotto['Bakhtiyari_A'.replace('_',' ')]
glotto['Middle Persian'] = glotto['Pahlavi']
glotto['Talysh'] = glotto['Talysh_Paul'.replace('_',' ')]
    


f = open('iran_components.txt','w')
for i,l in enumerate(langs):
    print(' '.join([
           l.replace(' ','\\underline{\\phantom{X}}'),
           #l,
           glotto[l],
           lonlat[l][0],
           lonlat[l][1],
           ]+
           ['{0:.2f}'.format(p) for p in theta[i,]]),file=f)


f.close()