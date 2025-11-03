from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hospedaje/<int:id>')
def detalle_hospedaje(id):
    return render_template('hospedajes/detalle.html')


@app.route('/reservas/consultar')
def consultar():
    return render_template('reservas/consultar.html')

@app.route('/reservas/checkout')
def reservas_checkout():
    return render_template('reservas/checkout.html')

@app.route('/perfil')
def perfil():
    return render_template('perfil/mis_reservas.html')


@app.route("/about") 
def about():
    return render_template("about.html")

@app.route("/aboutus")  
def aboutus():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact1.html")

@app.route("/service-detail")  
def service_detail():
    return render_template("service-detail.html")

# esta ruta de prueba para verificar  header y footer funciona bien ..
@app.route("/prueba")  
def prueba():
    return render_template("prueba.html")

@app.route("/faq")
def faq():
    return render_template("faq.html")

@app.route("/forgotpass")
def forgotpassword():
    return render_template("forgot-password.html")

@app.route("/gallery")
def gallery():
    return render_template("gallery1.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/roomlist")
def roomlist():
    return render_template("roomlist-2.html")

@app.route("/roomdetail")
def roomdetail():
    return render_template("detail-full.html")

@app.route("/availability")
def availability():
    return render_template("availability.html")

@app.route("/roomselect")
def roomselect():
    return render_template("room-select.html")

@app.route("/booking")
def booking():
    return render_template("booking.html")

@app.route("/checkout")
def checkout():
    return render_template("checkout.html")

@app.route("/confirmation")
def confirmation():
    return render_template("confirmation.html")

if __name__ == '__main__':
    # Ejecutar en modo debug para desarrollo
    app.run(host='0.0.0.0', port=5001, debug=True)
