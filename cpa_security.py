from prf import prf
from utils import rand_key,SEEDSIZE,xor_operation,change_m

iv=rand_key(SEEDSIZE)
# m=rand_key(4*SEEDSIZE)

k=rand_key(SEEDSIZE)



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

if __name__=="__main__":
    m=input()
    print(m,len(m))
    m=change_m(m, iv)
    print(m,len(m))
    cipher_text=output_feedback_encrypt(iv,m,k)  
    plain_text=output_feedback_decrypt(iv, cipher_text,k)
    print(verify(plain_text, m))
