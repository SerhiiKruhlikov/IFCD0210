import turtle
import math


# Упражнение №2: буква S
t = turtle.Turtle()
t.shape('turtle')
t.width(2)
# t.goto(0, 0)
# t.forward(100)
# t.left(90)
# t.forward(100)
# t.left(90)
# t.forward(100)
# t.right(90)
# t.forward(100)
# t.right(90)
# t.forward(100)

# Упражнение №3: квадрат
# for _ in range(1, 5):
#     t.forward(100)
#     t.left(90)

# Упражнение №4: окружность
# for _ in range(1, 73):
#     t.forward(10)
#     t.left(5)

# Упражнение №5: больше квадратов
# for i in range(11):
#     offset = -5 * i
#     t.penup()
#     t.goto(offset, offset)
#     t.pendown()
#     for _ in range(1, 5):
#         width = 20 + offset * -2
#         t.forward(width)
#         t.left(90)

# Упражнение №6: паук
# for _ in range(12):
#     t.goto(0, 0)
#     t.pendown()
#     t.right(30)
#     t.forward(100)
#     t.stamp()
#     t.penup()

# Упражнение №7: спираль
# t.goto(0, 0)
#
# radians_per_step = 0.12
#
# for i in range(1, 360):
#     current_angle = i * radians_per_step
#     step = 1 + 0.5 * current_angle
#     t.forward(step)
#     t.left(math.degrees(radians_per_step))


# Упражнение №9: правильные многоугольники
offset = 20
side_length = 40
R = side_length * math.sqrt(3) / 3

for n in range(3, 13):
    start_angle = 90 + 360 / n / 2

    if n > 3:
        R += offset
        side_length = 2 * R * math.sin(math.pi / n)
        t.forward(offset)
    elif n == 3:
        t.forward(R)

    t.left(start_angle)

    for i in range(n):
        t.forward(side_length)
        t.left(360 / n)

    t.left(-start_angle)


turtle.done()
