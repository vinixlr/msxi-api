from marshmallow import (
    Schema,
    validate,
    pre_load,
)
from marshmallow.fields import Str
from enums.enums import VeiculoStatus
from utils.responses.messages import MSG_FIELD_REQUIRED

VEICULO_STATUS = [status.value for status in VeiculoStatus]


class AlterarStatusRequestSchema(Schema):
    novo_status = Str(required=True, error_messages={'required': MSG_FIELD_REQUIRED},
                      validate=validate.OneOf(VEICULO_STATUS))

    @pre_load
    def equaliza_carro_status(self, data, **kwargs):
        if "novo_status" in data:
            data["novo_status"] = data.get("novo_status").upper()
        return data
