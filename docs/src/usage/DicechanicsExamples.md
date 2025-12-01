# Dicechancis examples
Here are a few example of how to model some known tabletop rpg systems.
## Blades in the Dark
In BitD, you create a pool of d6s through various means. It ranges from 0 to 6 dice. Then taking the highest. On a 3 you fail, 4 and 5 you succeed with a consequence on a 6 you succeeds

Lets say we amassed 4 dice
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
As previously mention the values have a meaning, so we can map them to new one.
```python
def BitD(outcomes):
    if outcomes < 4:
        return 0
    elif outcomes > 5:
        return 2
    else:
        return 1
print(ds.max(pool).map(BitD))
```
Output:
```
Die with mu - 1.46, sigma - 1.62
--------------------------------
0|## 6.25%
1|################ 41.98%
2|#################### 51.77%
```
So with 4 dice we have a 6.25% chance of just failing, which are pretty good odds.

## Free Leagues Alien RPG
In the Alien RPG you again have a 6ds dice pool, however you are look for Dice 
which rolled a 6, and counting them.

To model this you can consider the individual dice, to be a two sided dice with
either a hit (1) or miss (0).

So if we have a pool 5 dice we simply do.
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
In Call of Cthulhu you roll a d100 and then depending on your skill you have various 
thresholds which dictate which kind of success level you have.

```python
import ttstatistics.dicechanics as ds


def CoC(outcome):
	global skill
	if skill >= 50:
		fumble = 100
	else:
		fumble = 96
	if outcome >= fumble:
		return -1
	elif outcome == 1:
		return 4
	elif outcome > skill:
		return 0
	elif outcome <= skill // 5:
		return 3
	elif outcome <= skill // 2:
		return 2
	else:
		return 1


skill = 50
d = ds.d(100)
print(d.map(CoC))
```
Output:
```
Die with mu - 1.32, sigma - 4.15
--------------------------------
 4| 1.00%
 3|#### 9.00%
 2|###### 15.00%
 1|########## 25.00%
 0|#################### 49.00%
-1| 1.00%
```
