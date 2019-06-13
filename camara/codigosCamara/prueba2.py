from vincenty import vincenty


boston = (-38.835831, -72.702263)
newyork	 = (-38.837626, -72.704261)
print vincenty(boston, newyork)*1000
