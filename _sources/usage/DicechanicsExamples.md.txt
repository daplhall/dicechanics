# Dicechancis examples
Here are a few examples of how to model some known tabletop RPG systems.
## Blades in the Dark
In BitD, you create a pool of d6s and take the highest. On a hit less than 3, you get a consequence; on a 4 or 5, you succeed with a consequence; on a 6, you succeed.

Let's say we amassed 4 dice
```python
import ttstatistics.dicechanics as ds

d6 = ds.d(6)
pool = 4 @ d6
print(ds.max(pool))
```
Output:
```
Die with mu - 5.24, sigma - 5.98
--------------------------------
1| 0.08%
2| 1.16%
3|## 5.02%
4|##### 13.50%
5|########### 28.47%
6|#################### 51.77%
```
As previously mentioned, the values rolled are mapped to a meaning.
```python
def BitD(outcomes):
    if outcomes < 4:
        return 'C'# Consequence
    elif outcomes > 5:
        return 'S'# Success
    else:
        return 'M'# Mixed
print(ds.max(pool).map(BitD))
```
Output:
```
Die with mu - n/a, sigma - n/a
------------------------------
C|## 6.25%
M|################ 41.98%
S|#################### 51.77%
```
So with 4 dice, we have a 6.25% chance of just failing, which is pretty good odds.

## Free Leagues Alien RPG
In the Alien RPG, you again have a d6 dice pool; however, you are looking for Dice which rolled a 6, and count the number of these hits.

To model this, we can consider the individual d6 as a weighted two-sided die (a coin).

Let's say our pool has 5 dice, then we write:
```python
import ttstatistics.dicechanics as ds

d = ds.d(6).count(6)
print(ds.sum(5@d))
```
Output:
```
Die with mu - 0.83, sigma - 5.85
--------------------------------
0|#################### 40.19%
1|#################### 40.19%
2|######## 16.08%
3|## 3.22%
4| 0.32%
5| 0.01%
```
## Call of Cthulhu 7th Edition
In Call of Cthulhu, you roll a d100 against your skill. Here, there are 6 success levels to which the result can be mapped.

```python
import ttstatistics.dicechanics as ds


def CoC(outcome):
	global skill
	if skill >= 50:
		fumble = 100
	else:
		fumble = 96
	if outcome >= fumble:
		return "U"
	elif outcome == 1:
		return "C"
	elif outcome > skill:
		return "F"
	elif outcome <= skill // 5:
		return "E"
	elif outcome <= skill // 2:
		return "H"
	else:
		return "S"


skill = 50
d = ds.d(100)
print(d.map(CoC))
```
Output:
```
Die with mu - n/a, sigma - n/a
------------------------------
C| 1.00%
E|#### 9.00%
H|###### 15.00%
S|########## 25.00%
F|#################### 49.00%
U| 1.00%
```

## Burning Wheel Open Ended Rolls
In Burning Wheel you roll `Nd6` where a 4,5 or 6 on the d6 counts as a success. This can be modelled just like the Alien example. However Buring Wheel also has "open ended rolls" meaning that a 6 explodes such that each subsequent 6 counts as a hit.  

So lets say we roll 4d6 that is open ended, we can model it as:
```Python
def openEnded(outcome):
	if outcome % 6 == 0:
		return outcome // 6
	elif outcome % 4 == 0:
		return 1 + outcome // 6
	elif outcome % 5 == 0:
		return 1 + outcome // 6
	else:
		return 0 + outcome // 6


d6 = ds.d(6)
exploded_d6 = d6.explode(6, depth = 3)
print(ds.sum(4 @ exploded_d6.map(openEnded)))

```
Output:
```
Die with mu - 2.40, sigma - 1.37
--------------------------------
 0|#### 6.25%
 1|############## 20.83%
 2|#################### 29.51%
 3|################ 23.77%
 4|######### 12.59%
 5|### 4.95%
 6|# 1.57%
 7| 0.41%
 8| 0.09%
 9| 0.02%
10| 0.00%
11| 0.00%
12| 0.00%
13| 0.00%
14| 0.00%
15| 0.00%
16| 0.00%
```