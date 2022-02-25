from utils import dec_to_bin,SEEDSIZE,G,P
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
    

# print(function_G('1000'))
# print(function_G('100'))
# print(function_G('10'))
if __name__=="__main__":
    print(prg(dec_to_bin(2)))
    print(prg(dec_to_bin(13)))
# fk('011')=
 