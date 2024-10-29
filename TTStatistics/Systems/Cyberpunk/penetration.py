__all__ = ['penetration']

from numpy            import arange, sum, maximum, array
from ..dice._analytical_pdf import dicepdf

def odl_penetration(sp,N,D,mod):
   """
   sp : array_like or iterable

   Function that calucates the likelyhood for penetrating of a given SP 
   """
   DmgThatPenetrate = lambda x: arange(maximum(x-mod + 1,N) , N*D +1 )
   return array([sum(
                     [dicepdf(damage,N,D) for damage in DmgThatPenetrate(SP)]
                     ) for SP in sp])
   
def penetration(sp, dmgdice):
   """
      Penetration is  cyberpunk is when "DMG rolled" > SP.
      so the chance for penetration is the chance of rolling over SP.
      This is the sum of every point of damage possible over SP that the dice is capaple of
      ie. the survival function of the dice is the penetration
   """
   return dmgdice.sf(sp)