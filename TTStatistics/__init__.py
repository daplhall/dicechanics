__all__ = []

## With all you only get the base functionality, ie the Dice class and the standard dice
from .dice import *
__all__.extend(dice.__all__)

#from .            import Cyberpunk
#from .            import DnD5e
