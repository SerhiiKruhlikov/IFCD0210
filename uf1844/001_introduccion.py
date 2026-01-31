# Calcular el precio con IVA de un producto

precio_producto = 32.18
porcentaje_iva = 0.21

precio_total = precio_producto * (1 + porcentaje_iva)

# print("El precio total es: ", precio_total)
# print("El precio total es:", precio_total, sep=' ')
print("El precio total es: " + str(precio_total))

# ----------------

# Convertir de grados Celsius a Fahrenheit
# F = C * 1.8 + 32

grados_celsius = -17
grados_fh = grados_celsius * 1.8 + 32
# print(grados_celsius, '--->', grados_fh)
mensaje = str(grados_celsius) + " Grados Celsius son " + str(grados_fh) + " Grados Fh"
print(mensaje)

# ----------------

# Calcular el indice de masa corporal
# IMC = Peso(kg) / altura ** 2
# imc < 18 : bajo
# 18 < imc < 25: normal
# imc > 25 : sobrepeso

peso = 87
altura = 1.9
imc = peso / altura ** 2

print(imc)

if imc < 18:
    print("IMC es: ", imc, ", es Bajo")
elif 18 < imc < 25:
    print("IMC es: ", imc, ", es Normal")
else:
    print("sobrepeso")
