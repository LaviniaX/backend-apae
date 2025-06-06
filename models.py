from app import db # Importa a instância do SQLAlchemy de app.py
from datetime import date, datetime
import enum # Para o Enum de tipo de usuário

# --- Enums ---
class TipoUsuario(enum.Enum):
    ADMINISTRADOR = "administrador"
    FUNCIONARIO = "funcionario"

# --- Modelos ---

class Usuario(db.Model):
    __tablename__ = 'usuario'

    id_usuario = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    sobrenome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(128), nullable=False) # Armazenar hashes de senha, não senhas em texto puro!
    tipo = db.Column(db.Enum(TipoUsuario), nullable=False, default=TipoUsuario.FUNCIONARIO)

    def __repr__(self):
        return f"<Usuario {self.nome} {self.sobrenome} ({self.tipo.value})>"

class Paciente(db.Model):
    __tablename__ = 'paciente'

    id_paciente = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    nome_social = db.Column(db.String(100))
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True) # Email pode ser opcional para paciente
    senha = db.Column(db.String(128)) # Senha pode ser opcional se o paciente não fizer login

    # Relacionamento Um para Um com Prontuario
    id_prontuario = db.Column(db.Integer, db.ForeignKey('prontuario.id_prontuario'), unique=True)
    prontuario = db.relationship('Prontuario', backref='paciente', uselist=False, cascade="all, delete-orphan")


    def __repr__(self):
        return f"<Paciente {self.nome} ({self.cpf})>"


class Prontuario(db.Model):
    __tablename__ = 'prontuario'

    id_prontuario = db.Column(db.Integer, primary_key=True)

    # Informações do Paciente
    # Note: nome, nome_social, cpf, email, senha já estão em Paciente.
    # Evitamos repetição aqui. Acessamos via prontuario.paciente.nome

    # Dados de Cadastro e Identificação
    numero_prontuario = db.Column(db.String(50), unique=True, nullable=False) # Este é o identificador único do prontuário
    situacao_cadastro = db.Column(db.String(50))
    area_atendimento = db.Column(db.String(100))
    data_entrada = db.Column(db.DateTime)
    data_saida = db.Column(db.DateTime)
    data_emissao_rg = db.Column(db.Date)
    numero_rg = db.Column(db.String(20))
    numero_certidao_nascimento = db.Column(db.String(50))
    livro_folha = db.Column(db.String(50))
    cartorio = db.Column(db.String(100))
    naturalidade = db.Column(db.String(100))
    sexo = db.Column(db.String(50))
    data_nascimento = db.Column(db.Date) # Replicado para facilitar acesso direto via prontuário, mas idealmente vem de Paciente
    ocupacao = db.Column(db.String(100))
    numero_carteira_pcd = db.Column(db.String(50))
    numero_cartao_nis = db.Column(db.String(50))
    numero_cartao_sus = db.Column(db.String(50))
    raca_cor = db.Column(db.String(50))

    # Endereço
    endereco_logradouro = db.Column(db.String(255))
    endereco_numero = db.Column(db.String(20))
    endereco_complemento = db.Column(db.String(100))
    endereco_bairro = db.Column(db.String(100))
    endereco_cidade = db.Column(db.String(100))
    endereco_uf = db.Column(db.String(2))

    # Contatos
    telefone_residencial = db.Column(db.String(20))
    telefone_recados = db.Column(db.String(20))
    pessoa_contato_recados = db.Column(db.String(100))

    # Dados de Mãe, Pai, Responsável
    nome_mae = db.Column(db.String(200))
    cpf_mae = db.Column(db.String(14))
    telefone_mae = db.Column(db.String(20))
    email_mae = db.Column(db.String(120))
    ocupacao_mae = db.Column(db.String(100))

    nome_pai = db.Column(db.String(200))
    cpf_pai = db.Column(db.String(14))
    telefone_pai = db.Column(db.String(20))
    email_pai = db.Column(db.String(120))
    ocupacao_pai = db.Column(db.String(100))

    nome_responsavel = db.Column(db.String(200))
    cpf_responsavel = db.Column(db.String(14))
    telefone_responsavel = db.Column(db.String(20))
    email_responsavel = db.Column(db.String(120))
    ocupacao_responsavel = db.Column(db.String(100))

    # Questionário de Saúde
    medicamento_utilizado = db.Column(db.Text)
    possui_alergia = db.Column(db.Boolean)
    alergias_descricao = db.Column(db.Text) # Descrição se possui_alergia for True
    possui_comorbidade = db.Column(db.Boolean)
    comorbidades_descricao = db.Column(db.Text) # Descrição se possui_comorbidade for True
    convenio_medico = db.Column(db.String(100))
    atividade_fisica_liberada = db.Column(db.Boolean)
    meio_transporte = db.Column(db.String(100))
    autorizacao_uso_imagem = db.Column(db.Boolean)
    observacoes = db.Column(db.Text)

    # Deficiência/Transtorno
    modalidade = db.Column(db.String(100))
    tipo_deficiencia = db.Column(db.String(100))
    transtorno = db.Column(db.String(100))
    cid_10 = db.Column(db.String(20))

    def __repr__(self):
        return f"<Prontuario ID: {self.id_prontuario} - Nº: {self.numero_prontuario}>"