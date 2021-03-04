from sanic import Sanic, response

app = Sanic(__name__)


app.static("/assets", "src/web/assets/")
app.static("/favicon.ico", "src/web/favicon.ico")


@app.route("/")
async def main(req):
    return response.html(open("src/web/index.html").read())
