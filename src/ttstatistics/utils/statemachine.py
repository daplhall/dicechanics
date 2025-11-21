from collections.abc import Callable, Hashable
from typing import Any

type StateFunction = Callable[[Hashable, Any], [Hashable, Any]]


class StateMachine:
	def __init__(self):
		self.states = {}
		self.start: Any = None
		self.endStates = []

	def run(self, cargo):
		assert self.endStates is not None
		assert self.start is not None

		state = self.start
		while state not in self.endStates:
			function = self.states[state]
			state, cargo = function(state, cargo)
		return cargo

	def addState(self, state: Hashable, function: StateFunction):
		self.states[state] = function

	def setStartState(self, State):
		self.start = State

	def addEndState(self, state: Hashable):
		self.endStates.append(state)
