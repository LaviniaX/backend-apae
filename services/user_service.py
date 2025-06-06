from app import db
from models import Usuario, TipoUsuario
from sqlalchemy.exc import IntegrityError

class UserService:
    @staticmethod
    def get_all_users():
        return Usuario.query.all()

    @staticmethod
    def get_user_by_id(user_id):
        return Usuario.query.get(user_id)

    @staticmethod
    def get_user_by_email(email):
        return Usuario.query.filter_by(email=email).first()

    @staticmethod
    def create_user(nome, sobrenome, email, senha, tipo=TipoUsuario.FUNCIONARIO):
        try:
            # Em um app real, aqui você hash a senha (ex: bcrypt.hashpw)
            novo_usuario = Usuario(
                nome=nome,
                sobrenome=sobrenome,
                email=email,
                senha=senha, # Lembre-se de hashar em produção!
                tipo=tipo
            )
            db.session.add(novo_usuario)
            db.session.commit()
            return novo_usuario
        except IntegrityError:
            db.session.rollback()
            return None # Email já existe
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao criar usuário: {e}")
            return None

    @staticmethod
    def update_user(user_id, nome=None, sobrenome=None, email=None, senha=None, tipo=None):
        usuario = Usuario.query.get(user_id)
        if not usuario:
            return None

        try:
            if nome:
                usuario.nome = nome
            if sobrenome:
                usuario.sobrenome = sobrenome
            if email:
                usuario.email = email
            if senha:
                usuario.senha = senha # Lembre-se de hashar em produção!
            if tipo and isinstance(tipo, TipoUsuario):
                usuario.tipo = tipo

            db.session.commit()
            return usuario
        except IntegrityError:
            db.session.rollback()
            return None # Email já existe, ou outro erro de integridade
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao atualizar usuário: {e}")
            return None

    @staticmethod
    def delete_user(user_id):
        usuario = Usuario.query.get(user_id)
        if usuario:
            try:
                db.session.delete(usuario)
                db.session.commit()
                return True
            except Exception as e:
                db.session.rollback()
                print(f"Erro ao deletar usuário: {e}")
                return False
        return False