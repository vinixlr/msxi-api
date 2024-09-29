import hashlib
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from sqlalchemy import inspect
from enums.enums import VeiculoStatus
from utils.responses.messages import MSG_DATA_ERROR_ROLLBACK
from db.data import db

class UserModel(db.Model):
    __tablename__ = 'user_tb'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def __init__(self, nome, password):
        self.nome = nome
        self.password = self._hash_password(password)

    @classmethod
    def find_by_name(cls, nome=nome):
        return cls.query.filter_by(nome=nome).first()
    
    @staticmethod
    def _hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    def save_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True, None
        except IntegrityError as e:
            db.session.rollback()
            return False, MSG_DATA_ERROR_ROLLBACK
        except Exception as e:
            db.session.rollback()
            return False, MSG_DATA_ERROR_ROLLBACK

class VeiculoModel(db.Model):
    __tablename__ = 'veiculo_tb'

    id = db.Column(db.Integer, primary_key=True)
    nm_veiculo_marca = db.Column(db.String(30), nullable=False)
    nm_veiculo_modelo = db.Column(db.String(30), nullable=False)
    nm_veiculo_cor = db.Column(db.String(30), nullable=False)
    nr_veiculo_ano_modelo = db.Column(db.Integer, nullable=False)
    nm_veiculo_chassi = db.Column(db.String(50), nullable=False, unique=True)
    nm_veiculo_status = db.Column(db.String(20), nullable=False)
    dt_inclusao = db.Column(db.DateTime, default=datetime.now(), nullable=False)

    def __init__(self,
                 nm_veiculo_marca,
                 nm_veiculo_modelo,
                 nm_veiculo_cor,
                 nr_veiculo_ano_modelo,
                 nm_veiculo_chassi,
                 nm_veiculo_status,
                 dt_inclusao=datetime.now()):
        self.nm_veiculo_marca = nm_veiculo_marca
        self.nm_veiculo_modelo = nm_veiculo_modelo
        self.nm_veiculo_cor = nm_veiculo_cor
        self.nr_veiculo_ano_modelo = nr_veiculo_ano_modelo
        self.nm_veiculo_chassi = nm_veiculo_chassi
        self.nm_veiculo_status = nm_veiculo_status
        self.dt_inclusao = dt_inclusao

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
    
    @classmethod
    def find_by_veiculo_modelo(cls, modelo):
        return cls.query.filter_by(nm_veiculo_modelo=modelo).first()

    @classmethod
    def find_all_veiculos(cls):
        return cls.query.all()

    @classmethod
    def find_by_chassi(cls, chassi):
        return cls.query.filter_by(nm_veiculo_chassi=chassi).first()

    @classmethod
    def update_status(cls, novo_status, chassi):
        obj = cls.query.filter_by(nm_veiculo_chassi=chassi).first()
        if not obj:
            return None

        obj.nm_veiculo_status = getattr(VeiculoStatus, novo_status).value
        db.session.commit()
        return obj

    @classmethod
    def delete(cls, chassi):
        obj = cls.query.filter_by(nm_veiculo_chassi=chassi).first()
        if not obj:
            return None

        db.session.delete(obj)
        db.session.commit()
        return obj

    def save_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True, None
        except IntegrityError as e:
            db.session.rollback()
            return False, MSG_DATA_ERROR_ROLLBACK
        except Exception as e:
            db.session.rollback()
            return False, MSG_DATA_ERROR_ROLLBACK

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}