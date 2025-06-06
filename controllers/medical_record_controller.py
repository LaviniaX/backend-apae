from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from services.medical_record_service import MedicalRecordService
from services.patient_service import PatientService # Para obter dados do paciente associado
from datetime import date, datetime

medical_record_bp = Blueprint('medical_record_bp', __name__)

@medical_record_bp.route('/medical_records', methods=['GET'])
def list_medical_records():
    records = MedicalRecordService.get_all_medical_records()
    return render_template('medical_records/list.html', records=records)

@medical_record_bp.route('/medical_records/<int:record_id>', methods=['GET'])
def get_medical_record(record_id):
    record = MedicalRecordService.get_medical_record_by_id(record_id)
    if record:
        return render_template('medical_records/detail.html', record=record)
    return "Prontuário não encontrado", 404

@medical_record_bp.route('/medical_records/<int:record_id>/edit', methods=['GET', 'POST'])
def edit_medical_record(record_id):
    record = MedicalRecordService.get_medical_record_by_id(record_id)
    if not record:
        return "Prontuário não encontrado", 404

    if request.method == 'POST':
        data = request.form
        # Converte booleanos de checkboxes e datas para os tipos corretos
        data_processed = {
            key: value for key, value in data.items() if value # Remove campos vazios
        }
        for key in ['possui_alergia', 'possui_comorbidade', 'atividade_fisica_liberada', 'autorizacao_uso_imagem']:
            data_processed[key] = data.get(key) == 'on'

        # Lidar com conversão de datas para os tipos de modelo
        date_fields = [
            'data_entrada', 'data_saida', 'data_emissao_rg', 'data_nascimento'
        ]
        for field in date_fields:
            if field in data_processed and data_processed[field]:
                try:
                    # Tenta converter para datetime se for campo DateTime (como data_entrada/saida)
                    if hasattr(record, field) and isinstance(getattr(type(record), field).type, db.DateTime):
                        data_processed[field] = datetime.strptime(data_processed[field], '%Y-%m-%dT%H:%M') # Assume formato "2024-05-30T10:30"
                    # Tenta converter para date se for campo Date
                    elif hasattr(record, field) and isinstance(getattr(type(record), field).type, db.Date):
                        data_processed[field] = datetime.strptime(data_processed[field], '%Y-%m-%d').date() # Assume formato "2024-05-30"
                except ValueError:
                    print(f"Aviso: Formato de data inválido para {field}: {data_processed[field]}")
                    data_processed[field] = None # Ou manter original, ou levantar erro

        updated_record = MedicalRecordService.update_medical_record(record_id, **data_processed)
        if updated_record:
            return redirect(url_for('medical_record_bp.list_medical_records'))
        else:
            return render_template('medical_records/edit.html', record=record, error="Erro ao atualizar prontuário.")
    return render_template('medical_records/edit.html', record=record)

@medical_record_bp.route('/medical_records/<int:record_id>/delete', methods=['POST'])
def delete_medical_record(record_id):
    # Deletar prontuário sem deletar o paciente associado
    # Isso requer que o relacionamento no modelo Paciente não tenha 'cascade="all, delete-orphan"'
    # no prontuário. Se tiver, deletar o prontuário por aqui não funciona como o esperado.
    # Assumindo que você quer apenas deletar o prontuário.
    # O cascade está configurado para "all, delete-orphan" no Patient, então deletar paciente deleta prontuário.
    # Para deletar SÓ o prontuário, a relação precisa ser alterada ou você precisa desassociar antes.
    # No seu models.py atual, se você deletar o prontuário isoladamente, ele deixará o paciente órfão de prontuário.

    if MedicalRecordService.delete_medical_record(record_id):
        return redirect(url_for('medical_record_bp.list_medical_records'))
    return "Erro ao deletar prontuário", 500