# DiceStatistics a dice statistical tool
DiceStatistics provides a interface in python for doing dice statistics, which produces exact statistics for dice properbility
## Usage
2 classes are provided, a Dice class used for representing standard operations, and a Pool class which allows one to do custom operations based on the outcomes of each seperate dice.  
### *Dice Example*:

```
import TTStatistic as tts
import matplotlib.pyplot as plt
d6 = tts.d(6)
A = 2@d6 + 3
B = d6-d6*d6/d6
C = A + B

fig, ax = plt.subplots()
ax.plot(C.f, C.p)
plt.show()
```
```
@Dice('3:6, 1..2')
def mydice(outcome):
	if outcome == 4:
		return 4
	elif outcome > 4:
		return 3

dice = mydice():
```

### *Pool Example*
```
import TTStatistic as tts
import matplotlib.pyplot as plt

@tts.Pool(tts.d6, tts.d100, tts.d10)
def Advantage(Write me):
	Write me

fig, ax = plt.subplots()
ax.plot(C.f, C.p)
plt.show()
```

```
d10[10] -> pool
A = d10.pool(10) -> pool
A.perform(some_function)
```
## Building
Write me!