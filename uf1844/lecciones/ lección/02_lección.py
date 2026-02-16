for x in 1, 5, 2, 4, 3:
    print(x ** 2)


for x in "comprobar":
    print(x)


for x in range(1, 11, 2):
    print(x)

z = range(1, 11, 2)

print(type(z))

print(len(z))


def p3(string: object) -> object:
    print(x)
    print(x)
    print(x)


x = p3("saludos")

print(type(x))


def f(uno: int, dos: int) -> int:
    return uno + dos


print(f(1, f(2, 3)))

print(f("1", f("2", "3")))

print(f.__name__)
print(f)
