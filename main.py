from app import create_app
from config.develop import Config

server = create_app(Config)
server.run()