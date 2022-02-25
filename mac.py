from utils import dec_to_bin,rand_key,SEEDSIZE,xor_operation,change_m
from cpa_security import cpa_secure
from prf import prf
# m=rand_key(4*SEEDSIZE)

block_length=SEEDSIZE
k=rand_key(SEEDSIZE)
iv=rand_key(SEEDSIZE)

def cbc_mac(m,block_length,k):
    msg_length=len(m)
    no_of_blocks=msg_length//block_length
    prepend=bin(msg_length).replace('0b', '').zfill(block_length)
    m=prepend+m
    iv=''.zfill(block_length)
    # iv_length=len(iv)
    # while iv_length <block_length:
    #     iv='0'+iv
    #     iv_length+=1
    # print(iv,iv_length)
    # prf_input=prf(iv,x)
    for i in range(no_of_blocks):
        msg_i=m[i*block_length:(i+1)*block_length]
        xor_value=xor_operation(iv,msg_i)
        prf_input=prf(k,xor_value)
    return prf_input
        
def cca_secure(m,iv,block_length,k):
    cpa_output=cpa_secure(iv, m,k)
    cbc_mac_value=cbc_mac(cpa_output,block_length,k)
    return cpa_output+cbc_mac_value

def verify_mac(text,mac_length,k):
    mac_output=cbc_mac(text[:-1*mac_length],mac_length,k)
    text_mac=text[-1*mac_length:]
    return mac_output==text_mac

if __name__=="__main__":
    m=input("enter msg: ")
    # here k is sent only for length purpose
    m=change_m(m,k) 
    print(cbc_mac(m, block_length,k))
    cca_output=cca_secure(m,iv,block_length,k)
    print(verify_mac(cca_output, block_length,k))