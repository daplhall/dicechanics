from typing import Generator
from itertools import product
from math import sqrt
import operator as op
from DiceStatistics._parser import faces_to_count
from DiceStatistics.types import primitives
from DiceStatistics._math import gcd
import DiceStatistics.Pool as Pool 

type Dice = Dice
type Pool = Pool.Pool


class Dice(object):

	def __init__(self, faces, /, mask = None, rounding = None):
		self._f, self._c = faces_to_count(faces)		
		self._derived_attr()
		self._mask = mask if mask else None
		self._rounding = rounding if rounding else lambda x: x

	def _derived_attr(self):
		self._simplify()
		self._units = sum(self._c)
		self._p = [i/self._units for i in self._c]
		self._mean = sum(p*f for p, f in zip(self.c, self.p))
		self._var = sum(p*(x-self._mean)**2 for x, p in zip(self._f, self._p))
		self._cdf = self._cumulative()

	def _cumulative(self) -> list:
		res = []
		for p in self.p: ## can fold this out an call with iter to clean up the if statement
			res.append(p + res[-1] if res else p)
		return res
		
	def _simplify(self):
		if (c := self._c) and (len(c) > 1): 
			d = gcd(c[0], c[1])
			for i in c[2:]:
				d = gcd(d, i)
				if d == 1:
					break
			self._c = [c//d for c in self._c]

	@property
	def f(self) -> list:
		return self._f
	@property
	def p(self) -> list:
		return self._p

	@property
	def c(self) -> list:
		return self._c
	
	@property
	def mean(self) -> float:
		return self._mean

	@property
	def cdf(self) -> list:
		return self._cdf

	@property
	def var(self) -> float:
		return self._var

	@property
	def std(self) -> float:
		return sqrt(self._var)

	def copy(self) -> Dice:
		return Dice(i for i in self)

	def max(self):
		return max(self._f)

	def min(self):
		return min(self._f)
	
	def reroll(self, *redo, depth:int = 1) -> Dice:
		"""
		TODO Refactor
		Rerolling in properbility terms are given as
		P(n)*\sum_{i=0}^{n_r} P(R)^i
		so
			   |  P(n)^n_r                       for n in R
		P(n,n_r) ={
			   |  P(n)*\sum_{i=0}^{n_r} P(R)^i   else
		the else part is a finite geomentric series with the convergence
		1+r+r^2+r^3..r^n = (1-r^n)/(1-r)
		
		then to convert into counts we simply use
		p(n)^i = c(n)^i/D^i
		for the else part you can supsitute this into it
		and get
		c(n != R) = D^i*p(n!=R) = c(n) (D^i - c(R)^i)/(D - c(R))
		
		[For p(n,n_r) to be a count we need the same "units" on both branches]
		 
		 
		on reroll once on d6 we get the same from
		Q = tts.Dice([1,2,3,4,5]*6+[i for i in tts.d6])
		for reroll 2d6 on a 6 on a d6
		Q = tts.Dice([1,2,3,4,5]*36+[i for i in 2@tts.d6])
		for reroll 6 replacing 5 and 6 with 1d6
		C = tts.Dice([1,2,3,4]*6+2*[i for i in tts.d6])
		So we need to multiply all non redo time the demoninator of the dice that is replacing the roll
		
		think that reroll is just replacing a dice with the redo value
		
		l = sum([c for c, f in zip(self._c, self._f) if f in redo])
		f = list(filter(lambda x: x not in redo,(i for i in self)))
		return Dice(f*(self._units) + l**depth*[i for i in self])
		
		In the 1.0 we have 
		if x in redo:
            		newdice._P[i] = Rf*p
         	else:
            		newdice._P[i] = Rs*p
		so we multiply the chances of hitting times our own properbility
		this we need to account for,
		"""
		# Saving this legacy code for now
		i = depth # i +1
		D = self._units
		cr = sum([c for c, f in zip(self._c,self._f) if f in redo])
		A = (D**(i+1) - cr**(i+1))//(D - cr)
		count = []
		for c,f in zip(self._c, self._f):
			if f in redo:
				count.append(cr**i * c)
			else:
				count.append(A*c)
		res = self.copy()
		res._c = count
		res._derived_attr()
		res._simplify()
		return res

	
	def count(self, *count):
		return Dice(i in count for i in self)

	def __call__(self, func) :
		def wrapper():
			self.__init__(func(i) for i in self)
			return self
		return wrapper

	def __iter__(self) -> Generator[int | float]: # might need ot be text also when mask
		for f, c in zip(self.f, self.c):
			for _ in range(c):
				yield f
				
	def __contains__(self, value: any) -> bool:
		return value in self._f
	
	def _binary_level0(self, rhs: int | float, ops: callable ) -> Dice:
		return Dice(self._rounding(ops(f, rhs)) for f in self)

	def _binary_level1(self, rhs: Dice, ops:callable) -> Pool:
		return Dice(self._rounding(ops(*i)) for i in product(self, rhs))
	
	def _binary_op(self, rhs: int | float | Dice, ops:callable) -> Dice:
		if isinstance(rhs, primitives):
			return self._binary_level0(rhs, ops)
		elif isinstance(rhs, Dice):
			return self._binary_level1(rhs, ops)
		else: # TODO This here should test the other way around. maybe have a try catch
			raise Exception("Unexpected type in dice level 0")

	def __add__(self, rhs: int | float | Dice ) -> Dice :
		"""
		only does level 0, if higher up we reverse the call.
		TODO rounding reaction
		"""
		return self._binary_op(rhs, op.add)

	def __radd__(self, lhs: int | float | Dice)-> Dice:
		return self._binary_op(lhs, op.add)
	
	def __sub__(self, rhs: int | float | Dice ) -> Dice :
		# needs to react to rounding
		return self._binary_op(rhs, op.sub)

	def __rsub__(self, lhs: int | float | Dice)-> Dice:
		return self._binary_op(-lhs, op.add)

	def __mul__(self, rhs: int | float | Dice ) -> Dice :
		## Needs to react to rounding
		return self._binary_op(rhs, op.mul)
	
	def __rmul__(self, lhs: int | float | Dice) -> Dice:
		return self._binary_op(lhs, op.mul)

	def __truediv__(self, rhs: int | float | Dice ) -> Dice :
		# needs to reach to rounding
		return self._binary_op(rhs, op.truediv)
	
	def __floordiv__(self, rhs: int | float | Dice ) -> Dice :
		# needs to reach to rounding
		return self._binary_op(rhs, op.floordiv)

	def __lt__(self, rhs: int | float | Dice) -> Dice:
		return self._binary_op(rhs, op.lt)

	def __le__(self, rhs: int | float | Dice) -> Dice:
		return self._binary_op(rhs, op.le)

	def __ne__(self, rhs: int | float | Dice) -> Dice:
		return self._binary_op(rhs, op.ne)

	def __ge__(self, rhs: int | float | Dice) -> Dice:
		return self._binary_op(rhs, op.ge)
	
	def __gt__(self, rhs: int | float | Dice) -> Dice:
		return self._binary_op(rhs, op.gt)

	def __eq__(self, rhs: int | float | Dice) -> Dice:
		return self._binary_op(rhs, op.eq)
	
	def _rmatmul_level0(self, lhs:int, ops: callable) -> Dice:
		if neg := lhs < 0:
			lhs *= -1
		res = self
		for _ in range(lhs-1):
			res = ops(res,self)
		return -res if neg else res
	
	def _rmatmul_level1(self, lhs: Dice, ops: callable) -> Dice:
		"""
		This is a overlap operations, ie overlapping 2 results
		its not the same as "adding" two dice together and thus
		the counts needs to be the same units 	
		"""
		res = []
		units = self._units
		nrolls = max(lhs.min(), lhs.max())
		for i in lhs:
			base = units**(nrolls-i)
			res += [j for j in i@self]*base
		return Dice(res)
	
	def _binary_rmatmul(self, lhs: int | Dice, ops:callable):
		if isinstance(lhs, int):
			return self._rmatmul_level0(lhs, ops)
		elif isinstance(lhs, Dice):
			return self._rmatmul_level1(lhs, ops)
		else:
			raise Exception("Unexpected type in dice matmul")


	def __rmatmul__(self, lhs: int | Dice) -> Dice:
		"""
			Rolls self LHS times and adds them together
		"""
		return self._binary_rmatmul(lhs, op.add)
	
	def __matmul__(self, rhs):
		return rhs._binary_rmatmul(self, op.add)

	def _unary_level0(self, ops:callable) -> Dice:
		return Dice(self._rounding(ops(i)) for i in self)

	def __neg__(self) -> Dice:
		return self._unary_level0(op.neg)
	
	def __pos__(self) -> Dice:
		return self._unary_level0(op.pos)
	
	def __invert__(self) -> Dice:
		return self._unary_level0(op.invert)
	
