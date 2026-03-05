def area_rectangulo(base, altura):
    return base * altura


print("\n--- CALCULADORA DE ÁREA ---")

while True:
    try:
        base = float(input("Base del rectángulo: "))
        if base > 0:
            break
        else:
            print("La base tiene que ser positiva")
    except:
        print("Eso no es un número válido")


while True:
    try:
        altura = float(input("Altura del rectángulo: "))
        if altura > 0:
            break
        else:
            print("La altura tiene que ser positiva")
    except:
        print("Eso no es un número válido")

resultado = area_rectangulo(base, altura)
print(f"\nEl área es: {resultado}")
