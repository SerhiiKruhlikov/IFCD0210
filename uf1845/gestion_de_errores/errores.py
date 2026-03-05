def escribe(numero):
    try:
        n = int(numero)
        z=4/n
        print(f"El número es {n}")
    except ValueError:
        print("Número no válido")
    except ZeroDivisionError as z:
        print("No se puede dividir entre cero: ", z)
    except Exception as e:
        print("Se produjo el error" ,e)

#escribe('0')


def lista_err():
    try:
        lista = [1,2,3]
        print(lista[1])
        x = 1/0
    except (IndexError,TypeError) as e:
        print("Error: ", e)
    except ZeroDivisionError:
        print("División por cero")
    finally:
        print("Tírate por el barranco")


#lista_err()

def archivo():
    try:
        arch = open("basura.txt","r")
    except FileNotFoundError:
        arch = open("basura.txt","w")
    finally:
        print("El archivo se ha creado si no existía")


#archivo()

def persona( edad):
    if edad < 18:
        raise ValueError("La edad debe ser más de 18")
    print("Bienvenido al club")


def llama_persona(edad): 
    
    try:
        assert edad > 18, "La edad debe ser más de 18"
        persona(edad)
    except ValueError:
        pass
    except AssertionError as e:
        print("Comprobando...",e)

llama_persona(1)