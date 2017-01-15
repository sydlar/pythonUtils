import numpy,math,sympy
from numpy  import linalg as la



class Quaternion(numpy.ndarray):
        
        symbols = ["","i","j","k"]

	def __new__(cls,args):
            if len(args) != 4:
                raise ValueError("A quaternion needs 4 components. You supplied "+str(len(args))+" components.")
            return numpy.asarray(args).view(cls)



	def __mul__(self,other):
            try:
		w = self[0]*other[0] - self[1]*other[1]-self[2]*other[2]-self[3]*other[3]
		x = self[0]*other[1]+self[1]*other[0] + self[2]*other[3] - self[3]*other[2] 
		y = self[0]*other[2]+self[2]*other[0] + self[3]*other[1] - self[1]*other[3] 
		z = self[0]*other[3]+self[3]*other[0] + self[1]*other[2] - self[2]*other[1] 
		return Quaternion([w,x,y,z])
            except:
                return self*Quaternion([other,0,0,0])

        def __eq__(self,other):
            if type(other) != type(self):
                return False

            for i in range(3):
                if self[i] != other[i]:
                    return False
            return True

	def conjugate(self):
		return Quaternion([self[0],-self[1],-self[2],-self[3]])

        def __str__(self):
            output = str(self[0])
            for i in range(1,4):
                if (self[i] != 0):
                    output += " + "+str(self[i])+" "+self.symbols[i]
            return output

        def __repr__(self):
            output = str(self[0])
            for i in range(1,4):
                if (self[i] != 0):
                    output += " + "+str(self[i])+" "+self.symbols[i]
            return output

        def vectorPart(self):
            return numpy.array([self[i] for i in range(1,4)])

        def latex(self,delim):
            output = r'\begin{bmatrix}'+str(self[0])
            for i in range(1,4):
                output += delim +str(self[i])
            output += r'\end{bmatrix}'
            return output

        def latexRow(self):
            return self.latex(r' & ')

        def latexColumn(self):
            return self.latex(r' \\ ')

        def norm(self):
            return sympy.sqrt(self.dot(self))

def norm(vector):
    return sympy.sqrt(sum(x*x for x in vector))

def quaternion(w,x,y,z):
	return Quaternion([w,x,y,z])


def rotMatrix(theta):
    """
    Based on matrix multiplication FROM THE RIGHT!
    """
    return numpy.matrix([[sympy.cos(theta),sympy.sin(theta)],[-sympy.sin(theta),sympy.cos(theta)]])

def euler2matrix(h,p,b):
	A = [numpy.eye(3) for i in range(3)]
	V = [rotMatrix(b),rotMatrix(p),rotMatrix(h)]
	for i in range(3):
		for j in range(2):
			for k in range(2):
				A[i][(i+j)%3,(i+k)%3] = V[i][j,k]
	return reduce(lambda x,y:x.dot(y), A)

def quaternion2matrix(q,module=sympy):
    I = module.eye(4)
    output = module.zeros(3,3)
    qAst = q.conjugate()
    for i in range(3):
        print output
        ei = Quaternion(I[:,i+1])
        print I[:,i+1] 
        result = q*ei*qAst
        print result
        for j in range(3):
            print i
            output[j,i] = result[j+1]
    return output

def matrix2euler(m):
    p = math.asin(-m[2,1])
    h = math.atan2(m[2,0],m[2,2])
    b = math.atan2(m[0,1],m[1,1])
    return h,p,b

def qlog(q):
    w = q[0]
    vectorPart = q.vectorPart();
    vnorm = norm(vectorPart)
    angle = math.atan2(vnorm,w)

    return (2*angle/vnorm)*vectorPart

quaternion2vector = qlog

def qexp(e):
    vnorm = norm(e)
    vectorPart = (math.sin(vnorm/2)/vnorm) * e
    w = math.cos(vnorm/2)
    (x,y,z) = (vectorPart[i] for i in range(3))
    return quaternion(w,x,y,z)

vector2quaternion = qexp

def quaternion2axisAngle(q):
    vector = q.vectorPart();
    vnorm = norm(vector)
    qnorm = norm(q)
    
    w = q[0]/qnorm
    angle = 2*sympy.acos(w)
    return angle, vector/vnorm

def crossProduct(a,b):
    c = sympy.Matrix([0,0,0]) 
    for i in range(3):
            c[i] += a[(i+1)%3] * b[(i+2)%3]
            c[i] -= a[(i+2)%3] * b[(i+1)%3]
    return c

def scalarProduct(a,b):
    return sum((x*y for (x,y) in zip(a,b)))

def angle(a,b,module=sympy):
    return module.acos(scalarProduct(a,b)/norm(a)/norm(b))

q1 = quaternion(1,0,0,0)
qi = quaternion(0,1,0,0)
qj = quaternion(0,0,1,0)
qk = quaternion(0,0,0,1)


def rhp2xyz(r,h,p,module=math):
    return [r*module.cos(p)*module.sin(h),-r*module.sin(p),r*module.cos(p)*module.cos(h)]

def xyz2rhp(x,y,z,module=math):
    r = module.sqrt(x**2+y**2+z**2)
    p = module.asin(-y/r)
    h = module.atan2(x,z)
    return [r,h,p]



if __name__=="__main__":
    for el in  rotMatrix(0.5*math.pi):
        for e in el:
            print e

    from sympy import Matrix
    print angle(Matrix([3,4,5]),Matrix([2,3,4]))
    print(rhp2xyz(1,2,1))
