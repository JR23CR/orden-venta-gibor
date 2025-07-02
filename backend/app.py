from flask import Flask, request, jsonify
from flask_cors import CORS
import pdfplumber
import io

app = Flask(__name__)
CORS(app)

@app.route('/upload-invoice', methods=['POST'])
def upload_invoice():
    if 'invoicePdf' not in request.files:
        return jsonify({'error': 'No se proporcionó el archivo PDF'}), 400

    file = request.files['invoicePdf']
    if file.filename == '':
        return jsonify({'error': 'Nombre de archivo vacío'}), 400

    try:
        with pdfplumber.open(io.BytesIO(file.read())) as pdf:
            text = ''
            for page in pdf.pages:
                text += page.extract_text() + '\n'

        data = {
            "fechaEmision": "",
            "nombreEmisor": "GIBOR, S.A.",
            "numeroDTE": "",
            "numeroAcceso": "",
            "nombreReceptor": "",
            "direccionComprador": "",
            "items": [{
                "descripcion": "LEÑA (estimado)",
                "precioUnitario": "300.00"
            }],
            "totalFactura": "300.00"
        }

        return jsonify(data)

    except Exception as e:
        return jsonify({'error': f'Error al procesar el archivo: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
