from dicechanics._strplot import str_plot


def test_strplot(d6):
	d = 2 @ d6
	string = str_plot(d, 20)
	assert (
		string
		== ' 2|### 2.78%\n 3|####### 5.56%\n 4|########## 8.33%\n 5|############# 11.11%\n 6|################# 13.89%\n 7|#################### 16.67%\n 8|################# 13.89%\n 9|############# 11.11%\n10|########## 8.33%\n11|####### 5.56%\n12|### 2.78%\n'

	)
