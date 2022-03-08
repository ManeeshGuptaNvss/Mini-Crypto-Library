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
    

if __name__=="__main__":
    x=int(input("enter initial seed:"))
    print("PRG:",prg(dec_to_bin(x)))
 