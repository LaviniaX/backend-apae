from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from config import Config
import os

# --- Configuração do Aplicativo Flask ---
app = Flask(__name__)
app.config.from_object(Config)

# Inicializar o SQLAlchemy
db = SQLAlchemy(app)

# Importar os modelos APÓS db ser inicializado
from models import Usuario, Paciente, Prontuario, TipoUsuario
from datetime import date, datetime

# --- Registrar Blueprints (Controladores) ---
from controllers.user_controller import user_bp
from controllers.patient_controller import patient_bp
from controllers.medical_record_controller import medical_record_bp

app.register_blueprint(user_bp)
app.register_blueprint(patient_bp)
app.register_blueprint(medical_record_bp)

# --- Rota Principal (Controlador) ---
@app.route('/')
def index():
    # Esta é uma rota "de entrada" ou dashboard
    # Ela pode exibir um resumo ou links para as outras seções
    return render_template('dashboard.html') # Você precisará criar este template

# --- Funções de Inicialização ---
def create_db_tables():
    with app.app_context():
        db.create_all()
        print("Tabelas do banco de dados criadas ou já existentes.")

if __name__ == '__main__':
    create_db_tables()
    app.run(debug=True)