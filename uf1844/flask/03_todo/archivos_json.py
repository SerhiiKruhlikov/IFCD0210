import json

# with open('prueba.json', 'r', encoding='utf-8') as j:
#     txt = json.load(j)
#
# print(txt)
#
# txt.append({"nombre": "Serhii Kruhlikov", "libros": ["uno", "dos", "tres"]})
#
# with open('prueba.json', 'w', encoding='utf-8') as j:
#     json.dump(txt, j, indent=4, ensure_ascii=False)


with open('tareas.json', 'r', encoding='utf-8') as f:
    tareas = json.load(f)

nueva = {
    "id": 2,
    "description": "Segunda tarea",
    "fecha_alta": "2026-02-08 17:00:00",
    "fecha_completa": None
}

tareas.append(nueva)

with open('tareas.json', 'w', encoding='utf-8') as f:
    json.dump(tareas, f, indent=4, ensure_ascii=False)
