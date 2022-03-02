G=13
P=47
SEEDSIZE=16
import random


def dec_to_bin(x):
    return bin(x).replace('0b','')

def rand_key(n):
    key1=""
    for i in range(n):
         
        # randint function to generate
        # 0, 1 randomly and converting
        # the result into str
        temp = str(random.randint(0, 1))
        # Concatenation the random 0, 1
        # to the final result
        key1 += temp
    return(key1)

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

def change_m(msg,iv):
    msg_len=len(msg)
    iv_len=len(iv)
    remainder=msg_len%iv_len
    if remainder!=0:
        msg=msg.zfill(msg_len+(iv_len-remainder))
    return msg

def hardcore_predicate(s):
    # returning the MSB
    # return s[0]
    res=0
    for i in range(len(s)):
        res^=ord(s[i])-ord('0')
    return str(res)

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
    iv=rand_key(SEEDSIZE)
    k=rand_key(SEEDSIZE)    
    block_length=SEEDSIZE
    # print(xor_operation("1010","0000"))
    # print(prf('101','110'))
    
    # cpa secure
    # m=input()
    # print(m,len(m))
    # m=change_m(m, iv)
    # print(m,len(m))
    # cipher_text=output_feedback_encrypt(iv,m,k)  
    # plain_text=output_feedback_decrypt(iv, cipher_text,k)
    # print(verify(plain_text, m))
    
    
    # cca secure
    m=input("enter msg: ")
    # here k is sent only for length purpose
    m=change_m(m,k) 
    print(cbc_mac(m, block_length,k))
    cca_output=cca_secure(m,iv,block_length,k)
    print(verify_mac(cca_output, block_length,k))