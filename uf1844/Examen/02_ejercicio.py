print("\n--- LISTA DE 5 NÚMEROS ---")

numeros = []

for i in range(5):
    numeros.append(float(input(f"Número {i+1}: ")))


print(f"\nLista: {numeros}")
print(f"Mayor: {max(numeros)}")
print(f"Menor: {min(numeros)}") 
print(f"Suma: {sum(numeros)}")
