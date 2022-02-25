from utils import dec_to_bin,rand_key,SEEDSIZE,xor_operation
from cpa_security import cpa_secure
from prf import prf
m=rand_key(4*SEEDSIZE)
block_length=SEEDSIZE
x=rand_key(SEEDSIZE)
iv=rand_key(SEEDSIZE)

def cbc_mac(m,block_length,x):
    msg_length=len(m)
    no_of_blocks=msg_length//block_length
    iv=bin(msg_length).replace('0b', '')
    iv_length=len(iv)
    while iv_length <block_length:
        iv='0'+iv
        iv_length+=1
    # print(iv,iv_length)
    prf_input=prf(iv,x)
    for i in range(no_of_blocks):
        msg_i=m[i*block_length:(i+1)*block_length]
        xor_value=xor_operation(prf_input,msg_i)
        prf_input=prf(xor_value,x)
    return prf_input
        
def cca_secure(m,iv,block_length,x):
    cpa_output=cpa_secure(iv, m)
    cbc_mac_value=cbc_mac(cpa_output,block_length,x)
    return cpa_output+cbc_mac_value

def verify_mac(text,mac_length,x):
    mac_output=cbc_mac(text[:-1*mac_length],mac_length,x)
    text_mac=text[-1*mac_length:]
    return mac_output==text_mac

if __name__=="__main__":
    print(cbc_mac(m, block_length,x))
    cca_output=cca_secure(m,iv,block_length,x)
    print(verify_mac(cca_output, block_length, x))