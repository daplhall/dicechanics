from collections.abc import Iterable
from numpy           import array, int32, float32, int64, float64,\
                            sqrt, average, cumsum, copy, append, zeros, ndarray, \
                            issubdtype, integer, unique
from scipy.signal    import fftconvolve


# TODO cases for int float etc is the default so it goes into an else
class Dice(object):
   """
      Class that represents a dice of some form. It contains its PDF and CDF 
      and allows one to have an anydice like syntax to get the distribution for more than 1 dice rolled.
   """
   def __init__(self, d = 1, dist = None, startvalue = 1,**kwards):
      self._identity = {}
      if dist is None and isinstance(d, (int,float, int64, float64,int32,float32)):
         # flat distribution
         self._X = array(range(startvalue,d+startvalue));
         self._P = array([1/d]*d);
         self.length  = self._P.size-1
         i = str(self._X.size)
         self._identity = {i : 1}
         self._update()
      elif isinstance(d, Dice):
         # Copy dice
         self._X    = copy(d._X )
         self._P    = copy(d._P)
         self.length  = self._P.size
         self._csum   = copy(d._csum)
         self._identity = d._identity.copy()
         # self.__sf    = copy(d.__sf)
         self._mean     = d._mean
         self._var      = d._var
      elif isinstance(dist, Iterable):
         dist = array(dist)
         if issubdtype(dist.dtype, integer):
            l    = dist.size
            x, c = unique(dist, return_counts = True)            
            self._P = c/l
            self._X = x
            self.length = self._P.size
            self._update()
         else:
            ## For iterables such as list and tuples
            self._P = dist
            self._X = array(range(startvalue,startvalue+self._P.size));
            self.length  = self._P.size
            i = str(self._X.size)
            self._identity = {i : 1}
            self._update()
      elif callable(dist):
         # if d is a func
         self._X = array(range(startvalue,d+startvalue));
         self._P = d(self._X, d,**kwards)
         self.length  = self._P.size
         i = str(self._X.size)
         self._identity = {i : 1}
         self._update()
      else:
         raise ValueError

   def _update(self):
         self._csum= self._cumsum()
         #self.__sf    = self.__survival()
         self._mean  = self._calcmean()
         self._var   = self._calcvar()
         return

   def __str__(self):
      res = [f"{count}d{dice}"if dice != 'mod' else f"{count}" for dice, count in self._identity.items()]
      text = ""
      for item in res:
         if item[0] == '-':
            text += f"{item}"
         else:
            text += f"+{item}"
      return 'Dice: ' + text[1:]
   
   def __add__(self, right):
      newdice = Dice(self)
      if isinstance(right, (int ,float, int64, float64, int32, float32)):
         newdice._X = self._X + right
         newdice._P = self._P
         newdice._csum  = newdice._cumsum();
         newdice._sf    = newdice._survival();
         newdice._mean  = self._mean + right
         newdice._var   = self._var
         newdice._addidentity(right)
         return newdice
      elif isinstance(right, Dice):
         newdice.length  = self.length + right.length -1
         newdice._X = array(range(self._X[0] + right._X[0], self._X[-1] + right._X[-1] + 1))
         newdice._P = fftconvolve(self._P, right._P)
         newdice._csum = newdice._cumsum();
         newdice._sf   = newdice._survival();
         newdice._mean = self._mean + right._mean
         newdice._var  = self._var + right._var
         newdice._addidentity(right)
         return newdice
      
   def __radd__(self, left):
      return self + left;

   def __sub__(self, right):
      newdice = Dice(self);
      if isinstance(right, (int, int64, float, float64, int32, float32)):
         newdice._X = self._X - right
         newdice._P = self._P
         newdice._csum = newdice._cumsum();
         newdice._sf   = newdice._survival();
         newdice._mean = self._mean - right
         newdice._var  = self._var
         newdice._addidentity(-right)
         return newdice
      elif isinstance(right, Dice):
         right           = -right
         newdice.length  = self.length + right.length - 1
         newdice._X = array(range(self._X[0] + right._X[0], self._X[-1] + right._X[-1] + 1))
         newdice._P = fftconvolve(self._P, right._P)
         newdice._csum = newdice._cumsum();
         newdice._sf   = newdice._survival();
         newdice._mean = self._mean + right._mean
         newdice._var  = self._var + right._var
         newdice._addidentity(right)
         return newdice
   
   def __rsub__(self, left):
      return self - left;

   def __mul__(self, right):
      if isinstance(right, (int, int64, float, float64)):
         newdice = Dice(self)
         newdice.__mean *= right
         return newdice

   def __rmul__(self, left):
      return self*left
      
   def __rmatmul__(self, left):
      if isinstance(left, (int, int32, int64)):
         newdice = Dice(d = self);
         if left == 0:
            return  Dice(1)
         elif left == 1:
            return newdice
         else:
            for i in range(left - 1):
               ## make this recursive, such that we add d6 to d6 that thens add d6.... and so on
               newdice = newdice + self
            newdice._mean = self._mean*left
            return newdice

   def __neg__(self):
      newdice = Dice(self)
      newdice._identity = {("-"+key): val for key, val in self._identity.items()}
      newdice._X = -self._X[::-1]
      newdice._P =  self._P[::-1]
      newdice._calcmean()
      return newdice

   def _cumsum(self):
      return cumsum(self._P)

   def _survival(self):
      return cumsum(self._P[::-1])[::-1]

   def _calcmean(self):
      """
         Population mean
      """
      return sum(self._P*self._X);

   def _calcvar(self):
      return average((self.values - self._mean)**2, weights = self.prop)

   def _addidentity(self, dice):
      if isinstance(dice, Dice):
         for i in dice._identity:
            if i in self._identity:
               self._identity[i] += dice._identity[i]
            else:
               self._identity[i] = dice._identity[i]
      elif isinstance(dice, (int, float, int32, float32, int64, float64)):
         if 'mod' in self._identity:
            self._identity['mod'] += dice
            if self._identity['mod'] == 0:
               self._identity.pop('mod')
         else:
            self._identity['mod'] = dice 

   def _removeidentity(self, dice):
      if isinstance(dice, Dice):
         for i in dice._identity:
            if i in self._identity:
               self._identity[i] -= dice._identity[i]
               if self._identity[i] < 1:
                  self.pop(i)

   ### Exposed functions and properties
   @property
   def values(self):
      return self._X;

   @property
   def prop(self):
      """
         All values of the mass distrubiton function 
      """
      return self._P;

   @property
   def cumulative(self):
      """
         Returns the cumulive properbility list
      """
      return self._csum

   @property
   def survival(self):
      return 1-self._csum
   
   @property
   def mean(self):
      """
         returns the mean of the distribution
      """
      return self._mean;
   
   @property
   def std(self):
      """
         Standard deviation of the distribution
      """
      return sqrt(self._var)

   def pdf(self,values):
      if isinstance(values, (int, int32, int64)):
         values  = array([values])
      elif not isinstance(values, ndarray) and isinstance(values, Iterable):
         values  = array(values)
      values    -= self._X[0]
      res        = zeros(values.size)
      insidemask = (values >= 0) & (values <= self._X.size - 1)
      res[insidemask] = self._P[values[insidemask]] 
      res[(values  < 0) | (values >  self._X.size - 1)] = 0# could be  ~insidemask
      return res

   def cdf(self,values):
      if isinstance(values, (int, int32, int64)):
         values  = array([values])
      elif not isinstance(values, ndarray) and isinstance(values, Iterable):
         values  = array(values)
      values    -= self._X[0]
      res        = zeros(values.size)
      insidemask = (values >= 0) & (values <= self._X.size - 1)
      res[insidemask] = self._csum[values[insidemask]]
      res[values < 0] = 0
      res[values > self._X.size-1] = 1
      return res

   def sf(self, values):
      """
         survival function
      """
      return 1 - self.cdf(values)
   
   def set_startvalue(self, value):
      diff         = self._X[0] - value 
      self._X = array( range(value,(self._X[-1]-diff) + 1) );
      return

   def with_reroll(self, *redo, repeat = 1):
      """
         TODO  can be optimzied in terms of algorithm and code length   
         Modifies 1 dice such that the values in redo couunt as a recount

         if you eg want to model greath weapon fighting form dnd 5e, then you define
         that your dice are allowed to be rerolled.
         For this example we will use a greatsword of 2d6 damage

         gwf = 2@with_reroll(d6,redo = 1)

         This means roll 2 dice where they get to reroll their value of 1.

         The math behind this is that if you have a random number x in R, where are is the
         subset of numbers on the dice that should be rerolled
         then P(x in R) = P(x)^{n_r} where n_r is the number of rerolls
         the values not in R is given by
         P(n)*\sum_{i=0}^{n_r} P(R)^i
         so
                    |  P(n)^n_r                       for n in R
         P(n,n_r) ={
                    |  P(n)*\sum_{i=0}^{n_r} P(R)^i   else
         P(R) is the chance to get a reroll so sum of the properbility of all members

      """
      newdice = Dice(d=self)
      R  = sum([self.pdf(r) for r in redo])
      Rf = R**repeat
      Rs = (1 - Rf*R)/(1 - R)# Geometrix series for 1 + R + R^2 + R^3 ........ up to N
      for i, (p, x) in enumerate(zip(self._P, self._X)):
         if x in redo:
            newdice._P[i] = Rf*p
         else:
            newdice._P[i] = Rs*p
      return newdice

   def count(self, *count):
      """
         TODO can be expanded such that one can give multiple sets that needs to be "counted"
         if you give a set then all items in count must be seperate sets

         such that a non-coin like form can be addapted 

         converts dice into a binomial dice of Succes or failure in principle 

         counts the numbers in 'count'.
         So if you define d6.count(6) then roll of 6 is a succes
         and 1,2,3,4,5 is not. thus you gain a dice of (0,1/6),(1, 1/6)
      """

      if isinstance(count[0],Iterable):
         flat =  [item for sublist in count for item in sublist]
         Ps = [sum([self.pdf(i) for i in bracket]) for bracket in count]
         Pf = sum([self.pdf(i) for i in set(self.values)- set(flat)])
         return Dice(startvalue = 0, dist = append(Pf,Ps))
      else:
         Ps = sum([self.pdf(i) for i in count])
         Pf = sum([self.pdf(i) for i in set(self.values)- set(count)])
         return Dice(startvalue = 0, dist = append(Pf,Ps))

if __name__ == '__main__':
   import matplotlib.pyplot as plt