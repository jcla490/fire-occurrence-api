def fn(num):
    vals, counter = 0, 0
    even_nums = []
    while True:
        if vals < num:
            counter += 2
            even_nums.append(counter)
            vals += 1
        else:
            print(even_nums)

            return sum(even_nums)
    
e = fn(200)
print(e)