#GFRX
import numpy as np
from os import urandom

def WORD_SIZE():
    return(16);


MASK_VAL = 2 ** WORD_SIZE() - 1;

c=2**WORD_SIZE() - 4;

z=[0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1];

def rol(x,k):
    return(((x << k) & MASK_VAL) | (x >> (WORD_SIZE() - k)));

def ror(x,k):
    return((x >> k) | ((x << (WORD_SIZE() - k)) & MASK_VAL));

def add(x,y):
    return((x + y) % MASK_VAL);

def minus(x,y):
    return((x - y) % MASK_VAL);

def f_and(x):
    return(rol(x,1)&rol(x,8)^rol(x,2));

def f_addl(x,y):
    return(add(ror(x,8),y));

def inv_f_addl(x,y):
    return(rol(minus(x,y),8));

def f_addr(y,z):
    return(rol(y,3)^z);

def inv_f_addr(x,y):
    return ror(x^y,3);

def f_add(x,y):
    return(f_addr(f_addl(x,y),y));

def enc_one_round(l0,l1,r0,r1, k0, k1, k2):
    s0=f_and(l1)^l0^k0;
    s1=f_addl(l1,r0)^k1;
    s2=f_addr(r0,s1);
    s3=f_and(r0)^r1^k2;
    return(s1,s3,s0,s2)

def dec_one_round(c0,c1,c2,c3, k0, k1, k2):
    s1=c0^k1; s3=c1; s0=c2; s2=c3;
    r0=ror((c0^s2),3);
    l1=rol(minus(s1,r0),8);
    l0=s0^k0^f_and(l1);
    r1=s3^k2^f_and(r0);
    return(l0,l1,r0,r1)

#ks = [0 for i in range(3*Nr)];
def expand_key(k, Nr):
    ks = [0 for i in range(3*Nr)];
    #k_l0||k_l1||k_l2||k_r0||k_r1||k_r2|| = k[0]||k[1]||k[2]||k[3]||k[4]||k[5]
    ks[0]=k[1]; ks[1]=k[3]; ks[2]=k[0];
    string_key= k[0]<<80|k[1]<<64|k[2]<<48|k[3]<<32|k[4]<<16|k[5];
    rotated_string_key=(string_key<<24 & (2 ** 96 - 1))|string_key>>72;
    k_l0=rotated_string_key>>80&MASK_VAL;
    k_l1=rotated_string_key>>64&MASK_VAL;
    k_l2=rotated_string_key>>48&MASK_VAL;
    k_r0=rotated_string_key>>32&MASK_VAL;
    k_r1=rotated_string_key>>16&MASK_VAL;
    k_r2=rotated_string_key&MASK_VAL;

    for i in range(Nr-1):
        k_l1=f_addl(k_l1,k_l0)^c^z[i];
        k_l0=f_addr(k_l0,k_l1);
        k_r0=f_and(k_r1)^k_r0^c^z[i];

        #k0:
        ks[3*(i+1)]=k_l1;
        #k1:
        ks[3*(i+1)+1]=k_r0;
        #k2:
        ks[3*(i+1)+2]=k_l0;

    return(ks);

#dec_ks=ks[::-1];

def encrypt(p, ks, Nr):
    l0, l1, r0, r1 = p[0], p[1], p[2], p[3];
    for i in range(Nr):
        l0, l1, r0, r1 = enc_one_round(l0, l1, r0, r1, ks[3*i],ks[3*i+1],ks[3*i+2]);
    return(l0, l1, r0, r1);


def decrypt(c, dec_ks, Nr):
    dec_ks=ks[::-1];
    l0, l1, r0, r1 = c[0], c[1], c[2], c[3];
    for i in range(Nr):
        l0, l1, r0, r1 = dec_one_round(l0, l1, r0, r1, dec_ks[3*i+2],dec_ks[3*i+1],dec_ks[3*i]);
    return(l0, l1, r0, r1);


# SINGLE CIPHERTEXT PAIR PER SAMPLE
import numpy as np

def convert_to_binary(arr):
    X = np.zeros((8 * WORD_SIZE(),len(arr[0])),dtype=np.uint8);
    for i in range(8 * WORD_SIZE()):
        index = i // WORD_SIZE();
        offset = WORD_SIZE() - (i % WORD_SIZE()) - 1;
        X[i] = (arr[index] >> offset) & 1;
    X = X.transpose();
    return(X);


def make_train_data(n, nr, diff=(0x0, 0x0, 0x0, 0x0040)):

  Y = np.frombuffer(urandom(n), dtype=np.uint8); Y = Y & 1;
  num_rand_samples = np.sum(Y==0);

  keys = np.frombuffer(urandom(12*1),dtype=np.uint16).reshape(6,-1).flatten();
  ks = expand_key(keys, nr);

  plain0l0 = np.frombuffer(urandom(2*n),dtype=np.uint16);
  plain0l1 = np.frombuffer(urandom(2*n),dtype=np.uint16);
  plain0r0 = np.frombuffer(urandom(2*n),dtype=np.uint16);
  plain0r1 = np.frombuffer(urandom(2*n),dtype=np.uint16);

  plain1l0 = plain0l0 ^ diff[0];
  plain1l1 = plain0l1 ^ diff[1];
  plain1r0 = plain0r0 ^ diff[2];
  plain1r1 = plain0r1 ^ diff[3];

  plain1l0[Y==0] = np.frombuffer(urandom(2*num_rand_samples),dtype=np.uint16);
  plain1l1[Y==0] = np.frombuffer(urandom(2*num_rand_samples),dtype=np.uint16);
  plain1r0[Y==0] = np.frombuffer(urandom(2*num_rand_samples),dtype=np.uint16);
  plain1r1[Y==0] = np.frombuffer(urandom(2*num_rand_samples),dtype=np.uint16);

  ctdata0l0, ctdata0l1, ctdata0r0, ctdata0r1 = encrypt((plain0l0, plain0l1, plain0r0, plain0r1), ks, nr);
  ctdata1l0, ctdata1l1, ctdata1r0, ctdata1r1 = encrypt((plain1l0, plain1l1, plain1r0, plain1r1), ks, nr);

  X = convert_to_binary([ctdata0l0, ctdata0l1, ctdata0r0, ctdata0r1, ctdata1l0, ctdata1l1, ctdata1r0, ctdata1r1]);
  return(X,Y);