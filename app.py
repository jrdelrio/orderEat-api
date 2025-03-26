import requests, os
from flask import Flask, request, jsonify
import resend

app = Flask(__name__)
    
@app.route("/api/intern-email", methods=["POST"])
def send_intern_email():
    data = request.json
    
    email_body = f"""
        <!DOCTYPE html>
        <html>
            <head>
                <meta charset="UTF-8">
            </head>
            <body>
                <h2>Equipo de OrderEAT, han recibido un mensaje a través del sitio web.</h2>
                    <h3>Los datos del contacto son:</h3>
                    <p>Nombre: <span style="color: red">{data['name']}</span></p>
                    <p>Colegio: <span style="color: red">{data['school']}</span></p>
                    <p>Cargo: <span style="color: red">{data['position']}</span></p>
                    <p>Correo: <span style="color: red">{data['email']}</span></p>
                    <p>Teléfono: <span style="color: red">{data['phone']}</span></p>
                    
                    <p>Mensaje:</p>
                    <p style="color: red">{data.get('message', '(Sin mensaje)')}</p>
            </body>
        </html>
    """
    
    resend.api_key = os.getenv("RESEND_API_KEY")

    try:
        params: resend.Emails.SendParams = {
        "from": "Acme <onboarding@resend.dev>", # mail de order eat
        "to": [data['email']],
        "subject": "Hemos recibido tu mensaje",
        "html": email_body,
    }
        print("✅ Correo enviado correctamente:")
        return jsonify({"message": "Correo enviado ✅"}), 200
    except Exception as e:
        print("❌ Error al enviar el correo:", str(e))
        return jsonify({"error": "No se pudo enviar el correo ❌"}), 500

@app.route("/api/send-email", methods=["POST"])
def send_email():
    data = request.json
    
    print(data)

    email_body = f"""
        Nombre: {data['name']}
        Colegio: {data['school']}
        Cargo: {data['position']}
        Correo: {data['email']}
        Teléfono: {data['phone']}
        Mensaje: {data.get('message', '(Sin mensaje)')}
    """
    
    resend.api_key = os.getenv("RESEND_API_KEY")

    params: resend.Emails.SendParams = {
        "from": "Acme <onboarding@resend.dev>", # mail de order eat
        "to": [data['email']],
        "subject": "Hemos recibido tu mensaje",
        "html": email_body,
    }
    
    
@app.route("/api/test-connection", methods=["GET"])
def test_connection():
    print("Received request to test connection")
    return jsonify({"status": "ok", "message": "Conexión exitosa con OrderEAT API 🚀"}), 200

if __name__ == "__main__":
    app.run(debug=True)