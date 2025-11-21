from collections import defaultdict
from dataclasses import dataclass, field
from enum import IntEnum, auto

from ttstatistics.utils.statemachine import StateMachine


def findNumberIndex(string: str):
	for i, char in enumerate(string):
		if not char.isdigit():
			return i


def multiplyKeyCount(mapping, multiplier):
	for key in mapping.keys():
		mapping[key] *= multiplier


class ParserStates(IntEnum):
	START = auto()
	CLEAN = auto()
	FIRST_CHAR = auto()
	EXPAND = auto()
	REPEAT = auto()
	END = auto()


@dataclass
class ParserMetaData:
	input_: str
	index: int = 0
	buffer: str = ""
	output: defaultdict[int] = field(default_factory=lambda: defaultdict(int))


def start(state: ParserStates, cargo: ParserMetaData):
	return ParserStates.FIRST_CHAR, cargo


def first_char(state: ParserStates, cargo: ParserMetaData):
	i = findNumberIndex(cargo.input_)
	cargo.buffer = cargo.input_[:i]
	cargo.index = i
	if i is None:
		cargo.output[int(cargo.buffer)] += 1
		return ParserStates.END, cargo
	elif cargo.input_[i : i + 2] == "..":
		return ParserStates.EXPAND, cargo
	elif cargo.input_[i : i + 1] == ":":
		return ParserStates.REPEAT, cargo


def expand(state: ParserStates, cargo: ParserMetaData):
	subInput = cargo.input_[cargo.index + 2 :]
	i = findNumberIndex(subInput)
	start = int(cargo.buffer)
	end = int(subInput[:i])
	for i in range(start, end + 1):
		cargo.output[i] += 1
	if subInput[i:]:
		return ParserStates.REPEAT, cargo
	else:
		return ParserStates.END, cargo


def repeat(state: ParserStates, cargo: ParserMetaData):
	if not cargo.output:
		cargo.output[int(cargo.buffer)] += 1
	subInput = cargo.input_[cargo.index + 1 :]
	timesToRepeat = int(subInput)
	multiplyKeyCount(cargo.output, timesToRepeat)
	return ParserStates.END, cargo


parser = StateMachine()
parser.setStartState(ParserStates.START)
parser.addState(ParserStates.START, start)
parser.addState(ParserStates.FIRST_CHAR, first_char)
parser.addState(ParserStates.EXPAND, expand)
parser.addState(ParserStates.REPEAT, repeat)
parser.addEndState(ParserStates.END)
