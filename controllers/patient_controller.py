from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from services.patient_service import PatientService
from services.medical_record_service import MedicalRecordService # Pode ser útil para criar um prontuário ao criar paciente
from datetime import datetime, date
patient_bp = Blueprint('patient_bp', __name__)

@patient_bp.route('/patients', methods=['GET'])
def list_patients():
    patients = PatientService.get_all_patients()
    return render_template('patients/list.html', patients=patients)

@patient_bp.route('/patients/create', methods=['GET', 'POST'])
def create_patient():
    if request.method == 'POST':
        data = request.form
        # Dados do paciente
        nome = data['nome']
        nome_social = data.get('nome_social')
        cpf = data['cpf']
        email = data.get('email')
        senha = data.get('senha') # Lembre-se de hashar em produção!

        # Dados do prontuário (passados como **kwargs para o service)
        prontuario_data = {
            'numero_prontuario': data['numero_prontuario'],
            'situacao_cadastro': data.get('situacao_cadastro'),
            'area_atendimento': data.get('area_atendimento'),
            'data_entrada': datetime.strptime(data['data_entrada'], '%Y-%m-%d') if 'data_entrada' in data and data['data_entrada'] else None,
            'data_saida': datetime.strptime(data['data_saida'], '%Y-%m-%d') if 'data_saida' in data and data['data_saida'] else None,
            'data_emissao_rg': datetime.strptime(data['data_emissao_rg'], '%Y-%m-%d').date() if 'data_emissao_rg' in data and data['data_emissao_rg'] else None,
            'numero_rg': data.get('numero_rg'),
            'numero_certidao_nascimento': data.get('numero_certidao_nascimento'),
            'livro_folha': data.get('livro_folha'),
            'cartorio': data.get('cartorio'),
            'naturalidade': data.get('naturalidade'),
            'sexo': data.get('sexo'),
            'data_nascimento': datetime.strptime(data['data_nascimento'], '%Y-%m-%d').date() if 'data_nascimento' in data and data['data_nascimento'] else None,
            'ocupacao': data.get('ocupacao'),
            'numero_carteira_pcd': data.get('numero_carteira_pcd'),
            'numero_cartao_nis': data.get('numero_cartao_nis'),
            'numero_cartao_sus': data.get('numero_cartao_sus'),
            'raca_cor': data.get('raca_cor'),
            'endereco_logradouro': data.get('endereco_logradouro'),
            'endereco_numero': data.get('endereco_numero'),
            'endereco_complemento': data.get('endereco_complemento'),
            'endereco_bairro': data.get('endereco_bairro'),
            'endereco_cidade': data.get('endereco_cidade'),
            'endereco_uf': data.get('endereco_uf'),
            'telefone_residencial': data.get('telefone_residencial'),
            'telefone_recados': data.get('telefone_recados'),
            'pessoa_contato_recados': data.get('pessoa_contato_recados'),
            'nome_mae': data.get('nome_mae'),
            'cpf_mae': data.get('cpf_mae'),
            'telefone_mae': data.get('telefone_mae'),
            'email_mae': data.get('email_mae'),
            'ocupacao_mae': data.get('ocupacao_mae'),
            'nome_pai': data.get('nome_pai'),
            'cpf_pai': data.get('cpf_pai'),
            'telefone_pai': data.get('telefone_pai'),
            'email_pai': data.get('email_pai'),
            'ocupacao_pai': data.get('ocupacao_pai'),
            'nome_responsavel': data.get('nome_responsavel'),
            'cpf_responsavel': data.get('cpf_responsavel'),
            'telefone_responsavel': data.get('telefone_responsavel'),
            'email_responsavel': data.get('email_responsavel'),
            'ocupacao_responsavel': data.get('ocupacao_responsavel'),
            'medicamento_utilizado': data.get('medicamento_utilizado'),
            'possui_alergia': data.get('possui_alergia') == 'on', # Checkbox
            'alergias_descricao': data.get('alergias_descricao'),
            'possui_comorbidade': data.get('possui_comorbidade') == 'on', # Checkbox
            'comorbidades_descricao': data.get('comorbidades_descricao'),
            'convenio_medico': data.get('convenio_medico'),
            'atividade_fisica_liberada': data.get('atividade_fisica_liberada') == 'on', # Checkbox
            'meio_transporte': data.get('meio_transporte'),
            'autorizacao_uso_imagem': data.get('autorizacao_uso_imagem') == 'on', # Checkbox
            'observacoes': data.get('observacoes'),
            'modalidade': data.get('modalidade'),
            'tipo_deficiencia': data.get('tipo_deficiencia'),
            'transtorno': data.get('transtorno'),
            'cid_10': data.get('cid_10'),
        }

        patient = PatientService.create_patient(nome, nome_social, cpf, email, senha, **prontuario_data)
        if patient:
            return redirect(url_for('patient_bp.list_patients'))
        else:
            return render_template('patients/create.html', error="Erro ao criar paciente. CPF pode já existir.")
    return render_template('patients/create.html')

@patient_bp.route('/patients/<int:patient_id>', methods=['GET'])
def get_patient(patient_id):
    patient = PatientService.get_patient_by_id(patient_id)
    if patient:
        return render_template('patients/detail.html', patient=patient)
    return "Paciente não encontrado", 404

@patient_bp.route('/patients/<int:patient_id>/edit', methods=['GET', 'POST'])
def edit_patient(patient_id):
    patient = PatientService.get_patient_by_id(patient_id)
    if not patient:
        return "Paciente não encontrado", 404

    if request.method == 'POST':
        data = request.form
        # Dados do paciente
        nome = data.get('nome')
        nome_social = data.get('nome_social')
        cpf = data.get('cpf')
        email = data.get('email')
        senha = data.get('senha')

        updated_patient = PatientService.update_patient(patient_id, nome, nome_social, cpf, email, senha)

        # Atualiza dados do prontuário se existirem e forem enviados
        if patient.prontuario:
            prontuario_data = {
                'numero_prontuario': data.get('numero_prontuario'),
                'situacao_cadastro': data.get('situacao_cadastro'),
                'area_atendimento': data.get('area_atendimento'),
                'data_entrada': datetime.strptime(data['data_entrada'], '%Y-%m-%d') if 'data_entrada' in data and data['data_entrada'] else None,
                'data_saida': datetime.strptime(data['data_saida'], '%Y-%m-%d') if 'data_saida' in data and data['data_saida'] else None,
                'data_emissao_rg': datetime.strptime(data['data_emissao_rg'], '%Y-%m-%d').date() if 'data_emissao_rg' in data and data['data_emissao_rg'] else None,
                'numero_rg': data.get('numero_rg'),
                'numero_certidao_nascimento': data.get('numero_certidao_nascimento'),
                'livro_folha': data.get('livro_folha'),
                'cartorio': data.get('cartorio'),
                'naturalidade': data.get('naturalidade'),
                'sexo': data.get('sexo'),
                'data_nascimento': datetime.strptime(data['data_nascimento'], '%Y-%m-%d').date() if 'data_nascimento' in data and data['data_nascimento'] else None,
                'ocupacao': data.get('ocupacao'),
                'numero_carteira_pcd': data.get('numero_carteira_pcd'),
                'numero_cartao_nis': data.get('numero_cartao_nis'),
                'numero_cartao_sus': data.get('numero_cartao_sus'),
                'raca_cor': data.get('raca_cor'),
                'endereco_logradouro': data.get('endereco_logradouro'),
                'endereco_numero': data.get('endereco_numero'),
                'endereco_complemento': data.get('endereco_complemento'),
                'endereco_bairro': data.get('endereco_bairro'),
                'endereco_cidade': data.get('endereco_cidade'),
                'endereco_uf': data.get('endereco_uf'),
                'telefone_residencial': data.get('telefone_residencial'),
                'telefone_recados': data.get('telefone_recados'),
                'pessoa_contato_recados': data.get('pessoa_contato_recados'),
                'nome_mae': data.get('nome_mae'),
                'cpf_mae': data.get('cpf_mae'),
                'telefone_mae': data.get('telefone_mae'),
                'email_mae': data.get('email_mae'),
                'ocupacao_mae': data.get('ocupacao_mae'),
                'nome_pai': data.get('nome_pai'),
                'cpf_pai': data.get('cpf_pai'),
                'telefone_pai': data.get('telefone_pai'),
                'email_pai': data.get('email_pai'),
                'ocupacao_pai': data.get('ocupacao_pai'),
                'nome_responsavel': data.get('nome_responsavel'),
                'cpf_responsavel': data.get('cpf_responsavel'),
                'telefone_responsavel': data.get('telefone_responsavel'),
                'email_responsavel': data.get('email_responsavel'),
                'ocupacao_responsavel': data.get('ocupacao_responsavel'),
                'medicamento_utilizado': data.get('medicamento_utilizado'),
                'possui_alergia': data.get('possui_alergia') == 'on',
                'alergias_descricao': data.get('alergias_descricao'),
                'possui_comorbidade': data.get('possui_comorbidade') == 'on',
                'comorbidades_descricao': data.get('comorbidades_descricao'),
                'convenio_medico': data.get('convenio_medico'),
                'atividade_fisica_liberada': data.get('atividade_fisica_liberada') == 'on',
                'meio_transporte': data.get('meio_transport_type'),
                'autorizacao_uso_imagem': data.get('autorizacao_uso_imagem') == 'on',
                'observacoes': data.get('observacoes'),
                'modalidade': data.get('modalidade'),
                'tipo_deficiencia': data.get('tipo_deficiencia'),
                'transtorno': data.get('transtorno'),
                'cid_10': data.get('cid_10'),
            }
            MedicalRecordService.update_medical_record(patient.prontuario.id_prontuario, **prontuario_data)

        if updated_patient:
            return redirect(url_for('patient_bp.list_patients'))
        else:
            return render_template('patients/edit.html', patient=patient, error="Erro ao atualizar paciente.")
    return render_template('patients/edit.html', patient=patient)

@patient_bp.route('/patients/<int:patient_id>/delete', methods=['POST'])
def delete_patient(patient_id):
    if PatientService.delete_patient(patient_id):
        return redirect(url_for('patient_bp.list_patients'))
    return "Erro ao deletar paciente", 500