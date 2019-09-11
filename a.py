

m=0
def a():
	a=1
	b=2
	return a,b
	
def aa(a,b):
	global m
	m=1
	print(a,b)
	

a1,a2=a()
aa(a1,a2)
print(m)
