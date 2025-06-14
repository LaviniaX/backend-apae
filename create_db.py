# create_db.py

from app import app, db 

with app.app_context():
    print("Criando o banco de dados...")
    
    db.create_all()

    print("Banco de dados 'meu_banco_dados.db' e tabelas criadas com sucesso!")