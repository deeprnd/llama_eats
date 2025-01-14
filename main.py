from wsgiref.simple_server import make_server
import falcon
from services.agent.chains import Chains
from services.agent.embeddings import AgentEmbeddings
from services.llm_service import OrderingAgent
from services.eats.mock_eats_api import MockEatsAPI
from services.eats.eats_api import EatsAPI
from resources.order_resource import OrderResource
from stores.userstore import UserStore

def create_app(eats_api: EatsAPI, chains: Chains, embeddings: AgentEmbeddings, user_store: UserStore):
    ordering_agent = OrderingAgent(eats_api, chains, embeddings, user_store)
    app = falcon.App(middleware=falcon.CORSMiddleware(
    allow_origins='http://localhost:3000', allow_credentials='*'))
    
    order_resource = OrderResource(ordering_agent, eats_api)
    app.add_route('/query', order_resource, suffix='query')
    app.add_route('/order', order_resource, suffix='order')
    return app

if __name__ == '__main__':
    embeddings = AgentEmbeddings()
    user_store = UserStore(embeddings)
    chains = Chains(user_store)
    app = create_app(MockEatsAPI(), chains, embeddings, user_store)
    with make_server('', 8000, app) as httpd:
        print('Serving on port 8000...')
        httpd.serve_forever()