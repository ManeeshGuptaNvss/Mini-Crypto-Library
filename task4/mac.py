import random
SEEDSIZE=16
G=3
H=7
P=43649
def dec_to_bin(x):
    return bin(x).replace('0b','')
def hardcore_predicate(s):
    # returning the MSB
    # return s[0]
    int_s=int(s,2)
    if(int_s<P/2):
        return '0'
    else:
        return '1'
    
def xor_operation(x,y):
    ''' input: x-binary string, y-binary string
        output: res-binary string '''
    res=""
    if(len(x)!=len(y)):
        print("xor-->lengths are not same")
    length=min(len(x),len(y))
    for i in range(length):
        if(x[i]==y[i]):
            res+='0'
        else:
            res+='1'
    return res

def one_way_function(x):
    int_x=int(x,2)
    
    #discrete logarithm
    val= pow(G, int_x ,P)
    return dec_to_bin(val)

def function_G(x):
    hcp=hardcore_predicate(x)
    val=one_way_function(x)
    return val+hcp

def prg(x,length=SEEDSIZE):
    output=""
    for i in range(length):
        g_of_x=function_G(x)
        output+=g_of_x[-1]
        x=g_of_x[:-1]
        # print("x",x)
    return output
    
''' 
Input: x,k
Output: len(k)
'''
def prf(k,x):
    # str_x=dec_to_bin(x)
    prg_input=k
    for i in x:
        prg_output=prg(prg_input,2*len(prg_input))
        # print('G(K)',i)
        if(i=='0'):
            prg_input=prg_output[:len(prg_output)//2]
        else:
            prg_input=prg_output[len(prg_output)//2:]
        # print(prg_output,prg_input)
    return prg_input       

def rand_key(n):
    key1=""
    for i in range(n):
        temp = str(random.randint(0, 1))
        key1 += temp
    return(key1)

iv=rand_key(SEEDSIZE)
# m=rand_key(4*SEEDSIZE)

k=rand_key(SEEDSIZE)

def change_m(msg,iv):
    msg_len=len(msg)
    iv_len=len(iv)
    remainder=msg_len%iv_len
    if remainder!=0:
        msg=msg.zfill(msg_len+(iv_len-remainder))
    return msg


# one encryptor, one decryptor
def output_feedback_encrypt(iv,m,k):
    no_of_blocks=len(m)//len(iv)
    block_length=len(iv)
    # iv_int=int(iv,2)
    cipher_text=""
    for i in range(no_of_blocks):
        m_i=m[block_length*i:block_length*(i+1)]
        # print(m_i,x)
        # m_i_int=int(m_i,2)
        iv=prf(k,iv)
        cipher_text+=xor_operation(iv,m_i)
    print("cipher text",cipher_text)    
    return cipher_text
        # prf(k,prf_input)

   
def output_feedback_decrypt(iv,cipher,k):
    no_of_blocks=len(cipher)//len(iv)
    block_length=len(iv)
    plain_text=""
    for i in range(no_of_blocks):
        iv=prf(k,iv)
        cipher_i=cipher[block_length*i:block_length*(i+1)]
        plain_text+=xor_operation(cipher_i, iv)
    print("plain text after decryption:",plain_text)
    return plain_text

def verify(plain_text,m):
    return plain_text==m

def cpa_secure(iv,m,k):
    return iv+output_feedback_encrypt(iv, m,k)

block_length=SEEDSIZE
k=rand_key(SEEDSIZE)
iv=rand_key(SEEDSIZE)

# task 4
def cbc_mac(m,block_length,k):
    msg_length=len(m)
    no_of_blocks=msg_length//block_length
    prepend=bin(msg_length).replace('0b', '').zfill(block_length)
    m=prepend+m
    iv=''.zfill(block_length)
    for i in range(no_of_blocks):
        msg_i=m[i*block_length:(i+1)*block_length]
        xor_value=xor_operation(iv,msg_i)
        prf_input=prf(k,xor_value)
    return prf_input
        
if __name__=="__main__":
    m=input("enter msg: ")
    # here k is sent only for length purpose
    m=change_m(m,k)     
    block_length=len(k)
    print(cbc_mac(m, block_length,k))
    # cca_output=cca_secure(m,iv,block_length,k)
    # print(verify_mac(cca_output, block_length,k))