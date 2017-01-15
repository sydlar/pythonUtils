# -*- coding:utf8 -*-
"""
(Skrevet ca. 2010)

Modul som kan være nyttig ved arbeid med uendelige
rekker.

series-objektene representerer uendelige rekker, utregnet ved "lazy" evaluering.
D.v.s. at koeffesienter regnes ut først når vi spør etter dem. 

Modulen er laget for egen bruk i forbindelse med arbeid med rekkeutviklinger for 
ulike størrelser som dukker opp når man studerer trelegemeproblemet.

Det er kanskje ikke nødvendig å nevne at jeg hadde klart meg fint med å studere kun 
de 4-5 første leddene. Men, det var nå en vakker tanke da, at jeg faktisk hadde 
uendelige rekker for hånden. 

Man kan vel også legge til at beregningskompleksiteten for ledd av høyere orden gjør 
at mange av disse såkalt uendelige rekkene for alle praktiske formål er svært endelige.

MERK: Pr. i dag (2017) håper jeg at jeg hadde skrevet dette på en annen måte. En tanke ville
være å legge seg tettere opp til hvordan generatorer og iteratorer vanligvis behandles
i python, d.v.s. å gjøre det på en mer idiomatisk mpte, og samtidig unngå overforbruk av 
"magiske" funksjoner gom "__getattr__" o.l.
"""

from __future__ import division
import user 
from sympy import Symbol,S,Rational,oo,log

class series(object):
	def __init__(self,coeff=lambda n:0,**kwargs):
		#Coefficients
		self.coeff=coeff
		#Special coefficients:
		if kwargs.has_key('coeffList'):
			self.coeffList=kwargs['coeffList']
		else:
			self.coeffList=None
		#Variable
		if kwargs.has_key('var'):
			var=kwargs['var']
			if isinstance(var,str):
				var=Symbol(var)
			self.var=var
		else:
			self.var=Symbol('x')
		#Number of terms in string representations
		if kwargs.has_key('N'):
			self.N=kwargs['N']
		else:
			self.N=4
		#Upper bound for some iterations, including computation of degree and order
		if kwargs.has_key('UB'):
			self.UB=kwargs['UB']
		else:
			self.UB=self.N
		
		if kwargs.has_key('LB'):
			self.LB=kwargs['LB']
		else:
			self.LB=-5
		
		if kwargs.has_key('ord'):
			ord=kwargs['ord']
			self.ord=ord
			if not ord==oo:
				self.LB=ord
		
		if kwargs.has_key('deg'):
			deg=kwargs['deg']
			self.deg=deg
			if deg<self.UB:
				self.UB=deg
		
		self.doLevel=self.LB
		
		if kwargs.has_key('nicePrint'):
			self.nicePrint=kwargs['nicePrint']
		else:
			self.nicePrint=None
		if kwargs.has_key('powerCoeff'):
			self.powerCoeff=kwargs['powerCoeff']
		else:
			self.powerCoeff=None

	def __getattr__(self,navn):
		if navn=='ord':
			ord=self.LB
			while 1:
				if self[ord]:
					break
				else:
					ord+=1
				if ord > self.UB:
						break
						ord=oo
						self.deg=0
			self.LB=ord
			return ord
		
		if navn=='deg':
			#This gives the corret degree for polynomials with degree less than self.UB and greater thatn self.LB
			numZeros=4
			ord=self.ord
			if ord==oo:
				self.deg=0
				return 0
			deg=oo
			if self.UB==oo:
				self.UB=7
			for i in range(self.LB,self.UB+numZeros+1):
				if self[i]:
					deg=i
			if self.UB-deg>0:
				self.UB=deg
				self.deg=deg
				return deg
			else:
				self.deg=oo
				return oo
		
		if navn=='is_poly':
			if self.deg==oo or self.ord<0:
				return False
			else:
				self.N=self.deg
				return True
	
	def __repr__(self):
		return 'Potensrekke i variabelen '+str(self.var)+'.'
	
	def __str__(self):
		if not self:
			return str(0)
		elif self.nicePrint:
			def coeffStr(i):
				string=str(self[i])
				if len(string)>3:
					return '['+string+'] '
				if string=='0':
					return ''
				return string+' '
			
			def powerStr(i):
				if i==0:
					return ''
				elif i==1:
					return str(self.var)
				elif i<=self.deg:
					return str(self.var)+'**'+str(i)
				else:
					return ''
			
			def connectStr(i):
				if (not self[i]) or i>=self.deg:
					return ''
				if i>=self.deg or i>self.ord+self.N:
					return ''
				return '  +  '
			
			def termStr(i):
				if not self[i]:
					return ''
				if i>self.deg:
					return ''
				if i<=self.ord+self.N or i==self.N+1==self.deg:
					return coeffStr(i)+powerStr(i)
				if i==self.ord+self.N+1:
					return 'O('+powerStr(i)+')'
			ret=''
			for i in range(self.ord,self.ord+self.N+2):
				ret+=termStr(i)+connectStr(i)
		
		else:
			def coeffStr(i):
				string=str(self[i])
				if len(string)>3:
					return '['+string+'] '
				else:
					return string+' '
			
			def powerStr(i):
				if i==0:
					return ''
				elif i==1:
					return str(self.var)
				else:
					return str(self.var)+'**'+str(i)

			def connectStr(i):
				if not self[i] or i==self.N+1:
					return ''
				else:
					return '  +  '
			
			def termStr(i):
				if i==self.N+1:
					return 'O('+powerStr(i)+')'
				if not self[i]:
					return ''
				else:
					return coeffStr(i)+powerStr(i)
				
				if i==self.ord+self.N+1:
					return 'O('+powerStr(i)+')'
			ret=''
			for i in range(self.ord,self.N+2):
				ret+=termStr(i)+connectStr(i)
		
		return ret
	
	def __getitem__(self,i):
		if self.coeffList:
			if self.coeffList.has_key(i):
				return self.coeffList[i]
			else:
				ret=self.coeff(i)
				self.coeffList[i]=ret
				return ret
		else:
			ret=self.coeff(i)
			self.coeffList={i:ret}
		return ret
	
	def __setitem__(self,i,value):
		if self.__dict__.has_key('ord'):
			if value==0 and i==self.ord:
				del self.ord
			elif i<self.ord and not value==0:
				self.ord=i
		if self.__dict__.has_key('deg'):
			if value==0 and i==self.deg:
				del self.deg
			elif i>self.deg and not value==0:
				self.deg=i
		if self.coeffList:
			self.coeffList[i]=value
		else:
			self.coeffList={i:value}
	
	def __call__(self,p):
		if p==self.var:
			return self
		elif isinstance(p,Symbol):
			ret=self.copy()
			ret.var=p
			return ret
		#Preprosessering av inndata
		aux1=self
		if isinstance(p,series):
			aux2=p
		elif isinstance(p,tuple):
			try:
				aux2=expr2series(p[0],p[1])
			except:
				return None
		else:
			aux1,aux2=coerce(self,p)
		#Test av hvorvidt substitusjonen er implementert
		if (not aux1.ord>=0) or (not aux2.ord>0):
			raise NotImplementedError('We cannot yet substitute such series')
		#Selve substitusjonen:
		def retCoeff(n):
			if n==0:
				return aux1[0]
			ret=0
			for i in range(1,n+1):
				ret+=aux1[i]*aux2.getPowerCoeff((n,i))
			return ret
		return series(retCoeff,var=aux2.var,ord=aux1.ord*aux2.ord,deg=aux1.deg*aux2.deg)
		
		
	def __nonzero__(self):
		if self.ord==oo:
			return False
		else:
			return True
	
	def doit(self,doLevel,**kwargs):
		if kwargs.has_key('simplify'):
			simplify=kwargs['simplify']
		else:
			simplify=None
		if simplify:
			from sympy import expand,together
		for i in range(self.doLevel,doLevel+1):
			element=self[i]
			if simplify:
				try:
					element=expand(element)
					element=together(element)
				except:
					pass
			if not self.coeffList:
				self.coeffList={i:self[i]}
			else:
				self.coeffList[i]=self[i]
		self.doLevel=doLevel
	
	def copy(self):
		return series(copy(self.coeff),var=copy(self.var),coeffList=copy(self.coeffList),LB=copy(self.LB),UB=copy(self.UB),doLevel=copy(self.doLevel),powerCoeff=copy(self.powerCoeff))
	def __coerce__(self,data):
		if isinstance(data,series) and self.var==data.var:
			return self,data
		elif isinstance(data,int) or isinstance(data,float):
			return self,num2series(data,var=self.var)
		try: 
			return self,expr2series(data,self.var)
		except:
			raise ValueError('Incompatioble operands')
	
	def __add__(self,p):
		aux1,aux2=coerce(self,p)
		def retCoeff(n):
			return aux1[n]+aux2[n]
		return series(retCoeff,var=self.var,LB=min(aux1.LB,aux2.LB),UB=max(aux1.UB,aux2.UB))
	
	def __radd__(self,p):
		return self+p
	
	def __neg__(self):
		def retCoeff(n):
			return -self[n]
		return series(retCoeff,var=self.var,ord=self.ord,deg=self.deg,N=self.N,LB=self.LB,UB=self.UB)
	
	def __sub__(self,p):
		return self+(-p)
	
	def __rsub__(self,p):
		return p+(-self)
	
	def __mul__(self,p):
		if not self or not p:
			return null2series(var=self.var)
		aux1,aux2=coerce(self,p)
		retOrd=aux1.ord+aux2.ord
		def retCoeff(n):
			if n<retOrd:
				return 0
			ret=0
			for i in range(aux2.ord,n-aux1.ord+1):
				ret+=aux1[n-i]*aux2[i]
			return ret
		return series(retCoeff,ord=retOrd,UB=aux1.UB+aux2.UB,var=self.var,N=retOrd+4)

	def __rmul__(self,p):
		if not self or not p:
			return null2series(var=self.var)
		aux2,aux1=coerce(self,p)#Here, we switch the order. The rest of the code is equal to __mul__. This is implemented this way such that we can admit non-commutative coefficients.
		retOrd=aux1.ord+aux2.ord
		def retCoeff(n):
			if n<retOrd:
				return 0
			ret=0
			for i in range(aux2.ord,n-aux1.ord+1):
				ret+=aux1[n-i]*aux2[i]
			return ret
		return series(retCoeff,ord=retOrd,deg=aux1.deg+aux2.deg,var=self.var,N=retOrd+4)
		
	def __div__(self,p):
		aux1,aux2=coerce(self,p)
		return aux1*aux2.inv()
	def __truediv__(self,p):
		return self.__div__(p)
	def __rdiv__(self,p):
		aux2,aux1=coerce(self,p)
		return aux1*aux2.inv()
	def __rtruediv__(self,p):
		return self.__rdiv__(p)
	def inv(self):
		if not self.ord==0:
			return self.var**(-self.ord)*(self*self.var**(-self.ord)).inv()
		elif not self[0]==1:
			return inverse(self[0])*(self*inverse(self[0])).inv()
		else:
			aux=1-self
			aux.ord=1
			geo=geoSeries()
			return geo(aux)
	
	def __pow__(self,pow):
		if isinstance(pow,int) and pow>0:
			def retCoeff(n):
				return self.getPowerCoeff((n,pow))
			return series(retCoeff,var=self.var,ord=pow*self.ord,deg=pow*self.deg)
		elif isinstance(pow,int) and pow==0:
			return num2series(1)
		elif isinstance(pow,int) and pow<0:
			return (self.inv())**(-pow)
		else:
			try:
				return pow.__rpow__(self)
			except:
				return None
	
	def __rpow__(self,base):
		print 'VARNING: USELESS AND SLOW METHOD'
		EXP=expSeries()
		if isinstance(base,series):
			return EXP(base.ln()*self)
		else:
			try:
				base=S(base)
			except:
				pass 
			return EXP(log(base)*self)
		raise NotImplementedError()
	
	def getPowerCoeff(self,tuple):
		if self.powerCoeff:
			if self.powerCoeff.has_key(tuple):
				return self.powerCoeff[tuple]
		self.powerCoeff={}#List of coefficients 
		deg,pow=tuple
		if pow==0:
			if deg==0:
				self.powerCoeff[tuple]=1
				return 1
			else:
				return 0
		if pow==1:
			self.powerCoeff[tuple]=self[deg]
			return self[deg]
		else:
			if deg < pow*self.ord:
				return 0
			ret=0
			for i in range((pow-1)*self.ord,deg-self.ord+1):
				ret+=self[deg-i]*self.getPowerCoeff((i,pow-1))
			self.powerCoeff[tuple]=ret
			return ret
	
	def ln(self):#Slow
		LN=logSeries()
		aux=self*self.var**(-self.ord)
		constant=aux[0]
		aux=aux/constant-1
		aux.ord=1#Because of some bug, I have to force the order of aux
		logVariableTerm=self.ord*num2series(log(self.var))
		logConstantTerm=num2series(log(constant))
		mainTerm=LN(aux)
		return logVariableTerm+logConstantTerm+mainTerm
	
	def diff(self,var=None):
		if var and not self.var==var:
			return 0
		def retCoeff(n):
			return self[n+1]*(n+1)
		return series(retCoeff,var=self.var,LB=self.LB-1,UB=self.UB-1)
	
	def fdiff(self,var=None):
		return self.diff(var)
	
	def adiff(self,C0=0):
		#if self.orden<0:
		#	raise NotImplementedError('We have not implemented anti-differentiation for series of negative order. However, this should not be a problem to to if we allow to add a log(self.var)-summand to the constant term.')
		def retCoeff(n):
			if n==0:
				return C0+self[-1]*log(self.var)
			else:
				return self[n-1]*Rational(1,n)
		return series(retCoeff,var=self.var,LB=self.LB,UB=self.UB-1)
		
#Konstruksjon av ulike spesielle typer rekker:	
def expr2series(expr,var=Symbol('x')):
	dict={}
	ord=oo
	while expr:
		term=expr.as_leading_term(var)
		expr-=term
		(k,p)=term.as_coeff_exponent(var)
		if ord==oo:
			ord=p
		dict[p]=k
	def coeff(n):
		if dict.has_key(S(n)):
			return dict[S(n)]
		else:
			return 0
	return series(coeff,var=var,ord=ord,deg=p,nicePrint=True)
	

def termExpr2series(term,termVar=Symbol('n'),seriesVar=Symbol('x'),ord=ord):
	def coeff(n):
		return expr.subs({termVar: n})
	return series(coeff,var=seriesVar,ord=ord)

def null2series(var=Symbol('x')):
	return series(var=var,ord=oo,deg=0)

def num2series(value,var=Symbol('x')):
	try:
		value=S(value)
	except:
		pass
	return series(var=var,coeffList={0:value},LB=0,UB=0)

def symbol2series(symbol,var=Symbol('x'),ord=0,deg=oo):
	def retCoeff(n):
		if n<ord or n>deg:
			return 0
		else:
			return Symbol(symbol+'['+str(n)+']')
	return series(retCoeff,var=var,LB=ord,UB=deg,deg=deg,ord=ord)

def geoSeries(var=Symbol('x')):#(1-x)^(-1)
	def retCoeff(n):
		if n<0:
			return 0
		else:
			return 1
	return series(retCoeff,ord=0,deg=oo,var=var)
	
def expSeries(var=Symbol('x')):#e^x
	def retCoeff(n):
		if n<0:
			return 0
		elif n<2:
			return 1
		return retCoeff(n-1)*Rational(1,S(n))
	return series(retCoeff,var=var,ord=0,deg=oo)

def logSeries(var=Symbol('x')):#ln(1+x)
	def retCoeff(n):
		if n<1:
			return 0
		else:
			return Rational((-1)**(n-1),n)
	return series(retCoeff,var=var,deg=oo,ord=1)
	
def sinSeries(var=Symbol('x')):
	def invFakt(n):
		if n<0:
			return 0
		elif n<2:
			return 1
		return invFakt(n-1)*Rational(1,S(n))
	def retCoeff(n):
		if n%2==0:
			return 0
		else:
			return invFakt(n)*(-1)**Rational(n-1,2)
	return series(retCoeff,var=var,ord=1,deg=oo,N=6)


def cosSeries(var=Symbol('x')):
	def invFakt(n):
		if n<0:
			return 0
		elif n<2:
			return 1
		return invFakt(n-1)*Rational(1,S(n))
	def retCoeff(n):
		if n%2==1:
			return 0
		else:
			return invFakt(n)*(-1)**Rational(n,2)
	return series(retCoeff,var=var,ord=0,deg=oo,N=5)

def inverse(obj):
	try:
		return Rational(1,obj)
	except:
		try:
			return 1/obj
		except:
			try:
				return obj.inv()
			except:
				raise ValueError('Non-invertible element')
def copy(obj):
	try:
		return obj.copy()
	except:
		import copy
		return copy.copy(obj)
