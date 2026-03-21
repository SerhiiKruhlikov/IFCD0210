# script_generar_hash.py
from werkzeug.security import generate_password_hash

# Configuración
email = "juan@example.com"
password = "mi_password_123"  # Cambia esto por la contraseña que quieras

# Generar el hash
pw_hash = generate_password_hash(password)

print(f"Email: {email}")
print(f"Password: {password}")
print(f"Hash generado: {pw_hash}")
print()
print("SQL para insertar usuario:")
print(f"""
INSERT INTO usuarios (nombre, email, pw_hash, rol, f_alta) 
VALUES ('Juan Pérez', '{email}', '{pw_hash}', 'user', '2024-01-15');
""")