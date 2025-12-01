# Dicechanics getting started
Dicechanics is a general purpose probability calculator. The goal is that you can model any dice mechanics from an existing game or a game you develop, such that you can have a feel for how chances to the die rolling system affects the probability.  

Three classes are exposed:
1. Die 
2. Pool
3. Bag (Currently not implemented)

The Die is the lowest element, and represents a real life Die. A Pool is a group of dice,
allowing you to mix multiple dice and select subsets of their outcomes. Lastly the Bag which is a Pool of Pools, allowing you to compare different pools. They are all immutable. 
## Creating a die
Creating a Die is easy you simple invoke the `d` function.
```
import ttstatistics.dicechanics as ds
d6 = ds.d(6)
```
The above creates a six sided die with faces `1,2,3,4,5,6` all resent once.  

Another way is giving a list of faces you want.
```
ds.d([1,1,2,3,4,5,6])
```
Repeated faces are counted and taken into consideration, so this die is a 7-sided Die
with two faces with a ´1´.   

Instead of the above you can use a string following a specific format.
```
ds.d("<start>..<end>:<repeat>")
```
The previous example could be written as
```
ds.d("1:2,2..6")
```
## Creating a pool
There are two way of creating a pool. The one is applying the `@` operator on a die
```python
pool = 3 @ d6
```
This creates a pool of 3 six-sided dice. The other is with a dict and the `pool` function.
```python
ds.pool({d6:3})
```
The dice are the keys and the amount is the values of the dictionary.
## Operating on a pool
A pool in it self is worthless, you need to define what operations you do between the outcomes of the dice. This is done in a procedural way with the following functions
1. `sum(pool)`: sums the outcomes in the pool together, and creates a die representation of it.
2. `mult(pool)`: Same as `sum` just multiplies them  
3. `max(pool)`: Finds the max face of the outcomes
4. `min(pool)`: Finds the min face of the outcomes  

There is an additional function which allows custom operations called `perform`. It allows one to apply linear operations to the pool
```python
def addDoubleY(x, y):
    return x+y*2

perform(myPool, addDoubleY)
```
## Choosing a subset of pool outcomes
Before we get to the syntax, lets first look at what a subset means. Consider that you roll 3 d6, here a possible set of outcomes are `[1, 3, 6]`, the outcomes are sorted the dice are thrown at the same time. Then if we want to add the largest and the lowest here we simply index the sorted outcome list as following `sum([1,3,6][::2])`.  

This is the logic behind the syntax to follow. To select a subset we simply index our pool in the same way.
```
pool = 3@d6
ds.sum(pool[::2])
```
The logic is the same, we index into a sorted list of outcomes, where the largest is the highest index and the smallest value the lowest.  

You can also choose specific indexes
```
pool[1]
```
Because we have 3 dice, we choose the middle of them.

## Binary die operator as a shortcut
Dice also have binary and unary operations for interacting with other die or numbers.  
Example instead of using a pool to find the probability of 2d6, you can simply add the two primitives together.
```
sum2d6 = d6 + d6
```
This can be done also be done with numbers, and every binary operation. This is a shortcut for defining a dice with the same probability as rolling multiple.

## Visualizing results
You can simply print a Die to shows its probability.
```
>>> print(sum(2@d6))
Die with mu - 7.00, sigma - 2.42
--------------------------------
 2|### 2.78%
 3|####### 5.56%
 4|########## 8.33%
 5|############# 11.11%
 6|################# 13.89%
 7|#################### 16.67%
 8|################# 13.89%
 9|############# 11.11%
10|########## 8.33%
11|####### 5.56%
12|### 2.78%
```