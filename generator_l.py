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
# yield 产出之意 跳出 origin 起源 定义函数：
#函数名 参数 找到一个人，给他一些东西让他帮你办事
#for 就是挨个找，break 就是不找了，累了
#重要的是函数的执行流程 从哪进去 从哪儿出来 改变了些什么
#循环变量就是拿来计数的，找一个写一个，
#将抽象的东西变为形象，方便记忆与理解


