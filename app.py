from flask import Flask, render_template, request
import os
from database import db, Resultado
from pdf_extractor import buscar_resultados
from recommenderlm import recomendar_dieta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///resultados.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    nome = request.form.get('nome', 'Desconhecido')
    file = request.files.get('pdfExame', None)

    if file and file.filename.endswith('.pdf'):
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])

        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        resultados = buscar_resultados(filepath)
        if resultados is None:
            resultados = {}

        colesterol = float(resultados.get("colesterol") or 0)
        glicose = float(resultados.get("glicose") or 0)
        t3 = float(resultados.get("t3") or 0)
        t4 = float(resultados.get("t4") or 0)
        tsh = float(resultados.get("tsh") or 0)
        triglicerideos = float(resultados.get("triglicerideos") or 0)

    else:
        colesterol = float(request.form.get('colesterol_total') or 0)
        glicose = float(request.form.get('glicose') or 0)
        t3 = float(request.form.get('t3') or 0)
        t4 = float(request.form.get('t4') or 0)
        tsh = float(request.form.get('tsh') or 0)
        triglicerideos = float(request.form.get('triglicerideos') or 0)

        resultados = {
            "colesterol": colesterol,
            "glicose": glicose,
            "t3": t3,
            "t4": t4,
            "tsh": tsh,
            "triglicerideos": triglicerideos
        }

    dados = {
        "Colesterol": {"valor": colesterol},
        "Glicose": {"valor": glicose},
        "T3": {"valor": t3},
        "T4": {"valor": t4},
        "TSH": {"valor": tsh},
        "Triglicerídeos": {"valor": triglicerideos}
    }

    recomendacao = recomendar_dieta(dados)

    novo_resultado = Resultado(
        nome=nome,
        colesterol=colesterol,
        glicose=glicose,
        t3=t3,
        t4=t4,
        tsh=tsh,
        triglicerideos=triglicerideos,
        recomendacao=recomendacao
    )
    db.session.add(novo_resultado)
    db.session.commit()
    
    return render_template('valoresCalculados.html', dados=resultados, recomendacoes=recomendacao, nome=nome)

if __name__ == '__main__':
    app.run(debug=True)
