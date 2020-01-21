import pymc3 as pm
import theano.tensor as tt
import theano
import numpy as np
from collections import defaultdict
#theano.config.gcc.cxxflags = "-fbracket-depth=6000"
#THEANO_FLAGS = "-fbracket-depth=6000"
import pickle as pkl


def generate_data():
    """make data and variables"""
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
    return(change_list_final,langs,S,X,R,N,L,lang_binary,feat_binary)


change_list_final,langs,S,X,R,N,L,lang_binary,feat_binary = generate_data()


def GEM(beta):
    """griffiths-engen-mccloskey distribution"""
    pi = tt.concatenate([[1], tt.extra_ops.cumprod(1 - beta)[:-1]])
    return (beta * pi)



def logprob(theta,phi):
    """log-likelihood function, with discrete latent variables marginalized out"""
    def lprob(lang_array,feat_array):
        lps = pm.math.logsumexp(
                   tt.dot(lang_array      #N by L matrix
                   ,tt.log(theta+1e-1000) #L by T matrix
                  )+                      #N by T matrix
            tt.dot(feat_array             #N by S matrix
                          ,tt.log(phi.T)  #S by T matrix
                         )                #N by T matrix      
        ,axis=1)                          #N-length vector                              
        return(tt.sum(lps))               #constant
    return(lprob)



alpha = 1e-4

T = 10


np.random.seed(0)
model = pm.Model()
with model:
    gamma = pm.Gamma('gamma',1.,1.)
    delta = pm.Gamma('delta',1.,1.)
    beta_prime = tt.stack([pm.Beta('beta_prime_{}'.format(t),1.,gamma) for t in range(T)])
    beta = GEM(beta_prime)
    theta = tt.stack([pm.Dirichlet('theta_{}'.format(l),beta*delta,shape=T) for l in range(L)])
    phi = tt.stack([tt.concatenate([pm.Dirichlet('phi_{}_{}'.format(t,x),tt.ones(R[x])*alpha,shape=R[x]) for x in range(X)]) for t in range(T)])
    target = pm.DensityDist('target',logprob(theta=theta,phi=phi),observed=dict(lang_array=lang_binary,feat_array=feat_binary))
    for c in range(4):
        inference = pm.ADVI()
        inference.fit(100000, obj_optimizer=pm.adam(learning_rate=.01,beta1=.8),callbacks=[pm.callbacks.CheckParametersConvergence()])
        trace = inference.approx.sample()
        posterior = {k:trace[k] for k in trace.varnames if not k.endswith('__')}
        posterior['ELBO'] = inference.hist
        f = open('posterior_FINAL_dir_{}.pkl'.format(c),'wb')
        pkl.dump(posterior,f)
        f.close()
