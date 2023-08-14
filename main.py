from app import make_app

server = make_app()
server.run(debug=True)