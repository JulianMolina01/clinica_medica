from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

from flask import make_response, Response
import pdfkit 

from flask_mail import Mail
from flask_mail import Message

app = Flask(__name__)

app.config['MAIL_SERVER']='sandbox.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = 'softwaretestmolina@gmail.com'
app.config['MAIL_PASSWORD'] = 'softwaretestm'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)

app.secret_key = 'clave_secreta'

mydb = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '123Password123',
    database = 'clinica'
)


@app.route('/templates/dashboard.html')
def dashboard():
    if 'nombre' in session:

        pacientes = []
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM pacientes")
        pacientes = mycursor.fetchall()

        return render_template('/dashboard.html', nombre=session['nombre'], pacientes = pacientes)
    else:
        return redirect(url_for('login'))

@app.route('/templates/login.html', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM login WHERE usuario = %s AND password = %s", (email, password))
        usuario = mycursor.fetchone()
        print("======= %s", usuario)
        if usuario:
            session['nombre'] = usuario[1]
            return redirect(url_for('dashboard'))
        else:
            return render_template('/login.html', mensaje = 'Email o Contraseña incorrectos, intente de nuevo por favor.')
    else:
        return render_template('/login.html')
    
@app.route('/logout')
def logout():
    session.pop('nombre', None)
    return redirect(url_for('login'))

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        email = request.form['email']
        contra = request.form['password']
        repite_contra = request.form['password_dos']
        if contra== repite_contra:
            mycursor = mydb.cursor()
            mycursor.execute("SELECT * FROM login WHERE usuario = %s", (email,))
            resultado = mycursor.fetchone()
            if resultado:
                # El registro ya existe, enviar un mensaje y redirigir al usuario
                return render_template('/registro.html', mensaje = 'El registro ya existe!')
            else:
                mycursor.execute("INSERT INTO login (usuario, password) VALUES (%s, %s)", (email, contra))
                mydb.commit()
                return render_template('/registro.html', mensaje = 'Cuenta creada con exito!')
        else:
            return render_template('/registro.html', mensaje = 'Las contraseñas no coinciden :(')
    else:
        return render_template('/registro.html')



@app.route('/registro_paciente', methods=['GET', 'POST'])
def registro_paciente():
    if request.method == 'POST':
        ap = request.form['ap']
        am = request.form['am']
        noms = request.form['nombres']
        edad = request.form['edad']
        tel = request.form['telefono']
        email = request.form['email']
        dir = request.form['dir']
        contra = '123'
        repite_contra = '123'
        if contra== repite_contra:
            mycursor = mydb.cursor()
            mycursor.execute("SELECT * FROM pacientes WHERE correo = %s", (email,))
            resultado = mycursor.fetchone()
            if resultado:
                # El registro ya existe, enviar un mensaje y redirigir al usuario
                
                return redirect(url_for('dashboard'))
            else:
                mycursor.execute("INSERT INTO pacientes (apellido_paterno, apellido_materno, nombres, edad, telefono, correo, direccion) VALUES (%s, %s, %s, %s, %s, %s, %s)", (ap, am, noms, edad, tel, email, dir))
                mydb.commit()
                return redirect(url_for('dashboard'))
        else:
            return render_template('/registro.html', mensaje = 'Las contraseñas no coinciden :(')
    else:
        return render_template('/dashboard.html')



@app.route('/eliminar_paciente/<id>/')
def eliminar_paciente(id):
    mycursor = mydb.cursor()
    query = f"DELETE FROM pacientes WHERE id = {id}"
    mycursor.execute(query)
    mydb.commit()
    return redirect(url_for('dashboard'))


@app.route('/actualizar_paciente', methods=['GET', 'POST'])
def actualizar_paciente():
    id = request.args.get('id') 
    pacientitos = []
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM pacientes WHERE Id =  %s" %id)
    pacientitos = mycursor.fetchall()
    return render_template('/actualizar_paciente.html', pacientitos = pacientitos)

@app.route('/actualizar', methods=['GET', 'POST'])
def actualizar():
    if request.method == 'POST':
        idu = request.form['id']
        ap = request.form['ap']
        am = request.form['am']
        noms = request.form['nombres']
        edad = request.form['edad']
        tel = request.form['telefono']
        email = request.form['email']
        dir = request.form['dir']
        contra = '123'
        repite_contra = '123'
        if contra== repite_contra:
            mycursor = mydb.cursor()
            mycursor.execute("UPDATE pacientes SET apellido_paterno = %s, apellido_materno = %s, nombres = %s, edad = %s, telefono = %s, correo = %s, direccion = %s WHERE Id = %s",
                       (ap, am, noms, edad, tel, email, dir, idu))
            resultado = mycursor.fetchone()
            mydb.commit()
            print(resultado)
            return redirect(url_for('dashboard'))
        
@app.route('/datos_paciente', methods=['GET', 'POST'])
def datos_paciente():
    id = request.args.get('id') 
    datos_paciente = []
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM pacientes WHERE Id =  %s" %id)
    datos_paciente = mycursor.fetchall()
    res = render_template('/datos_paciente.html', datos_paciente = datos_paciente)
    response_string = pdfkit.from_string(res, False)
    response = make_response(response_string)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline;filename=datos_paciente.pdf'
    return response



@app.route('/templates/citas.html')
def citaspage():
    if 'nombre' in session:

        pacientes = []
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM citas")
        pacientes = mycursor.fetchall()

        return render_template('/citas.html', nombre=session['nombre'], pacientes = pacientes)
    else:
        return redirect(url_for('login'))
@app.route('/registro_cita', methods=['GET', 'POST'])
def registro_cita():
    if request.method == 'POST':
        nom = request.form['nom']
        tel = request.form['tel']
        email = request.form['email']
        sintomas = request.form['sintomas']
        fecha = request.form['fecha']
        depto = request.form['depto']
        gen = request.form['gen']
        hora = request.form['hora']
        contra = '123'
        repite_contra = '123'
        if contra== repite_contra:
            mycursor = mydb.cursor()
            mycursor.execute("INSERT INTO citas (NombreP, NTelefono, Email, Sintomas, Fecha, Depto, Genero, Hora) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (nom, tel, email, sintomas, fecha, depto, gen, hora))
            mydb.commit()
            return redirect(url_for('citaspage'))
        else:
            return render_template('/citas.html', mensaje = 'Las contraseñas no coinciden :(')
    else:
        return render_template('/citas.html')
@app.route('/datos_citapaciente', methods=['GET', 'POST'])
def datos_citapaciente():
    id = request.args.get('id') 
    datos_paciente = []
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM citas WHERE Id =  %s" %id)
    datos_paciente = mycursor.fetchall()
    res = render_template('/datos_citapaciente.html', datos_paciente = datos_paciente)
    response_string = pdfkit.from_string(res, False)
    response = make_response(response_string)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline;filename=datos_paciente.pdf'
    return response

@app.route('/eliminar_cita/<id>/')
def eliminar_cita(id):
    mycursor = mydb.cursor()
    query = f"DELETE FROM citas WHERE id = {id}"
    mycursor.execute(query)
    mydb.commit()
    return redirect(url_for('citaspage'))

@app.route('/enviar_mail', methods=['GET', 'POST'])
def enviar_mail():
    id = request.args.get('id') 
    pacientitos = []
    mycursor = mydb.cursor()
    mycursor.execute("SELECT email FROM citas WHERE id =  %s" %id)
    pacientitos = mycursor.fetchall()
    if pacientitos is not None:
        print(pacientitos[0])
        msg = Message('Clinica Medica - Cita Medica', sender =   'softwaretestmolina@gmail.com', recipients = ['%s', pacientitos[0]])
        msg.body = "Tiene usted una cita hoy en CLINICA MEDICA"
        mail.send(msg)
    return redirect(url_for('sentmail'))

@app.route('/templates/sentmail.html')
def sentmail():
    return render_template('/sentmail.html')

@app.route('/')
def home():
    return render_template('/index.html')
@app.route('/templates/citas.html')
def citas():
    return render_template('/citas.html')
@app.route('/templates/servicios.html')
def servicios():
    return render_template('/servicios.html')
@app.route('/templates/pacientes.html')
def pacientes():
    return render_template('/pacientes.html')
@app.route('/templates/contacto.html')
def contacto():
    return render_template('/contacto.html')


if __name__ == '__main__':
    app.run(port=4000, host='0.0.0.0')