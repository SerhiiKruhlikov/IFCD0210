import time


# Decorador
def saludar_decorador(func):
    def nueva_funcion():
        print('Antes de la función')
        func()
        print('Después de la función')
    return nueva_funcion


@saludar_decorador
def saludar():
    print('hola mundo')


# saludo = saludar_decorador(saludar)

# saludo()
#saludar()


def medir_tiempo(func):
    def envoltura(*args, **kwargs):
        inicio = time.time()
        resultado = func(*args, **kwargs)
        fin = time.time()
        print(f"La función ha tardado {fin - inicio:.4f}")
        return resultado
    return envoltura


@medir_tiempo
def sumatorio(limite):
    total = 0
    for i in range(limite):
        total += i
        time.sleep(0.001)
    return total


x = sumatorio(1000)
print(f"Total: {x}")
