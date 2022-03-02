from prg import prg

''' 
Input: x,k
Output: len(k)
'''



def prf(k,x):
    # str_x=dec_to_bin(x)
    prg_input=k
    for i in x:
        prg_output=prg(prg_input)
        # print('G(K)',i)
        if(i=='0'):
            prg_input=prg_output[:len(prg_output)//2]
        else:
            prg_input=prg_output[len(prg_output)//2:]
        # print(prg_output,prg_input)
    return prg_input       

if __name__=="__main__":
    print(prf('101','110')) 