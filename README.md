# Tabletop statistics
Tabletop Statistics is a small library to help one explore or develop new tabletop games which involve some random element.

Currently, it only contains dicechanics, which is a general purpose statistcical library, which allows one to find exact statistics for arbitary operations on pools of arbitary dice.  

In the future it will also contain deckchanics for exploring the statistics of card games.

## Documentation and examples
[Documentation and examples on GitHub pages](https://daplhall.github.io/dicechanics)

## A taste of dicechanics
Dicechanics exposes an API that allows one with a few lines to get statsitical data of dice operations. Consider you are playing your favorite tabletop roleplaying system in which you roll five six-sided dice and add the two highest, you write the following
```python
import ttstatistics.dicechanics as ds

pool = 5 @ ds.d(6)
print(ds.sum(pool[-2:]))
```
Output:
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
# Bulding
## Build and install
```bash
git clone <TTstatistics>
cd TTstatistics
pip install .
```
## Building documentation
```bash
cd docs && mkdir build
sphinx-build -M html src build
```
Remember to install its `requirements.txt` when code updates

## Running benchmarks
To run the benchmarks and save them.
```bash
pytest benchmarks --benchmark-autosave
```
To run specific tests in a file.
```bash
pytest benchmarks\test_bm_dice.py::<Benchmark>
```
to compare different runs
```bash
pytest-benchmark compare [ids,...]
```

## Running tests
Tests are executed by the following:
```
pytest tests
```

# Building UMl
```
plantuml -f png --output-dir png src/**/*.puml
```