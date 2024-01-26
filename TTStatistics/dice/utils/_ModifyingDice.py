__all__ = ['foldnegative','foldpositive','remove_dice']

from numpy import sum, argmax, zeros_like, sum
from scipy.signal import deconvolve
from .._Dice import Dice

#TODO what happens if you exceed the dice range with a cutoff? 
def foldnegative(dice:Dice, cutoff:int = 0) -> Dice:
   """
   "Friend" function of dice
   rolls all negative into the lowest value
   """
   summask = dice.values <= cutoff
   Psum   = sum(dice._P[summask])
   i0      = sum(summask)-1 # index of "0"
   newdice = Dice(dice.length - i0
                  , startvalue = dice._X[0]+i0)
   newdice._P[0] = Psum 
   newdice._P[1:] = dice._P[i0+1:]
   return newdice

def foldpositive(dice:Dice, cutoff:int = 1):
   """
   "Firend" function to dice

   Cutoff is where you say everything over this value, and store it in its location (given that the cutoff is defined in the range)
   eg. cutoff = 3 on a d6, then P(3)+P(4)+P(5)+P(6) is stored at 3.
   """
   summask = dice.values >= cutoff
   Psum    = sum(dice._P[summask])
   i0      = argmax(summask) # First instance of 1 in sunmask
   newdice = Dice(i0 + 1, startvalue = dice.X[0])
   newdice._P[-1]  = Psum
   newdice._P[:-1] = dice._P[:i0]
   return newdice

def remove_dice(dice, remove):
   dist, _ = deconvolve(dice.prop, remove.prop)
   D =  Dice(dice.length - remove.length
            ,  startvalue = dice._X[0] - remove.__X[0]
            ,  dist = dist
   )
   return D

def _reroll(t, dice, basedie = None):
   """
   Calulates the properbility of rolling X=x if rerolling no x is allowed
   so basilly you reroll what is not equal to the number you want. 
   TODO  check of the sum of 2 wanted numbers is the same 
   
   Follows
   P(t) = sum_i^t P(N,t)*P(N-i, t-i)
   where N is the number of dice, and t is the wanted number
   N-1 in the second factor is because if you roll a i succes then you need to roll i less dice the second time

   found it here, but it is quite logical as we ask P(t = z), then we just need to add the properbility of every combination 
   https://rpg.stackexchange.com/questions/201364/anydice-counting-successes-on-dice-and-rerolling-any-bonus-dice-below-the-t

   """
   if basedie is None:
      basedie = dice
   res = 0
   for i in range(t + 1):
      rm = basedie if i == 0 else remove_dice(dice,basedie)
      res += dice.pdf(i)*rm.pdf(t-i)
   return res

# def with_reroll(dice, redo = 1):
#    """
#       TODO  can be optimzied in terms of algorithm and code length   
#       Modifies 1 dice such that the values in redo couunt as a recount

#       if you eg want to model greath weapon fighting form dnd 5e, then you define
#       that your dice are allowed to be rerolled.
#       For this example we will use a greatsword of 2d6 damage

#       gwf = 2@with_reroll(d6,redo = 1)

#       This means roll 2 dice where they get to reroll their value of 1.
#    """
#    newdice = Dice(d=dice)
#    if not hasattr(redo,'__len__'):
#       redo = (redo,)
#    R = sum([dice.pdf(r) for r in redo])
#    for i, (p, x) in enumerate(zip(dice._Dice__pdf_P, dice._Dice__pdf_X)):
#       if x in redo:
#          newdice._Dice__pdf_P[i] = R*p
#       else:
#          newdice._Dice__pdf_P[i] = (1+R)*p
#    return newdice

# def with_reroll(dice, basedie = None):
#    """
#    Todo optimize where possible, eg. vectorize
#    Fired of "Dice"

#    calulates _reroll for all t value in a dice


#    This used by applying to 1 dice and then use the @ operator to roll multiple
#    """
#    if basedie is None:
#       basedie = dice
#    prop = zeros_like(dice.prop)
#    for idx, t in enumerate(dice.values):
#       prop[idx] = _reroll(t, dice, basedie)
#    newdice = Dice(dice)   
#    newdice._Dice__pdf_P = prop
#    return newdice



