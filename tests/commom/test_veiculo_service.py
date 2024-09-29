from endpoints.service.veiculo_service import VeiculoService
from models.model import VeiculoModel



def test_inserir_veiculo_request_sucesso(mocker):

    mock_obj = VeiculoModel(
        "fiat",
        "siena",
        "prata",
        2016,
        "1245JF34289710",
        "CONNECTADO"
    )

    mocker.patch("endpoints.service.veiculo_service.VeiculoModel.save_to_db", return_value=(mock_obj, None))
    result, erro = VeiculoService().inserir_veiculo_request({}, {})
    assert isinstance(result, VeiculoModel)
    assert erro is None

def test_inserir_veiculo_request_erro(mocker):
    mocker.patch("endpoints.service.veiculo_service.VeiculoModel.save_to_db", return_value=(None, Exception))
    result, erro = VeiculoService().inserir_veiculo_request({}, {})
    assert result is None
    assert erro is not None

def test_consulta_veiculos_request_sucesso(mocker):
    mock_obj = VeiculoModel(
        "fiat",
        "siena",
        "prata",
        2016,
        "1245JF34289710",
        "CONNECTADO"
    )

    mocker.patch("endpoints.service.veiculo_service.VeiculoModel.find_all_veiculos", return_value=[mock_obj])
    result, erro = VeiculoService().consulta_veiculos({})
    assert result is not None
    assert erro is None

def test_consulta_chassi_request_sucesso(mocker):
    mock_obj = VeiculoModel(
        "fiat",
        "siena",
        "prata",
        2016,
        "1245JF34289710",
        "CONNECTADO"
    )

    mocker.patch("endpoints.service.veiculo_service.VeiculoModel.find_by_chassi", return_value=mock_obj)
    result, erro = VeiculoService().consulta_chassi({}, {})
    assert result is not None
    assert erro is None

def test_alterar_status_request_sucesso(mocker):
    mock_obj = VeiculoModel(
        "fiat",
        "siena",
        "prata",
        2016,
        "1245JF34289710",
        "CONNECTADO"
    )

    mocker.patch("endpoints.service.veiculo_service.VeiculoModel.update_status", return_value=mock_obj)
    result, erro = VeiculoService().alterar_status({}, {}, {})
    assert result is not None
    assert erro is None

def test_deletar_veiculo_request_sucesso(mocker):
    mock_obj = VeiculoModel(
        "fiat",
        "siena",
        "prata",
        2016,
        "1245JF34289710",
        "CONNECTADO"
    )

    mocker.patch("endpoints.service.veiculo_service.VeiculoModel.delete", return_value=mock_obj)
    result, erro = VeiculoService().deletar_veiculo({}, {})
    assert result is not None
    assert erro is None