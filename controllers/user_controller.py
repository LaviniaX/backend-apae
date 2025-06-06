from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from services.user_service import UserService
from models import TipoUsuario # Importa o Enum

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/users', methods=['GET'])
def list_users():
    users = UserService.get_all_users()
    return render_template('users/list.html', users=users)

@user_bp.route('/users/create', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        data = request.form
        nome = data['nome']
        sobrenome = data['sobrenome']
        email = data['email']
        senha = data['senha']
        tipo_str = data.get('tipo', 'FUNCIONARIO') # Default para FUNCIONARIO
        tipo = TipoUsuario[tipo_str.upper()] # Converte string para Enum

        user = UserService.create_user(nome, sobrenome, email, senha, tipo)
        if user:
            return redirect(url_for('user_bp.list_users'))
        else:
            return render_template('users/create.html', error="Erro ao criar usuário. Email pode já existir.", TipoUsuario=TipoUsuario)
    return render_template('users/create.html', TipoUsuario=TipoUsuario)

@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = UserService.get_user_by_id(user_id)
    if user:
        return render_template('users/detail.html', user=user)
    return "Usuário não encontrado", 404

@user_bp.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_user(user_id):
    user = UserService.get_user_by_id(user_id)
    if not user:
        return "Usuário não encontrado", 404

    if request.method == 'POST':
        data = request.form
        nome = data.get('nome')
        sobrenome = data.get('sobrenome')
        email = data.get('email')
        senha = data.get('senha')
        tipo_str = data.get('tipo')
        tipo = TipoUsuario[tipo_str.upper()] if tipo_str else None

        updated_user = UserService.update_user(user_id, nome, sobrenome, email, senha, tipo)
        if updated_user:
            return redirect(url_for('user_bp.list_users'))
        else:
            return render_template('users/edit.html', user=user, error="Erro ao atualizar usuário.", TipoUsuario=TipoUsuario)
    return render_template('users/edit.html', user=user, TipoUsuario=TipoUsuario)

@user_bp.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    if UserService.delete_user(user_id):
        return redirect(url_for('user_bp.list_users'))
    return "Erro ao deletar usuário", 500