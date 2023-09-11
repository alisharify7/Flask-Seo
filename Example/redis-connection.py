import redis
from flask import Flask
from FlaskSeo import FlaskSeo



app = FlaskSeo(Flask, __name__)
app.set_seo_connection("redis", redis.Redis())



@app.route("/AllUserAgent/", SeoCheck=True, UserAgent="*")
def AllUserAgent():
    return "Hello"


@app.route("/AppleBotUserAgent/", SeoCheck=True, UserAgent="AppleBot")
def UserAgent():
    return "Hello"


@app.route("/bingbotUserAgent/", SeoCheck=True, UserAgent="BingBot")
def bingbotUserAgent():
    return "Hello"


@app.route("/GoogleBotUserAgent/", SeoCheck=True, UserAgent="GoogleBot")
def GoogleBotUserAgent():
    return "Hello"




@app.route("/<string:name>/", SeoCheck=True, UserAgent="GoogleBot")
def InvalidUrl():
    """
        because of using variable in url this url is not indexed in `robots.txt`
        if you want to force flask-seo to index this url use
        SeoForce=True in parameters

        like:
            @app.route("/<string:name>/", SeoCheck=True, SeoForce=True, UserAgent="GoogleBot")

    """
    return "Hello"



