# Tabletop statistics
![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png) This project is currently under renovation, APIs are very much subject to change.  
An library for python which provides an interface for modelling dice mechanics. The library have no external dependencies.

## API Documentation
[Documentation on github pages](https://daplhall.github.io/dicechanics)
## Build and install
```bash
git clone <TTstatistics>
cd TTstatistics
pip install .
```
## Dicechanics: A statistical module for dice operations
This submodule exposes 3 classes
1. `Die` The base unit of statistics; Dice are immutable.
2. `Pool` Contains multiple dice which can be operated on together. (Currently not fully reimplemented)
3. `Bag` Contains multiple pools which can be operated on together (Currently not implemented)
### Die
To create a die you simply invoke the `d` interface function.
```python
d6 = ds.d(6) # creates a six sided die.
d42 = ds.d(42) # creates for 42 sided die.
```
This interface can also take a string following a certain syntax.
```python
d("<start..end:repeat>") 
```
Here two number separated by `..` defines a range to be expanded while `:` defines how many times that range is repeated. Multiple of these statements can be written if separated by a comma.
```python
d("1..2:4, 2") # a die with 5 2s and 4 1s
```
A list of numbers can also be given instead, here each entry will be counted.
```python
d([1,2,3,4,2,1])# 2 1s, 2 2s, 1 3 and 1 4
```
---
Dice have die specific operations overloads that allow then to act as a vector or number.
```python
d6 = d(6)
d3 = d(3)
d3+d6-d3*d6/d6
```
These will create new dice objects. New Dice can be made by mapping to new faces.
```python
def filter(outcome):
    if outcome == 4:
        return 4
    elif outcome > 4:
        return 3

newDie =  d('3:6,1..2').map(filter):
```
The same can be achieved by using the die as a decorator
```python
@d('3:6, 1..2')
def mappedDie(outcome):
    if outcome == 4:
        return 4
    elif outcome > 4:
        return 3

newDie = mappedDie()
```
---
Dice has a string representation that is a sideways plot
```cmd
>>> print(d6+d6)
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
---
Dice also have specific shortcut operations. `count` counts the given faces.
```python
d6.count(5,6) # a die with 1 and 0 as faces.
```
`reroll` rerolls af set of faces to a given depth.
```python
d6.reroll(5,6, depth = 3) # rerolls a d6 on 5 or 6 up to 3 times
```
`explode` or `implode` explodes/implodes the faces (reroll but add the rolled face or sub from the old face).
```python
d6.explode(2,6, depth = 3) 
d6.implode(1,2,3, depth = 12) 
```
## Pool
![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png) Not fully reimplemented yet.
Pools are collections of dice, which you want to group together and perform special or custom operations on. The pool is created through the `pool` function, and takes a dict of `Die`.
```
myPool = ds.pool({d6:3,d42:1})
```
To perform an operation on the pool, meaning roll your dice and do something with them, there are multiple procedures to choose from.  
1. `sum(pool)`: sums the outcomes in the pool together, and creates a die representation of it.
2. `mult(pool)`: Same as `sum` just multiplies them  
3. `max(pool)`: Finds the max face of the outcomes
4. `min(pool)`: Finds the min face of the outcomes

There is an additional function which allows custom operations called `perform`. It takes a function that doesn't care about the order of operations of the rolled faces. It takes two arguments.
```python
def addDoubleY(x, y):
    return x+y*2

newDie = perform(myPool, addDoubleY)
```
This can also be achieved through a decorator
```python
@myPool
def addDoubleY(x, y):
    return x+y*2
newDie = addDoubleY()
```
When working with Pools, it not uncommon to roll then and then only operate of a specific subset of the rolled dice. Eg. roll 2 d20 take the highest. The `Pool` class allows slicing it to indicate which subset you want to use.
```python
pool = pool({d20:4, d4:1})
sum(pool[2:]) # the subscript says from the second lowest and up
```
It can also be defined with a boolean list.
```python
pool = pool({d20:4, d4:1})
sum(pool[False, True, True, True, True]) # lowest is to the left
```
Its important to note that the left of the slice or list indicates the Die that ROLLED
the smallest value, its not the left most die defined in the entry data.

The performance between selecting die and not is around 5-6x. however the smaller subset
of die one considers the closer they become. In real world cases the 5-6x is not noticeable (it is noticeable for rolling 50 50 sided dice).

---
Bags can be expanded by pool-pool operations
```python
A = pool({d6:4})
B = pool({d4:2, d20:1})
C = A+B # equivalent to pool({d4:2, d20:1, d6:4})
```
or by expanding it with a die.
```python
A = pool({d6:4})
A.expand(d6) # equivalent to pool({d6:5})
```
## Bag
![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png) Not implemented yet.

# Running benchmarks
To run the benchmarks and saving them.
```bash
pytest benchmarks --benchmark-autosave
```
to run specific tests in a file.
```bash
pytest benchmarks\test_bm_dice.py::<Benchmark>
```
to compare different runs
```bash
pytest-benchmark compare [ids,...]
```

# Running tests
The tests are executed by the following command.
```
pytest tests
```

# Building documentation
```bash
cd docs && mkdir build
sphinx-build -M html src build
```
remember to install its `requirements.txt` when code updates