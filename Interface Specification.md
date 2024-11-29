# Basic usage
The Module needs to expose the Dice class which needs to be used in the following way
(N@D + D + Mod) > DC
Such that you can easily write troll like operations
For this dice needs a few operator overloads
@ operator - that "rolls"  N dice
+ operator - that adds a single number of anytype to the dice
           - that adds another dice to the dice eg 1d8 + 1d6
- operator - opposite of +
* operator - multiply the dice by a single number
/ operator - divides dice by a single number, you must be able to specifiy rounding in dice creation, roll under takes precidence when doing dice dice arithmatic
> operator - compares the dice with a single number
D.count(...)  - counts the faces given as arugment 

# Constructors needs
number - defines the highest numbered face and assumes a sequence from 1 to number
text - defines the number of faces defined by a sequence eg "1,2,3..6,9", 
        which defines a sequence of [1,2,3,4,5,6,9]
        it also needs to count the number of elements eg "1,2,3,3,4,4"
        needs to calulate the properbilites of the dice pr number.


# Children
## zDice
defines a 1z9 which defines a sequence from 0 to 9
