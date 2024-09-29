import requests

from models.model import VeiculoModel
from config.logger import log
from utils.responses.messages import MSG_NO_DATA_FOUND


class VeiculoService:
    def inserir_veiculo_request(self, novo_veiculo_request, login_request):
        log(f"user {login_request.get("user_name")} : iniciando requisição de inserir veiculo")
        try:
            retorno, erros = (VeiculoModel(
                novo_veiculo_request.get("nm_veiculo_marca"),
                novo_veiculo_request.get("nm_veiculo_modelo"),
                novo_veiculo_request.get("nm_veiculo_cor"),
                novo_veiculo_request.get("nr_veiculo_ano_modelo"),
                novo_veiculo_request.get("nm_veiculo_chassi"),
                novo_veiculo_request.get("nm_veiculo_status"))
                              .save_to_db())
            log(f"user {login_request.get("user_name")} : inserção de veiculo realizada com sucesso")
            return retorno, erros

        except requests.exceptions.RequestException as e:
            log(f"user {login_request.get("user_name")} : erro ao inserir veiculo")
            return None, str(e)

    def consulta_veiculos(self, login_request):
        log(f"user {login_request.get("user_name")} : iniciando requisição de busca de veiculos")
        try:
            retorno = VeiculoModel.find_all_veiculos()
            if not retorno:
                log(f"user {login_request.get("user_name")} : erro ao consultar de veiculos")
                return None, MSG_NO_DATA_FOUND

            log("consulta de veiculos realizada com sucesso")

            veiculo_map = [{"veiculo_nome": veiculo.nm_veiculo_modelo, "veiculo_chassi": veiculo.nm_veiculo_chassi} for
                           veiculo in retorno]
            return veiculo_map, None

        except requests.exceptions.RequestException as e:
            log(f"user {login_request.get("user_name")} : erro ao consultar veiculos")
            return None, str(e)

    def consulta_chassi(self, chassi, login_request):
        log(f"user {login_request.get("user_name")} : iniciando requisição de consulta de chassi")
        try:
            retorno = VeiculoModel.find_by_chassi(chassi)
            if not retorno:
                log(f"user {login_request.get("user_name")} : erro ao consultar chassi")
                return None, MSG_NO_DATA_FOUND

            log("consulta de chassi realizada com sucesso")

            return retorno, None

        except requests.exceptions.RequestException as e:
            log(f"user {login_request.get("user_name")} : erro ao consultar veiculos")
            return None, str(e)

    def alterar_status(self, chassi, novo_status_request, login_request):
        log(f"user {login_request.get("user_name")} : iniciando alteração de status")
        try:
            obj = VeiculoModel.update_status(novo_status_request, chassi)
            if not obj:
                log(f"user {login_request.get("user_name")} : erro ao consultar chassi")
                return None, MSG_NO_DATA_FOUND

            log("consulta de chassi realizada com sucesso")

            return obj, None

        except requests.exceptions.RequestException as e:
            log(f"user {login_request.get("user_name")} : erro ao consultar veiculos")
            return None, str(e)

    def deletar_veiculo(self, chassi, login_request):
        log(f"user {login_request.get("user_name")} : iniciando delete de registro")
        try:
            obj = VeiculoModel.delete(chassi)
            if not obj:
                log(f"user {login_request.get("user_name")} : erro deletar registro")
                return None, MSG_NO_DATA_FOUND

            log("veiculo deletado com sucesso")

            return obj, None

        except requests.exceptions.RequestException as e:
            log(f"user {login_request.get("user_name")} : erro ao deletar veiculo")
            return None, str(e)