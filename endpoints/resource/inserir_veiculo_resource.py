from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from schema.inserir_veiculo_schema import InserirVeiculoRequestSchema
from infra.helper import validate_jwt
from utils.utilitarios import has_empty_or_null_value
from endpoints.service.veiculo_service import VeiculoService
from utils.responses.responses import resp_error, resp_ok
from utils.responses.messages import (
    MSG_ERRO_TOKEN,
    MSG_SUCCESS,
    MSG_INVALID_DATA,
    MSG_ERRO_VEICULO_INSERT
)

RESOURCE_NAME = "Inserir Veiculo"

class InserirVeiculoResource(Resource):
    def post(self):
        """
        Resource responsavel por inserir um veiculo
        """
        req_data = request.get_json() or None
        if not req_data or has_empty_or_null_value(req_data):
            return resp_error(RESOURCE_NAME, None, MSG_INVALID_DATA)
        
        try:
            inserir_veiculo_request = InserirVeiculoRequestSchema().load(req_data)
        except ValidationError as err:
            return resp_error(RESOURCE_NAME, err.messages, MSG_ERRO_VEICULO_INSERT)
        
        login_request, erros = validate_jwt(request.headers.get("idSessao"))
        if erros:
            return resp_error(RESOURCE_NAME, None, MSG_ERRO_TOKEN)
        
        retorno, erros = VeiculoService().inserir_veiculo_request(inserir_veiculo_request, login_request)

        if not retorno:
            return resp_error(RESOURCE_NAME, None, erros)
        return resp_ok(RESOURCE_NAME, MSG_SUCCESS, data={})
