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
## Dicechanics: A module for dice operations and probability
This submodule exposes 3 classes
1. `Die` The base unit of statistics; Dice are immutable.
2. `Pool` Contains multiple dice which can be operated on together. (Currently not fully reimplemented)
3. `Bag` Contains multiple pools which can be operated on together (Currently not implemented)
### Sample usage
Consider you are playing your favorite tabletop roleplay in which you roll a 5 six sided dice (called a d6) and add the two highest, you simply write the following
```python
import ttstatistics.dicechanics as dc
pool = 5@dc.d6
print(dc.sum(pool[3:]))
```
Which produces
```cmd
Die with mu - 9.93, sigma - 14.30
---------------------------------
 2| 0.01%
 3| 0.06%
 4| 0.40%
 5|# 1.03%
 6|## 2.71%
 7|#### 5.21%
 8|######## 9.98%
 9|############# 15.43%
10|################## 21.81%
11|#################### 23.73%
12|################# 19.62%
```

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