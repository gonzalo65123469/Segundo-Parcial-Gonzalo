from flask import Flask, render_template, request, redirect, url_for, session
app = Flask(__name__)
app.secret_key = 'gonzalo123'  # Clave secreta para la sesión

# Ruta para la página principal (listado de productos)
@app.route('/')
def index():
    if 'productos' not in session:
        session['productos'] = []
    
    return render_template('index.html', productos=session['productos'])

# Ruta para agregar un nuevo producto
@app.route('/nuevo', methods=['GET', 'POST'])
def nuevo_producto():
    if request.method == 'POST':
        producto = {
            'id': len(session['productos']) + 1,
            'nombre': request.form['nombre'],
            'cantidad': int(request.form['cantidad']),
            'precio': float(request.form['precio']),
            'fecha_vencimiento': request.form['fecha_vencimiento'],
            'categoria': request.form['categoria']
        }
        session['productos'].append(producto)
        session.modified = True
        return redirect(url_for('index'))

    return render_template('nuevo.html')

# Ruta para editar un producto
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    producto = next((prod for prod in session['productos'] if prod['id'] == id), None)
    if not producto:
        return "Producto no encontrado", 404

    if request.method == 'POST':
        producto['nombre'] = request.form['nombre']
        producto['cantidad'] = int(request.form['cantidad'])
        producto['precio'] = float(request.form['precio'])
        producto['fecha_vencimiento'] = request.form['fecha_vencimiento']
        producto['categoria'] = request.form['categoria']
        session.modified = True
        return redirect(url_for('index'))

    return render_template('editar.html', producto=producto)

# Ruta para eliminar un producto
@app.route('/eliminar/<int:id>')
def eliminar_producto(id):
    session['productos'] = [prod for prod in session['productos'] if prod['id'] != id]
    session.modified = True
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
