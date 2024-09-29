from marshmallow import Schema, validate, pre_load
from marshmallow.fields import Str, Integer
from enums.enums import VeiculoStatus
from utils.responses.messages import MSG_FIELD_REQUIRED

VEICULO_STATUS = [status.value for status in VeiculoStatus]

class InserirVeiculoRequestSchema(Schema):
    nm_veiculo_marca = Str(required=True, error_messages={'required': MSG_FIELD_REQUIRED})
    nm_veiculo_modelo = Str(required=True, error_messages={'required': MSG_FIELD_REQUIRED})
    nm_veiculo_cor = Str(required=True, error_messages={'required': MSG_FIELD_REQUIRED})
    nr_veiculo_ano_modelo = Integer(required=True, error_messages={'required': MSG_FIELD_REQUIRED})
    nm_veiculo_chassi = Str(required=True, error_messages={'required': MSG_FIELD_REQUIRED})
    nm_veiculo_status = Str(required=True, error_messages={'required': MSG_FIELD_REQUIRED}, validate=validate.OneOf(VEICULO_STATUS))

    @pre_load
    def equaliza_carro_status(self, data, **kwargs):
        if "nm_veiculo_status" in data:
            data["nm_veiculo_status"] = data.get("nm_veiculo_status").upper()
        return data
