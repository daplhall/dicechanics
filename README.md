# DiceStatistics a dice statistical tool
DiceStatistics provides a interface in python (inspired by anydice) for doing dice statistics, which produces exact statistics for dice properbility
## Build
- create venv
- install packages in requirements.txt
- `python -m build .`
- `pip install dist\*.whl`
### Examples
To make notebooks work with venv use `ipython kernel install --user --name=DiceStatistics`
## Usage
2 classes are provided, a Dice class used for representing statistical data and simple arithmatics, and a Pool class which allows one to do custom operations based on the outcomes of multiple seperate dice (eg. keep the highest 3 of a pool of 4).  
### *Dice Example*:
Dice always finds the lowest number of faces to represent the dice, so a 6 sided dice
with equal amount of 1,2,3 on its faces becomes a d3
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
import DiceStatistics as tts
@tts.d('3:6, 1..2')
def mydice(outcome):
	if outcome == 4:
		return 4
	elif outcome > 4:
		return 3

funky_dice = mydice():
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