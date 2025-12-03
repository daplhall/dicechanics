# Dicechanics getting started
Dicechanics is a general-purpose dice probability calculator that provides an easy-to-use interface.

A three-tier system of classes is exposed
1. Die, the base primitive of dicechanics
2. Pool, a group of mixed dice
3. Bag, a pool of pools(Currently not implemented)
All classes are immutable.
## Creating a die
Creating a Die is easy; you invoke the d function.
```python
import ttstatistics.dicechanics as ds
d6 = ds.d(6)
```
The above creates a six-sided die with faces `1,2,3,4,5,6` all represented once.  

Another way is to give a list of faces you want.
```python
ds.d([1,1,2,3,4,5,6])
```
Repeated faces are counted and taken into consideration, so this die is a 7-sided Die
with two faces with a ´1´.   

Instead of the above, you can use a string which can be expanded
```python
ds.d("1:2,2..6")
```
It follows this syntax:
```python
ds.d("<start>..<end>:<repeat>, <new statement>")
```
## Creating a pool
The most common way to create a pool is to use the `@` operator on a primitive.
```python
pool = 3 @ d6
```
Which creates a pool of 3 six-sided dice, another way is with a dict and the `pool` function.
```python
ds.pool({d6:3})
```
The dice are the keys, and the amount is the value of said die.
## Extending pools
To extend pools, you add another pool to it.
```python
p = 3@d6 + 1@d8
```
Or you can extend it one die at a time.
```python
p.extend(d10)
```
## Operating on a pool
A pool by itself does nothing; through the context of an operation, it gains meaning. The following operations are predefined:
1. `sum(pool)`: Sums the outcomes.
2. `mult(pool)`: Multiplies the outcomes.
3. `max(pool)`: Finds the maximum outcome.
4. `min(pool)`: Finds the minimum outcomes.
There is a fifth function named `perform` that allows one to write custom operations:
```python
def addDoubleY(x, y):
    return x+y*2

perform(myPool, addDoubleY)
```
All of these operations collapse the pool into a primitive.
## Choosing a subset of pool outcomes
Let's start by understanding what a pool subset is. Consider that you roll 3d6. A possible set of sorted outcomes is `[1, 3, 6]`. If we then want to sum the lowest outcome and highest outcome, we choose those indices: sum([1,3,6][::2]). This is also how you select subsets with the pool class. 
```python
pool = 3@d6
ds.sum(pool[::2])
```
or
```python
ds.sum(pool[0,-1])
```
## Using binary die operators to create new primitives
You can create new primitives through binary and unary operations; Meaning, instead of using a pool to find the probability of 2d6, you can add the two primitives together.
```
_2d6 = d6 + d6
```
## Visualising results
Printing a primitive shows a probability graph. 
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
Here, `mu` is the mean and `sigma` is the standard deviation.