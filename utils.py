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

if __name__=="__main__":
    print(xor_operation("1010","0000"))