from ttstatistics.core.operations import add, mul
from ttstatistics.core.operations import (
	max as max_,
)
from ttstatistics.core.operations import (
	min as min_,
)
from ttstatistics.core.operations import perform as performCore
from ttstatistics.dicechanics import protocols
from ttstatistics.dicechanics.die import Die
from ttstatistics.dicechanics.statisticals.factory import createStatistical


def perform(pool: protocols.Pool, function) -> protocols.Die:
	statistical = createStatistical(performCore(pool, function))
	return Die(statistical)


def sum(pool: protocols.Pool) -> protocols.Die:
	"""
	Function that sums the pool outcomes.

	Parameters
	----------
	pool: Pool

	Returns
	-------
	out: Die
	"""
	return perform(pool, add)


def mult(pool: protocols.Pool) -> protocols.Die:
	"""
	Function that multiplies the pool outcomes.

	Parameters
	----------
	pool: Pool

	Returns
	-------
	out: Die
	"""
	return perform(pool, mul)


def max(pool: protocols.Pool) -> protocols.Die:
	"""
	Function that takes the max of the pool outcomes.

	Parameters
	----------
	pool: Pool

	Returns
	-------
	out: Die
	"""
	return perform(pool, max_)


def min(pool: protocols.Pool) -> protocols.Die:
	"""
	Function that takes the min of the pool outcomes.

	Parameters
	----------
	pool: Pool

	Returns
	-------
	out: Die
	"""
	return perform(pool, min_)
