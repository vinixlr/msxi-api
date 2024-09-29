from flask import Flask
from flask_restful import Api

from db.data import db
from config.logger import configurar_logger
from endpoints.resource.login_resource import LoginResource
from endpoints.resource.consulta_veiculos_resource import ConsultaVeiculoResource
from endpoints.resource.consulta_veiculo_chassi_resource import ConsultaChassiResource
from endpoints.resource.inserir_veiculo_resource import InserirVeiculoResource
from endpoints.resource.alterar_status_resource import AlterarStatusResource
from endpoints.resource.deletar_veiculo_resource import DeletarVeiculoResource


app = Flask(__name__)
api = Api(app)
api.prefix = '/api'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True


api.add_resource(LoginResource, '/login', methods=['POST'], endpoint='/login')
api.add_resource(ConsultaVeiculoResource, '/veiculos', methods=['GET'], endpoint='/consulta_veiculo_get')
api.add_resource(ConsultaChassiResource, '/veiculos/<chassi>', methods=['GET'], endpoint='/consulta_chassi_get')
api.add_resource(InserirVeiculoResource, '/inserir-veiculo', methods=['POST'], endpoint='/inserir_veiculo_post')
api.add_resource(AlterarStatusResource, '/veiculos/<chassi>', methods=['PUT'], endpoint='/alterar_status_put')
api.add_resource(DeletarVeiculoResource, '/veiculos/<chassi>', methods=['DELETE'], endpoint='/deletar_veiculo_delete')




def app_start():
    db.init_app(app)
    configurar_logger()

    with app.app_context():
        db.create_all()
    return app

app = app_start()



if __name__ == '__main__':
    app.run(debug=False)