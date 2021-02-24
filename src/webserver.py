from sanic import Sanic, response

app = Sanic(__name__)


@app.route("/")
async def main(req):
    return response.text("Hello, World!")
