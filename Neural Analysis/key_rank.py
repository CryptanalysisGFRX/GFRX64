from os import urandom
from keras.models import load_model

import numpy as np

from random import randint

#load distinguishers
net6 = load_model('best6depth10.keras')


def key_rank_one_round(nr, net, n_blocks=1, diff=(0x0, 0x0, 0x0, 0x0040)):

    plain0l0 = np.frombuffer(urandom(2*n_blocks), dtype=np.uint16).reshape(n_blocks, -1)
    plain0l1 = np.frombuffer(urandom(2*n_blocks), dtype=np.uint16).reshape(n_blocks, -1)
    plain0r0 = np.frombuffer(urandom(2*n_blocks), dtype=np.uint16).reshape(n_blocks, -1)
    plain0r1 = np.frombuffer(urandom(2*n_blocks), dtype=np.uint16).reshape(n_blocks, -1)

    plain1l0 = plain0l0 ^ diff[0]
    plain1l1 = plain0l1 ^ diff[1]
    plain1r0 = plain0r0 ^ diff[2]
    plain1r1 = plain0r1 ^ diff[3]

    plain0l0, plain0l1, plain0r0, plain0r1 = dec_one_round(plain0l0, plain0l1, plain0r0, plain0r1, 0, 0, 0)
    plain1l0, plain1l1, plain1r0, plain1r1 = dec_one_round(plain1l0, plain1l1, plain1r0, plain1r1, 0, 0, 0)

    keys = np.frombuffer(urandom(12*1), dtype=np.uint16).reshape(6, -1).flatten()

    ks = expand_key(keys, nr)
    k2 = ks[-1]
    k1 = ks[-2]
    k0 = ks[-3]

    ctdata0l0, ctdata0l1, ctdata0r0, ctdata0r1 = encrypt((plain0l0, plain0l1, plain0r0, plain0r1), ks, nr)
    ctdata1l0, ctdata1l1, ctdata1r0, ctdata1r1 = encrypt((plain1l0, plain1l1, plain1r0, plain1r1), ks, nr)

    trial_k0 = np.arange(2**16);

    cdata0l0, cdata0l1, cdata0r0, cdata0r1 = dec_one_round(ctdata0l0, ctdata0l1, ctdata0r0, ctdata0r1, trial_k0, k1, k2)
    cdata1l0, cdata1l1, cdata1r0, cdata1r1 = dec_one_round(ctdata1l0, ctdata1l1, ctdata1r0, ctdata1r1, trial_k0, k1, k2)

    cdata0l0 = np.tile(cdata0l0,2**16); cdata0l1 = np.tile(cdata0l1, 2**16);
    #cdata0r0 = np.tile(cdata0r0,2**16); cdata0r1 = np.tile(cdata0r1, 2**16);
    #cdata1l0 = np.tile(cdata1l0,2**16); cdata1l1 = np.tile(cdata1l1, 2**16);
    #cdata1r0 = np.tile(cdata1r0,2**16); cdata1r1 = np.tile(cdata1r1, 2**16);

    X = convert_to_binary([cdata0l0.flatten(), cdata0l1.flatten(), cdata0r0.flatten(), cdata0r1.flatten(), cdata1l0.flatten(), cdata1l1.flatten(), cdata1r0.flatten(), cdata1r1.flatten()])
    
    Z = net.predict(X,batch_size=10000); Z = Z/(1-Z); 
    Z = np.log2(Z); Z = Z.reshape(n_blocks,-1); Z = np.sum(Z,axis=0);
    rank0 = np.sum(Z > Z[k0]); rank1 = np.sum(Z >= Z[k0]);

    return(rank0, rank1);


def stats_key_rank(n, nr, net, n_blocks, diff=(0x0, 0x0, 0x0, 0x0040)):
  r = np.zeros(n);
  for i in range(n):
    a,b = key_rank_one_round(nr, net, n_blocks=n_blocks, diff=diff);
    r[i] = randint(a,b);
  return(np.median(r), np.mean(r), r);

def test(k,n):
  for i in range(k,n):
    a,b,r = stats_key_rank(1000, 8, net6, n_blocks=2**i);
    np.save('./data_8r_attack/data_'+str(i)+'.npy',r);
    print(i,a,b);

test(5,8);

