import time

import icepool as ds

from ttstatistics.core.bag import Bag
from ttstatistics.core.genericmapping import GenericMapping
from ttstatistics.core.operations.macro import Operators
from ttstatistics.core.operations.micro import add

t = time.perf_counter()
q = GenericMapping(dict.fromkeys(range(1, 51), 1))
bag = Bag({q: 50})
b = Operators.performOnBag(bag, add)
print(time.perf_counter() - t)

q = ds.d(50).pool(50)
t = time.perf_counter()
q.sum()
print(time.perf_counter() - t)
