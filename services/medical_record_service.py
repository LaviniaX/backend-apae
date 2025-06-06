from app import db
from models import Prontuario, Paciente
from datetime import date, datetime

class MedicalRecordService:
    @staticmethod
    def get_all_medical_records():
        return Prontuario.query.all()

    @staticmethod
    def get_medical_record_by_id(record_id):
        return Prontuario.query.get(record_id)

    @staticmethod
    def get_medical_record_by_patient_id(patient_id):
        return Prontuario.query.filter_by(id_prontuario=patient_id).first() # id_prontuario é PK e FK

    @staticmethod
    def get_medical_record_by_number(prontuario_number):
        return Prontuario.query.filter_by(numero_prontuario=prontuario_number).first()

    @staticmethod
    def create_medical_record_for_patient(patient_id, **data):
        paciente = Paciente.query.get(patient_id)
        if not paciente:
            return None # Paciente não encontrado

        if paciente.prontuario:
            return None # Paciente já possui um prontuário

        try:
            novo_prontuario = Prontuario(
                **data # Todos os dados do formulário
            )
            paciente.prontuario = novo_prontuario # Associa o prontuário ao paciente
            db.session.add(novo_prontuario)
            db.session.commit()
            return novo_prontuario
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao criar prontuário: {e}")
            return None

    @staticmethod
    def update_medical_record(record_id, **data):
        prontuario = Prontuario.query.get(record_id)
        if not prontuario:
            return None

        try:
            for key, value in data.items():
                if hasattr(prontuario, key):
                    # Lidar com tipos de data, se necessário
                    if 'data' in key and isinstance(value, str):
                        try:
                            # Tenta converter para datetime para campos DateTime
                            if isinstance(getattr(Prontuario, key).type, db.DateTime):
                                setattr(prontuario, key, datetime.strptime(value, '%Y-%m-%dT%H:%M')) # Ex: "2024-05-30T10:30"
                            # Tenta converter para date para campos Date
                            elif isinstance(getattr(Prontuario, key).type, db.Date):
                                setattr(prontuario, key, datetime.strptime(value, '%Y-%m-%d').date()) # Ex: "2024-05-30"
                            else:
                                setattr(prontuario, key, value)
                        except ValueError:
                            print(f"Aviso: Formato de data inválido para {key}: {value}")
                            # Pode levantar um erro ou ignorar, dependendo da necessidade
                            pass
                    else:
                        setattr(prontuario, key, value)
            db.session.commit()
            return prontuario
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao atualizar prontuário: {e}")
            return None

    @staticmethod
    def delete_medical_record(record_id):
        prontuario = Prontuario.query.get(record_id)
        if prontuario:
            try:
                # Se Paciente tem cascade "all, delete-orphan" para prontuario,
                # deletar o paciente já deletaria o prontuário.
                # Se você quiser deletar apenas o prontuário sem deletar o paciente,
                # precisa remover a associação primeiro.
                # Exemplo:
                # if prontuario.paciente:
                #     prontuario.paciente.prontuario = None
                db.session.delete(prontuario)
                db.session.commit()
                return True
            except Exception as e:
                db.session.rollback()
                print(f"Erro ao deletar prontuário: {e}")
                return False
        return False