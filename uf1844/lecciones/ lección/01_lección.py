print("Como te llamas?")
name = input()
print("Рад познакомится, ", name, "!", sep="")
age = int(input("Cuantos años tienes" + name + "?"))
x = age + 1
print("А я думал, тебе", x, end="")

if 11 <= x <= 19:
    print("лет")
elif x % 10 == 1:
    print("год")
elif 2 <= x % 10 <= 4:
    print("года")
else:
    print("лет")
print("!")

