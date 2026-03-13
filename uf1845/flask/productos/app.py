from flask import Flask,render_template,request,redirect, url_for,send_from_directory
import sqlite3

app = Flask(__name__)
BD = "productos.sqlite"


def get_conection():
    cnx = sqlite3.connect(BD)
    cnx.row_factory = sqlite3.Row  # Para usar los nombres de columnas
    return cnx

def init_bd():
    conn = get_conection()
    conn.execute('''
    create table if not exists producto(
            id integer primary key autoincrement,
            codigo text unique not null,
            nombre text not null,
            precio real not null,
            cantidad integer not null,
            fecha_caducidad text not null
            )
    '''
    )
    conn.commit()
    conn.close()

# creamos la bd si no existe
init_bd()




@app.route('/')
def index():
    conn = get_conection()
    productos = conn.execute("select * from producto").fetchall()
    conn.close
    return render_template('index.html', prods=productos)

#Editar producto
@app.route('/editar/<int:id>', methods=['POST','GET'])
def editar(id):
    conn = get_conection()
    producto = conn.execute('select * from producto where id = ?',
                            (id,)).fetchone()
    
    if request.method == 'POST':
        codigo = request.form['codigo']
        nombre = request.form['nombre']
        precio = request.form['precio']
        cantidad = request.form['cantidad']
        fecha_caducidad = request.form['fecha_caducidad']

        conn.execute('''update producto set 
                    codigo=?, 
                    nombre=?, 
                    precio=?,
                    cantidad=?,
                    fecha_caducidad=?
                    where id=?
                    ''',
                    (codigo,nombre,precio,cantidad,fecha_caducidad,id)
                    )
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    
    conn.close()
    return render_template('editar.html', prod=producto)

# Borrar
@app.post('/borrar/<int:id>')
def borrar(id):
    conn = get_conection()
    conn.execute("delete from producto where id=?",(id,))

    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# Insertar

@app.route('/crear', methods=['POST','GET'])
def crear():
    if request.method == 'POST':
        codigo = request.form['codigo']
        nombre = request.form['nombre']
        precio = request.form['precio']
        cantidad = request.form['cantidad']
        fecha_caducidad = request.form['fecha_caducidad']

        conn = get_conection()
        conn.execute('''insert into producto(codigo,nombre,precio,cantidad,fecha_caducidad)
                    values (?,?,?,?,?)''',
                    (codigo,nombre,precio,cantidad,fecha_caducidad))
        
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    
    return render_template('crear.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    file.save('archivos/' + file.filename)
    file_url = url_for('uploaded_file',filename=file.filename, _external=True)
    return f'Archivo subido correctamente <br> Enlace: <a href="{file_url}">{file_url}</a>'

@app.route('/archivos/<filename>')
def uploaded_file(filename):
    return send_from_directory('archivos',filename)