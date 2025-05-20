from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz

db = SQLAlchemy()

def get_sao_paulo_time():
    sao_paulo_tz = pytz.timezone("America/Sao_Paulo")
    return datetime.now(sao_paulo_tz)

class Resultado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    data_criacao = db.Column(db.DateTime, default=get_sao_paulo_time)
    glicose = db.Column(db.Float)
    t3 = db.Column(db.Float)
    t4 = db.Column(db.Float)
    tsh = db.Column(db.Float)
    colesterol = db.Column(db.Float)
    triglicerideos = db.Column(db.Float)
    recomendacao = db.Column(db.Text)

    def _repr_(self):
        return f'<Resultado {self.id} - {self.nome}>'
