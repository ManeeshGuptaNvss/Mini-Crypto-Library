import random
G=3
H=7
P=43649
# n is the number of bits in P
n=len(bin(P).replace('0b', ''))
SEEDSIZE=16
# task 1
def dec_to_bin(x):
    return bin(x).replace('0b','')

def rand_key(n):
    key1=""
    for i in range(n):
        temp = str(random.randint(0, 1))
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
# task 2
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

# task 3
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

# task 4
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
# task 6
def fixed_hash(x1,x2):
    x1_int=int(x1,2);x2_int=int(x2,2)
    res1=pow(G,x1_int,P)
    res2=pow(H,x2_int,P)
    result=(res1*res2)%P
    result_bin=dec_to_bin(result)
    result_bin=result_bin.zfill(n)
    print("f_hash:",result_bin)
    return result_bin
# task 7
iv='0'*n
def var_hash(msg,iv):
    block_size=n
    len_msg=len(msg)
    len_msg_block=dec_to_bin(len_msg).zfill(block_size)
    extra=len_msg%block_length
    msg=msg.zfill(len_msg+extra)
    msg=msg+len_msg_block
    no_of_blocks=len(msg)//block_size
    for i in range(no_of_blocks):
        input_block=msg[i*block_size:(i+1)*block_size]
        iv=fixed_hash(iv,input_block)
    return iv
# task 8
def hmac(msg,k):
    k=k.zfill(n)
    ipad=bin(0x5c).replace('0b','').zfill(8)
    opad=bin(0x36).replace('0b','').zfill(8)  
    ipad=ipad*(n//8)
    opad=opad*(n//8)
    k_xor_ipad=xor_operation(k, ipad)
    k_xor_opad=xor_operation(k, opad)
    iv='0'*n
    output_fixed_hash_ipad=fixed_hash(k_xor_ipad, iv)
    output_fixed_hash_opad=fixed_hash(k_xor_opad, iv)
    output_var_hash=var_hash(msg, output_fixed_hash_ipad)
    hmac_val=fixed_hash(output_var_hash, output_fixed_hash_opad)
    return hmac_val

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
    # m=input("enter msg: ")
    # # here k is sent only for length purpose
    # m=change_m(m,k) 
    # print(cbc_mac(m, block_length,k))
    # cca_output=cca_secure(m,iv,block_length,k)
    # print(verify_mac(cca_output, block_length,k))
    
    # hmac
    # print(fixed_hash('1010111101010101', '1011011101110110'))
    msg=input("enter msg: ")
    # print(var_hash(msg))
    print(hmac(msg, '101010'))