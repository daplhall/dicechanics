from typing import Callable, Any

type NumVector = list[float]
type BinaryFunc_T = Callable[[Any, Any], Any]
type UnaryFunc_T = Callable[[Any], Any]
type CompareFunc_T = Callable[[Any, Any], bool]