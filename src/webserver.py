from sanic import Sanic, response
from src.api import api

app = Sanic(__name__)

app.blueprint(api)
app.static("/assets", "src/web/assets/")
app.static("/favicon.ico", "src/web/favicon.ico")


@app.route("/")
@app.route("/<path:path>")
async def main(req, path=None):
    return response.html(open("src/web/index.html").read())
