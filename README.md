# Dicechanics: Library for modelling dice mechanics
An library for python which provides an interface for modelling dice mechanics.  

## API Documentation
[Documentation on github pages](https://daplhall.github.io/dicechanics)
## Build and install
```bash
python -m build .
pip install dist\*.whl
```
## Usage
2 classes are provided, a Dice class used for representing statistical data and can perform simple arithmetics, and a Pool class which allows one to do custom linear operations based on the outcomes of multiple separate dice (it only takes 2 values at a time, thus the operation declaration is `lambda x,y: ...`

They are accessed through the `d(...)`, `z(...)`, `pool(...)` functions.

### *Dice parser*:
The dice class can take a sting input, that if follows a givens tructure expands into multiple numbers.
```python
d('1,2,3,4,5') # gives a dice with numbers 1 through 5
d('1..6:2, 2') # gives numbers 1 through 6 twice and an extra 2
d('1..4:4, 1:3, 1..2, 6') # is equivalent to the dict: {1:8,2:5,3:4,4:4,6:1}
```

### *Dice Example*:
Creating a dice which have the faces `1..6` and doing operations with it.
```python
d6 = d(6)
A = 2@d6 + 3 # roll 2 d6 add them, then add 3
B = d6-d6*d6/d6
C = A + B

prop = C.p # get probability of result
faces = C.f # get faces of result, 1:1 with probability
```
Mapping outcomes on a dice to create a new one.
```python
def filter(outcome):
    if outcome == 4:
        return 4
    elif outcome > 4:
        return 3

funky_dice = d('3:6,1..2').map(filter):
```
Which can also be written with a decorator
```python
@d('3:6, 1..2')
def mydice(outcome):
    if outcome == 4:
        return 4
    elif outcome > 4:
        return 3

funky_dice = mydice()
```

### *Pool Example*
Calculating the probabilities for getting the sum of the highest 3 of 3d6 and 2d10
```python
mypool = pool([d6]*3 + [d10]*2)
res = mypool[3:].perform(ops.add) # reduces the result to a dice representation
```
or through a decorator
```python
@pool([d6]*3 + [d10]*2)
def mypool(x, y):
    return x + y

res = mypool()
```

## Running benchmarks
To run the benchmarks and saving them.
```bash
pytest benchmarks --benchmark-autosave
```
to run specific tests in a file.
```bash
pytest benchmarks\test_bm_dice.py::<Benchmark>
```
to compare differnt runs
```bash
pytest-benchmark compare [ids,...]
```

## Running tests
The tests are executed by the following command.
```
pytest tests
```

## Building documentation
```bash
cd docs && mkdir build
sphinx-build -M html src build
```