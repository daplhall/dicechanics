# Basic usage
The Module needs to expose the Dice class which needs to be used in the following way  
(N@D + D + Mod) > DC  
Such that you can easily write troll like operations

# Levels
- Level 0: Dice operations
- Level 1: Dice-Pool operations
- Level 2: Pool-Pool operations
- level 3: User defined operations functions (Icepool article )


# Exposed Classes
There are 2 types of classes in TTStatistics. The first is the Dice and the second is the Pool  
In short the die is the representation of a single die, which have its own properties and base statistics.
## Dice
Kwargs: mask, rounding['regular', 'up', 'down']
### Attributes
f - faces, should be masked if mask is given and sorted by mask  
c - the number of the faces. which when taking c/sum(c)
p - properbilites, just a cached c/sum(c) as c only changes through operations


### Operators
These operators generate either a pool if the thing is a die/pool and a die if its a number
For this dice needs a few operator overloads  
\@ operator : Pool - that "rolls"  N dice, creating a pool
\+ operator : Pool - that adds a single number of anytype to the dice  
           - that adds another dice to the dice eg 1d8 + 1d6  
\- operator : Pool - opposite of +  
\* operator : [Pool, Die]- multiply the dice by a single number  
\/ operator - divides dice by a single number, you must be able to specifiy rounding in dice creation, roll under takes precidence when doing dice dice arithmatic  
\> operator - compares the dice with a single number
D.count(...)  - counts the faces given as arugment 

### masking
You need to beable to mask the faces with letters
```
d = Dice("1,3,2", mask = ['A','B','C'])
``o
then if you then call `d.f` you get the mask in the order of the dice

### Constructors needs
number - defines the highest numbered face and assumes a sequence from 1 to number
text - defines the number of faces defined by a sequence eg "1,2,3..6,9", 
        which defines a sequence of [1,2,3,4,5,6,9]
        it also needs to count the number of elements eg "1,2,3,3,4,4"
        needs to calulate the properbilites of the dice pr number.

### Children
#### zDice
defines a 1z9 which defines a sequence from 0 to 9

## Pool
is the collection of many dice
dice - The collection of dice
f - faces
p - properbility
c - counts