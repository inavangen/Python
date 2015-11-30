import timeit
timer = timeit.Timer(stmt="a+=1", setup="a=0")
time = timer.timeit(number=10000)
times = timer.repeat(repeat=5, number= 10000)
print times