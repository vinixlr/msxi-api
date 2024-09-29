from flask import request
from flask_restful import Resource
from infra.helper import validate_jwt
from endpoints.service.veiculo_service import VeiculoService
from utils.responses.responses import resp_error, resp_ok
from utils.responses.messages import MSG_ERRO_TOKEN, MSG_SUCCESS


RESOURCE_NAME = "Consulta Veiculos"

class ConsultaVeiculoResource(Resource):
    def get(self):
        """
        Resource responsavel por buscar veiculos
        """
        login_request, erros = validate_jwt(request.headers.get("idSessao"))
        if erros:
            return resp_error(RESOURCE_NAME, None, MSG_ERRO_TOKEN)
        
        retorno, erros = VeiculoService().consulta_veiculos(login_request)
        if erros:
            return resp_error(RESOURCE_NAME, None, erros)

        return resp_ok(RESOURCE_NAME, MSG_SUCCESS, data={"veiculos": retorno})