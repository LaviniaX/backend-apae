from app import db
from models import Paciente, Prontuario
from sqlalchemy.exc import IntegrityError
from datetime import date, datetime

class PatientService:
    @staticmethod
    def get_all_patients():
        return Paciente.query.all()

    @staticmethod
    def get_patient_by_id(patient_id):
        return Paciente.query.get(patient_id)

    @staticmethod
    def get_patient_by_cpf(cpf):
        return Paciente.query.filter_by(cpf=cpf).first()

    @staticmethod
    def create_patient(nome, nome_social, cpf, email=None, senha=None, **prontuario_data):
        try:
            novo_paciente = Paciente(
                nome=nome,
                nome_social=nome_social,
                cpf=cpf,
                email=email,
                senha=senha # Lembre-se de hashar em produção!
            )
            db.session.add(novo_paciente)
            db.session.flush() # Para que novo_paciente.id_paciente seja gerado antes de criar o prontuário

            # Cria o prontuário associado
            novo_prontuario = Prontuario(
                # Popula os campos do prontuário com os dados passados em prontuario_data
                # Exemplo: numero_prontuario=prontuario_data.get('numero_prontuario')
                # E o resto dos campos do formulário
                **prontuario_data
            )
            novo_paciente.prontuario = novo_prontuario # Associa o prontuário ao paciente

            db.session.add(novo_prontuario)
            db.session.commit()
            return novo_paciente
        except IntegrityError:
            db.session.rollback()
            return None # CPF ou prontuário já existe, ou outro erro de integridade
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao criar paciente: {e}")
            return None

    @staticmethod
    def update_patient(patient_id, nome=None, nome_social=None, cpf=None, email=None, senha=None):
        paciente = Paciente.query.get(patient_id)
        if not paciente:
            return None

        try:
            if nome:
                paciente.nome = nome
            if nome_social:
                paciente.nome_social = nome_social
            if cpf:
                paciente.cpf = cpf
            if email:
                paciente.email = email
            if senha:
                paciente.senha = senha # Lembre-se de hashar em produção!

            db.session.commit()
            return paciente
        except IntegrityError:
            db.session.rollback()
            return None # CPF ou email já existe, ou outro erro de integridade
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao atualizar paciente: {e}")
            return None

    @staticmethod
    def delete_patient(patient_id):
        paciente = Paciente.query.get(patient_id)
        if paciente:
            try:
                db.session.delete(paciente) # Isso também vai deletar o prontuário devido ao cascade
                db.session.commit()
                return True
            except Exception as e:
                db.session.rollback()
                print(f"Erro ao deletar paciente: {e}")
                return False
        return False