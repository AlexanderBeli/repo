# даны координаты попадания дротика на поле игры дартс
# определить количество очков

# радиус 1 круга - 5 см
# радиус 2 круга - 10 см
# радиус 3 круга - 15 см

x = float(input())
y = float(input())
# уравнение окружности

if x**2 + y**2 < 25:
    print(100)
elif x**2 + y**2 < 100:
    print(50)
elif x**2 + y**2 < 225:
    print(20)
else:
    print(0)
