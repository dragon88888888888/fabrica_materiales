from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fabrica.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Material(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    descripcion = db.Column(db.String(200))

@app.before_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    materiales = Material.query.all()
    return render_template('index.html', materiales=materiales)

@app.route('/add', methods=['GET', 'POST'])
def add_material():
    if request.method == 'POST':
        nombre = request.form['nombre']
        cantidad = request.form['cantidad']
        descripcion = request.form.get('descripcion')

        nuevo_material = Material(nombre=nombre, cantidad=cantidad, descripcion=descripcion)
        db.session.add(nuevo_material)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('add_material.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_material(id):
    material = Material.query.get_or_404(id)

    if request.method == 'POST':
        material.nombre = request.form['nombre']
        material.cantidad = request.form['cantidad']
        material.descripcion = request.form.get('descripcion')

        db.session.commit()
        return redirect(url_for('index'))

    return render_template('edit_material.html', material=material)

@app.route('/delete/<int:id>')
def delete_material(id):
    material = Material.query.get_or_404(id)
    db.session.delete(material)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
