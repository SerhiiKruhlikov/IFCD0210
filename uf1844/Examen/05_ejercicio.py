inventario = {
    "manzanas": 10,
    "peras": 5,
    "naranjas": 8,
}

while True:
    print("\n--- MENÚ PRINCIPAL ---")
    print("1. Ver inventario")
    print("2. Agregar producto")
    print("3. Cambiar cantidad")
    print("4. Quitar producto")
    print("5. Salir")

    opcion = input("\nElegí una opción: ")

    if opcion == "1":
        if len(inventario) == 0:
            print("No hay productos")
        else:
            print("\n--- INVENTARIO ---")
            for producto in inventario:
                print(f"{producto}: {inventario[producto]} unidades")

    elif opcion == "2":
        producto = input("Nombre del producto: ").lower()
        if producto in inventario:
            print("Ese producto ya existe")
        else:
            try:
                cantidad = int(input("Cantidad: "))
                if cantidad >= 0:
                    inventario[producto] = cantidad
                    print("Producto agregado")
                else:
                    print("La cantidad no puede ser negativa")
            except:
                print("Número inválido")

    elif opcion == "3":
        producto = input("Qué producto querés actualizar: ").lower()
        if producto in inventario:
            try:
                nueva_cantidad = int(input("Nueva cantidad: "))
                if nueva_cantidad >= 0:
                    inventario[producto] = nueva_cantidad
                    print("Cantidad actualizada")
                else:
                    print("No puede ser negativa")
            except:
                print("Número inválido")
        else:
            print("Ese producto no existe")

    elif opcion == "4":
        producto = input("Producto a eliminar: ").lower()
        if producto in inventario:
            confirmar = input(f"Seguro que querés eliminar {producto}? (s/n): ")
            if confirmar == "s":
                del inventario[producto]
                print("Producto eliminado")
            else:
                print("No se eliminó")
        else:
            print("No existe ese producto")

    elif opcion == "5":
        print("Adiós!")
        break

    else:
        print("Opción incorrecta, elegí del 1 al 5")
