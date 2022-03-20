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
    return output
    
def prf(k,x):
    prg_input=k
    for i in x:
        prg_output=prg(prg_input,2*len(prg_input))
        if(i=='0'):
            prg_input=prg_output[:len(prg_output)//2]
        else:
            prg_input=prg_output[len(prg_output)//2:]
    return prg_input       

def rand_key(n):
    key1=""
    for i in range(n):
        temp = str(random.randint(0, 1))
        key1 += temp
    return(key1)


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
    cipher_text=""
    for i in range(no_of_blocks):
        m_i=m[block_length*i:block_length*(i+1)]
        iv=prf(k,iv)
        cipher_text+=xor_operation(iv,m_i)
    print("cipher text",cipher_text)    
    return cipher_text
    
   
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
        print("XOR_Value:",xor_value)
        iv=prf(k,xor_value)
        print("NEW IV:",iv)
    return iv
        
if __name__=="__main__":
    m=input("enter msg: ")
    # here k is sent only for length purpose
    k=input("Enter k in 16-bits:")
    m=change_m(m,k)     
    iv=input("Enter an iv in 16-bits:")
    block_length=len(k)
    print(cbc_mac(m, block_length,k))
