from dicechanics.math import gcd


def test_GCD():
	X = [15, 10, 20, 25]
	r = gcd(X[0], X[1])
	for i in X[2:]:
		r = gcd(r, i)
	assert r == 5
