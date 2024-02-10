from flask import Flask
from FlaskSeo import FlaskSeo

app = FlaskSeo(flask_cls=Flask, name=__name__)

@app.route("/AllUserAgents/", SeoCheck=True, UserAgents=["*"])
def AllUserAgents():
    return "Hello"


@app.route("/AppleBotUserAgents/", SeoCheck=False, UserAgents=["AppleBot"])
def UserAgents():
    return "Hello"


@app.route("/bingbotUserAgents", SeoCheck=True, UserAgents=["BingBot"])
def bingbotUserAgents():
    return "Hello"


@app.route("/GoogleBotUserAgents", SeoCheck=True, UserAgents=["GoogleBot"])
def GoogleBotUserAgents():
    return "Hello"




@app.route("/<string:name>/", SeoCheck=True, UserAgents=["GoogleBot", "*"], SeoForce=True)
def InvalidUrl():
    """
        because of using variable in url this url is not indexed in `robots.txt`
        if you want to force flask-seo to index this url use
        SeoForce=True in parameters

        like:
            @app.route("/<string:name>/", SeoCheck=True, SeoForce=True, UserAgents="GoogleBot")

    """
    return "Hello"


if __name__ == "__main__":
    app.run()
