def cube(n):
    return n*n*n

def generate_cubes(n):
    return [cube(i) for i in range(n+1)]

def generate_bender_numbers(n):
    bender_numbers = {}
    cubes = generate_cubes(n)

def generate_pairs(n):
    for i in range(n):
        row = []
        #a^3+b^3 === b^3+a^3 so only need to generate half the pairs since (8, 9) will === (9,8)
        for j in range(i, n):
             row.append((i, j))
        print(row)


print(generate_cubes(10))
rdict = {}
rdict[(1,1)] = cube(1) + cube(1)
print(rdict)
generate_pairs(10)