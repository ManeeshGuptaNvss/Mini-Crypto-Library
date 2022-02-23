G=13
P=47
SEEDSIZE=16

def dec_to_bin(x):
    return bin(x).replace('0b','')

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

def prg(x):
    output=""
    for i in range(2*SEEDSIZE):
        g_of_x=function_G(x)
        output+=g_of_x[-1]
        x=g_of_x[:-1]
        # print("x",x)
    return output
    

# print(function_G('1000'))
# print(function_G('100'))
# print(function_G('10'))
# print(prg(dec_to_bin(2)))
# print(prg(dec_to_bin(13)))

# fk('011')=
def prf(k,x):
    # str_x=dec_to_bin(x)
    prg_input=k
    for i in x:
        prg_output=prg(prg_input)
        if(i=='0'):
            prg_input=prg_output[:len(prg_output)//2]
        else:
            prg_input=prg_output[len(prg_output)//2:]
        print(prg_output,prg_input)
    return prg_output        

print(prf('101','110'))  
