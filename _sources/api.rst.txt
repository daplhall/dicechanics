API
==================
Through out this documentation the work unit is used to refer to the current type you are look at.  
When you import dicehancis you get the following imported

.. py:module:: dicechanics

.. autofunction:: dicechanics.d
.. autofunction:: dicechanics.z
.. autofunction:: dicechanics.pool

.. py:data:: d4

   A 4 sided die

.. py:data:: d6

   A 6 sided die

.. py:data:: d8

   A 8 sided die

.. py:data:: d10

   A 10 sided die

.. py:data:: d12

   A 12 sided die

.. py:data:: d20

   A 20 sided die

.. py:data:: d100

   A 100 sided die

.. py:data:: z9

   A 10 sided die with values [0..9]

.. autoclass:: dicechanics::Die
   :members:
   :undoc-members: 
   :special-members: __add__, __radd__, __sub__, __rsub__, __mul__, __rmul__, __truediv__, __flordiv__, __lt__, __ge__, __gt__, __eq__, __ne__, __neg__, __call__ , __rmatmul__, __matmul__
   :inherited-members: UserDict
   :member-order: groupwise
   :exclude-members: setdefault, __weakref__, __str__, __repr__, __new__


.. autoclass:: dicechanics::Pool
   :special-members:
   :members:
   :member-order: bysource
   :exclude-members:  __weakref__, __str__, __repr__

