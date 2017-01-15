# -*-coding:utf8-*-
"""
Modul som definerer funksjoner som kommer til nytte når man bruker
python-skript til å generere latex-kode, f.eks. i forbindelse 
med produksjon av matteoppgaver.

Når man kombinerer dette med pythontex, kan man f.eks. få autogenererte
matplotlib-plot direkte inn i latex-dokumentet.
"""


from sympy import latex
import os

import matplotlib
matplotlib.use('pgf')
pgf_with_pdflatex = {"pgf.texsystem": "pdflatex","font.size":8,"font.family":"serif"}
matplotlib.rcParams.update(pgf_with_pdflatex)

personalSettings = {
        'axes.linewidth' :0.2,
        'xtick.minor.size' : 1.5,
        'ytick.minor.size' : 1.5,
        'ytick.minor.width' : 0.2,
        'ytick.minor.width' : 0.2,
        'xtick.major.size' : 2.5,
        'ytick.major.size' : 2.5,
        'ytick.major.width' : 0.2,
        'ytick.major.width' : 0.2,
        'lines.linewidth' : 0.5,
        'lines.color' : 'red',
        'lines.markersize': 2,
        'lines.antialiased': True,
        }
matplotlib.rcParams.update(personalSettings)

from matplotlib import pyplot

#
# CONSTANTS
#
NUMBER_OF_DECIMALS = 2
FIGNUM = 0
PNUM = 0
PID = os.getpid()
FIGDIR = "pyfigs"

def rnd(x):
    try:
        return round(x,NUMBER_OF_DECIMALS)
    except:
        return x

def beginEquation(option=None):
    if option == 'inl':
        print '$'
    elif option == 'num':
        print r'\begin{equation}'
    else:
        print '$$'

def endEquation(option=None):
    if option == 'inl':
        print '$'
    elif option == 'num':
        print r'\end{equation}'
    else:
        print '$$'


def asColumn(vector,applyFunc = rnd):
    return asVector(vector,r' \\ ',applyFunc = applyFunc)

def asRow(vector,applyFunc = rnd):
    return asVector(vector,r' & ',applyFunc = applyFunc)

def asVector(vector,separator,applyFunc = rnd):
    out = '\\begin{bmatrix}\n' + asList(vector,separator,applyFunc = applyFunc) + '\n\\end{bmatrix}'
    return out

def asMatrix(matrix,applyFunc = rnd):
    out = '\\begin{bmatrix}\n'
    for row in matrix:
        out += asList(row,r' & ',applyFunc = applyFunc) + ' \\\\\n'
    out += '\\end{bmatrix}'
    return out

def asList(vector,separator,applyFunc = rnd):
    function =  applyFunc if applyFunc  else lambda x : x
    return separator.join(map(lambda x : str(function(x)),vector))

def asPoint(point,applyFunc = rnd):
    return r'\left( '+asList(point,",",applyFunc = applyFunc)+r' \right) '


def asTikzPoint(point,name=None,ID=None):
    global PNUM
    PNUM = PNUM+1
    ID = ID or PNUM
    name = name or str(ID)
    return r'\node ({0}) at ({1},{2}) {{}};\filldraw ({0}.center) circle (1pt);\node[above] at ({0}) {{${0}$}};'.format(name,point[0],point[1])

def asTikzVector(components,source=(0,0),name=None):
    name = name and r'${}$'.format(name) or ""
    return r'\draw[-latex] ({0},{1}) --node[sloped,above] {{{4}}} ({2},{3});'.format(source[0],source[1],components[0]+source[0],components[1]+source[1],name)

def latexPrecision(n):
    global NUMBER_OF_DECIMALS
    NUMBER_OF_DECIMALS = n

def asLinearSystem(A,labels = False ):
    n = A.shape[0]
    lab = labels if labels else ["x_"+str(i) for i in range(1,n+1)]

    def printAsFirst(i,j):
        if A[i,j] == 1:
            return lab[j]+ "&&"
        elif A[i,j] == -1:
            return r'\;-\;'+lab[j]+"&&"
        elif A[i,j] != 0 :
            return latex(A[i,j])+r'\,'+lab[j]+"&&"
        return "&&";

    def printNormal(i,j):
        if A[i,j] == 1:
            return r'\;+\;&'+lab[j]+ "&"
        elif A[i,j] == -1:
            return r'\;-\;&'+lab[j]+"&"
        elif A[i,j] > 0:
            return r'\;+\;&'+latex(A[i,j])+r'\,'+lab[j]+"&"
        elif A[i,j]<0:
            return r'\;-\;&'+latex(-A[i,j])+r'\,'+lab[j]+"&"
        else:
            return "&&"

    out = "\\begin{alignat*}{"+str(2*(n+1))+"}"
    for i in range(n):
        first = True
        out += printAsFirst(i,0)
        for j in range(1,n):
            out+=printNormal(i,j)
        out += "\;= &\;"+latex(A[i,n]) +"\\\\\n"
    out+="\\end{alignat*}"
    return out;


def includeFigure(name=None,plotter=pyplot):
    global FIGNUM

    if(not name):
        FIGNUM += 1
        pgfPath = FIGDIR+"/figure"+str(FIGNUM)+"_"+str(PID)+".pgf"
    else:
        pgfPath = FIGDIR+"/"+name+".pgf"
    
    try:
        os.mkdir(FIGDIR)
    except OSError as e:
        pass


    plotter.savefig(pgfPath)
    print r'\begin{center}\input{'+pgfPath+r'}\end{center}'


def tabular(data,heading,adjustment='c'):
    
    n = len(heading)

    adj = adjustment*n
    
    out = r'\begin{tabular}{'+adj+'}\n\\toprule\n'
    out += "&".join(map(str,heading)) + '\\\\\n\midrule\n'
    out +='\\\\\n'.join(map(' & '.join,(map(str,line) for line in data)))
    out +='\\\\\n\\bottomrule\n\end{tabular}'
    return out

def printDict(symbolTable):
    return tabular(symbolTable.items(),["Key","Value"],"l")

#
# Main
#########################
if __name__=="__main__":
    import math

    print asColumn([2,1.0/3],applyFunc = lambda x : x**23)
    print asRow([2,1.0/3],applyFunc = lambda x : 0.0)
    latexPrecision(4)
    print asPoint([3,1,4],applyFunc = lambda x : rnd(math.sin(x)))
    latexPrecision(10)
    print asMatrix([[2,1.0/3],[3,4]])
    print tabular([[2,3,4],[3,4,5]],["a","b","c"])
