__all__ = ['advantage', 'disadvantage']
from ..dice import Dice

def advdis(d):
   """
      Function that calulates the properbilies in a vectorized sense
      Only 0 or -1 is not calulated

      Used by both advantage as disadvantage as they are the inverse
      of each other.
   """
   return d.prop[1:]**2 + 2*d.prop[1:]*d.cumulative[:-1]



def advantage(d: Dice) -> Dice:
   """
      dnd advantage
      "Friend function" for dice class
      this is general way if doing it, allowing uneven distributions

      todo This can be even more general where 2 dice are allowed 
      from different distribtuions, eg 1d6 and 1d8

      todo expand to N dice for both cases

      if the dice a normal standard dice then one could use
      (2*y -1)/d^2
   """
   if not isinstance(d, Dice):
      raise ValueError
   newdice = Dice(d)
   newdice._P[0]  = d.prop[0]**2
   newdice._P[1:]= advdis(d)
   newdice._Dice__cumsum()
   return newdice

def disadvantage(d: Dice) -> Dice:
   """
      dnd disadvantage
      "Friend function" for dice class
      this is general way if doing it, allowing uneven distributions

      todo This can be even more general where 2 dice are allowed 
      from different distribtuions, eg 1d6 and 1d8

      todo expand to N dice for both cases

      if the dice a normal standard dice then one could use
      (2*y -1)/d^2
   """
   if not isinstance(d, Dice):
      raise ValueError
   newdice = Dice(d)
   newdice._P[-1]  = d.prop[0]**2
   newdice._P[:-1] = advdis(d)[::-1]
   newdice._Dice__cumsum()
   return newdice
