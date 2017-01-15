# -*-coding:utf8-*-
"""
Modul som kan brukes til å lage autogenererte
oppgaver og løsningsforslag for studenter
som trener på gauss-eliminasjon.
"""

import random
from sympy import *

RANGE = 3;
N = 3

def relem():
    return S(random.randint(-RANGE,RANGE))

def output(obj):
    return latex(obj)

def makeRandomSystem():
    A = Matrix([relem() for i in range(N*(N+1))])
    A = A.reshape(N,N+1)
    x = Matrix([relem() for i in range(N)])
    A[:,N] = A[:,0:N]*x
    return A,x



def gaussElimination(A):
    global out
    out =  "$$\n"+ output(A)+"\n$$\n$$"
    n = A.shape[0]
    def swap(i,k):
        global out
        tmp = A[i,:]
        A[i,:] = A[k,:]
        A[k,:] = tmp
        out += "\\sim" + output(A)

    def prepare(i):
        k = i
        while (k <n and A[k,i] == 0):
            k+=1
        if k >= n:
            return False
        elif i != k:
            swap(i,k);
        return True

    for i in range(n):
        if i%2 == 0 and i != 0:
            out += "$$"
        if not prepare(i):
            return ""
        for j in range(n):
            if j == i:
                continue
            A[j,:] = A[j,:] - A[i,:]*A[j,i]/A[i,i]
        A[i,:] /= A[i,i]
        out+= "\n\\sim"+  output(A)
        if i%2 == 1 and i != n-1:
            out+= "$$"
    out += "$$\n"
    return out


def printAsEquation(A):
    
    def printAsFirst(i,j):
        if A[i,j] == 1:
            return "x_"+str(j+1)+ "&"
        elif A[i,j] == -1:
            return "-x_"+str(j+1)+"&"
        elif A[i,j] != 0 :
            return latex(A[i,j])+"x_"+str(j+1)+"&"
        return "&";

    def printNormal(i,j):
        if A[i,j] == 1:
            return "+& x_{"+str(j+1)+ "}&"
        elif A[i,j] == -1:
            return "-& x_{"+str(j+1)+"}&"
        elif A[i,j] > 0:
            return "+&"+latex(A[i,j])+"x_{"+str(j+1)+"}&"
        elif A[i,j]<0:
            return "-&"+latex(-A[i,j])+"x_{"+str(j+1)+"}&"
        else:
            return "&&"

    n = A.shape[0]
    out = "\\begin{matrix}\n"
    for i in range(n):
        first = True
        for j in range(0,n):
            if (first):
                out += printAsFirst(i,j)
                first = False
            else:
                out+=printNormal(i,j)
        out += "=& "+latex(A[i,n]) +"\\\\\n"
    out+="\\end{matrix}"
    return out;
     

def printSolution(x):
    output = ""
    for i in range(len(x)-1):
        output += "x_{"+str(i+1)+"} = "+latex(x[i])+"\\quad "
    output += "x_{"+str(len(x))+"} = "+latex(x[-1])
    return output
        

def generateExercise():
    gauss = ""
    while (gauss==""):
        A,x = makeRandomSystem();
        output = "QUESTION\nLøs ligningsystemet\n$$\n"+printAsEquation(A)+"\n$$\nSOLUTION\nSystemet løses ved radoperasjoner på koeffesientmatrisen:\n"
        gauss = gaussElimination(A)
        output += gauss+"\nDermed har vi løsningen $$"+printSolution(x)+"$$."
    return output

if __name__=="__main__":
    N=3
    A,x = makeRandomSystem();
    pprint(A)
    print gaussElimination(A)



