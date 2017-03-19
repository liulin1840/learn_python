def triangles():
    L = [1]
    while True:
        yield L
        L.append(0)
        L = [L[i - 1] + L[i] for i in range(len(L))]

def fib(max):
    result  = [0,1]
    n=0
    while n < max:
        a, b = result[-2],result[-1]+result[-2]
        result.append(b)
        n = n + 1
    return result

if __name__ == '__main__':
	print(fib(6))
	n = 0
	for t in triangles():
	    print(t)
	    n = n + 1	
	    if n == 10:
	        break