from ttstatistics.utils._plot import StringPlot


def test_BarsPlot(d4):
	plot = StringPlot.bars(d4.keys(), d4.values())
	assert plot == (
		"1|#################### 0.25\n2|#################### 0.25\n3|######"
		"############## 0.25\n4|#################### 0.25\n"
	)
