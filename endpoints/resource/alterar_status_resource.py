from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from infra.helper import validate_jwt
from endpoints.service.veiculo_service import VeiculoService
from schema.alterar_status_schema import AlterarStatusRequestSchema
from utils.utilitarios import has_empty_or_null_value
from utils.responses.responses import resp_error, resp_ok
from utils.responses.messages import (
    MSG_ERRO_TOKEN,
    MSG_SUCCESS,
    MSG_INVALID_DATA,
    MSG_ERRO_STATUS_UPDATE,
)

RESOURCE_NAME = "Alterar Status"


class AlterarStatusResource(Resource):
    def put(self, chassi):
        """
        Resource responsavel por alterar veiculo status
        """
        req_data = request.get_json() or None
        if not req_data or has_empty_or_null_value(req_data):
            return resp_error(RESOURCE_NAME, None, MSG_INVALID_DATA)

        try:
            novo_status_request = AlterarStatusRequestSchema().load(req_data)
        except ValidationError as err:
            return resp_error(RESOURCE_NAME, err.messages, MSG_ERRO_STATUS_UPDATE)

        login_request, erros = validate_jwt(request.headers.get("idSessao"))
        if erros:
            return resp_error(RESOURCE_NAME, None, MSG_ERRO_TOKEN)

        retorno, erros = VeiculoService().alterar_status(chassi, novo_status_request.get("novo_status"), login_request)
        if erros:
            return resp_error(RESOURCE_NAME, None, erros)

        return resp_ok(RESOURCE_NAME, MSG_SUCCESS, data={"chassi": retorno.nm_veiculo_chassi, "status": retorno.nm_veiculo_status})
