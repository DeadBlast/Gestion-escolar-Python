__author__ = 'jujoj'
import sqlite3
from flask import Flask, render_template, request,redirect
import configparser
config = configparser.ConfigParser()
try:
    config.read('config.cfg')
    ip=config['datos']['ip']
    port=int(config['datos']['port'])
except:
    print("Creando configuraciones....")
    config['datos'] = {'ip' : 'localhost' , 'port' : '5000'}
    with open('config.cfg', 'w') as archivoconfig:
        config.write(archivoconfig)
    config.read('config.cfg')
    ip=config['datos']['ip']
    port=int(config['datos']['port'])
#Conectamos con la base de datos
con = sqlite3.connect('estudiantes.db')
#Intentamos crear la base datos si es que no existe
try:
    con.execute('CREATE TABLE alumnos (id integer primary key AUTOINCREMENT ,nombre TEXT, curp TEXT,'
                'edad TEXT,matricula TEXT,grado TEXT,sexo TEXT, padre TEXT, curpp TEXT, dir TEXT, calle TEXT,'
                'escolaridad TEXT,ocup TEXT, tel TEXT, correo TEXT, red TEXT)')
    print("Creando base de datos....")
    con.close()
except:
    con.close()
#Buscamos las configuraciones
app = Flask(__name__)
#Pagina de inicio
@app.route('/')
def index():
    return render_template('index.html')
#Pagina para añadir nuevos alumnos
@app.route('/agregar')
def add():
    return render_template('agregar.html')
@app.route('/agregar',methods=['POST','GET'])
#Funcion que añade alumnos
def addrec():
    if request.method=='POST':
        try:
            nombre = request.form['nombre'].upper()
            curp = request.form['curp'].upper()
            edad = request.form['edad'].upper()
            matricula = request.form['matricula'].upper()
            grado=request.form['grado']
            sexo=request.form['sexo'].upper()
            padre=request.form['padre'].upper()
            curpp=request.form['curpp'].upper()
            dir=request.form['dir'].upper()
            calle=request.form['calle'].upper()
            escolaridad=request.form['escolaridad'].upper()
            ocup=request.form['ocup'].upper()
            tel=request.form['tel']
            correo=request.form['correo'].upper()
            red=request.form['red'].upper()
            con=sqlite3.connect("estudiantes.db")
            cur=con.cursor()
            datos=[nombre,curp,edad,matricula,grado,sexo,padre,curpp,dir,calle,escolaridad,ocup,tel,correo,red]
            cur.execute("INSERT INTO alumnos VALUES(NULL,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", datos)
            con.commit()
            con.close()
            msg="Alumno añadido con exito!"
            return render_template('resultado.html',msg=msg)
        except:
            msg="No se pudo añadir al usuario!"
            return render_template('resultado.html',msg=msg)
#Funcion que mostrara a todos los alumnos
@app.route('/lista')
def list():
   con = sqlite3.connect("estudiantes.db")
   con.row_factory = sqlite3.Row
   cur = con.cursor()
   cur.execute("select * from alumnos order by nombre COLLATE nocase")

   rows = cur.fetchall();
   if rows==[]:
       msg= "No hay datos aun!"
       return render_template('resultado.html',msg=msg)
   else:
       return render_template("lista.html",rows = rows)
@app.route('/buscar')
def buscador():
    return render_template('busqueda.html')
@app.route('/user/')
@app.route('/user/<id>')
def userinfo(id=None):
    if id is None:
        return 'No hay nada'
    else:
         con=sqlite3.connect('estudiantes.db')
         con.row_factory = sqlite3.Row
         cur=con.cursor()
         par=(id,)
         cur.execute("SELECT * FROM alumnos WHERE id=?",par)
         row = cur.fetchone()
         return render_template("ver.html",row=row)
@app.route('/editar/')
@app.route('/editar/<id>')
def useredit(id=None):
    if id is None:
        return 'No hay nada'
    else:
         con=sqlite3.connect('estudiantes.db')
         con.row_factory = sqlite3.Row
         cur=con.cursor()
         par=(id,)
         cur.execute("SELECT * FROM alumnos WHERE id=?",par)
         row = cur.fetchone()
         return render_template("editar.html",row=row)
@app.route('/editar/',methods=['POST','GET'])
def editrec():
    if request.method == 'POST':
        try:
            id=request.form['id']
            nombre = request.form['nombre'].upper()
            curp = request.form['curp'].upper()
            edad = request.form['edad'].upper()
            matricula = request.form['matricula'].upper()
            grado=request.form['grado']
            sexo = request.form['sexo'].upper()
            padre = request.form['padre'].upper()
            curpp = request.form['curpp'].upper()
            dir = request.form['dir'].upper()
            calle = request.form['calle'].upper()
            escolaridad = request.form['escolaridad'].upper()
            ocup = request.form['ocup'].upper()
            tel = request.form['tel']
            correo=request.form['correo'].upper()
            red=request.form['red'].upper()
            con = sqlite3.connect("estudiantes.db")
            cur = con.cursor()
            datos = [nombre, curp, edad, matricula, grado, sexo, padre, curpp, dir, calle, escolaridad, ocup, tel,correo,red,id]
            cur.execute("UPDATE alumnos SET nombre=?,curp=?,edad=?,matricula=?,grado=?,sexo=?,padre=?,curpp=?,dir=?,calle=?,escolaridad=?,ocup=?,tel=?,correo=?,red=? WHERE id=?",datos)
            con.commit()
            con.close()
            return redirect("/user/"+str(id))
        except:
            msg = "No se pudo actualizar la informacion! :("
            return render_template('resultado.html', msg=msg)
@app.route('/eliminar/')
@app.route('/eliminar/<id>')
def eliminarpage(id=None):
    if id is None:
        return "Nada"
    else:
        return render_template('eliminar.html',id=id)
@app.route('/eliminar/',methods=['POST','GET'])
def eliminar():
    if request.method=='POST':
        try:
            borrar=request.form['borrar']
            id=(request.form['id'],)
            if borrar=='no':
                return redirect('/user/'+str(id[0]))
            else:
                con=sqlite3.connect('estudiantes.db')
                cur=con.cursor()
                cur.execute("delete from alumnos where id=?",id)
                con.commit()
                con.close()
                msg='Borrado con exito!'
                return render_template('resultado.html',msg=msg)
        except:
            return 'lol'


@app.route('/buscar',methods=['POST','GET'])
def buscar():
    if request.method=='POST':
        try:
            busqueda=request.form['busqueda']
            if busqueda=='1':
                input=request.form['input']
                con=sqlite3.connect('estudiantes.db')
                con.row_factory = sqlite3.Row
                par=(input,)
                cur=con.cursor()
                cur.execute("select * from alumnos where grado=? order by nombre collate nocase",par)
                rows=cur.fetchall()
                if rows == []:
                    msg = "Aun no hay alumnos en el grupo: " + str(input)
                    return render_template('resultado.html', msg=msg)
                else:
                    return render_template("lista.html", rows=rows)
            else:
                campo=request.form['campo']
                input = request.form['input'].upper()
                con=sqlite3.connect("estudiantes.db")
                con.row_factory = sqlite3.Row
                cur=con.cursor()
                par=("%"+input+"%")
                text="SELECT * FROM alumnos WHERE "+campo+" like '"+par+"' order by nombre collate nocase"
                cur.execute(text)
                rows = cur.fetchall()
            if rows==[]:
                msg="No se ha encontrado resultados para la busqueda: "+str(input)
                return render_template('resultado.html',msg=msg)
            else:
                return render_template("lista.html",rows = rows)
        except:
            return 'Ha ocurrido un error!'
@app.route('/about')
def about():
    return redirect('http://deadblast.xyz/')
if __name__ == '__main__':
   app.run(host=ip,port=port,debug=True)
