from flask import Flask

from api.views import bp


def create_app():
    # create and configure the app
    app = Flask(__name__)
    app.register_blueprint(bp)
    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8002)
