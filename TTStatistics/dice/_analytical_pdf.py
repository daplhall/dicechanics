__all__ = ['dicepdf']

from numpy import arange, sum, int64
from scipy.special import factorial

def BinomialFraction(n,k):
   return factorial(n)/(factorial(n-k) * factorial(k))

# TODO give better name, eg dicepdf
def dicepdf(x,n,d):
   """
   x : Number you want to find the likelyhood off ('called T in source')
   n : number of dice
   d : dice type eg d6 (source calls it 's')   
   source : 
      https://mathworld.wolfram.com/Dice.html
      https://towardsdatascience.com/modelling-the-probability-distributions-of-dice-b6ecf87b24ea
      https://stats.stackexchange.com/questions/3614/how-to-easily-determine-the-results-distribution-for-multiple-dice
   """
   assert(x >= n), f"x is not within range for {n}d{d}"
   k   = arange(0, int((x-n)/d) + 1)# Flooring is important
   psi = (-1)**k *BinomialFraction(n,k)*BinomialFraction(x-d*k-1, n-1)
   return sum(psi)/d**n

def var1D(D, mean):
   x = arange(1,D+1)
   return sum((x-mean)**2)/D

def MeanD(N,D):
   return N*(0.5*D + 0.5)

   
