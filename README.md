# Flask-Seo
a simple Flask Extension for Improving Seo(Search engine optimization)



installation:

      ----
      Not Implemented Yet



## 0.0 How to Use:


```python
from flask import Flask
from Flask_Seo import FlaskSeo

app = FlaskSeo(Flask, __name__)


app.set_seo_connection('redis', redis.Redis) 
or
app.set_seo_connection('default', True) 



@app.route("/", SeoCheck=True, ForceSeo=True, UserAgent="*")
def index():
     return "Index page"
```

  
    SeoCheck:bool=True, ForceSeo:bool=True UserAgent:str="*"

if you wanna an url indexed in Robots.txt File use `SeoCheck=True` in route function to saying to flask_seo add this url to robots.txt file
some urls by security reasons cannot added to robots.txt file if you wanna force Flask_seo to index these type of urls use `SeoForce=True` this means
add this url to robots.txt no matter if its not secure
use UserAgent="some agent name" for specifying user-agent that you want to index the urls


### app.set_seo_connection('connector_type',  connector)
the set_seo_connection() has to connector redis, default 

in `default` mode all urls are stored in app.config varable

in `redis` mode all urls are stored in redis database

```python
# Redis Connection
from redis import Redis
from flask import Flask
from Flask_Seo import FlaskSeo

app = FlaskSeo(Flask, __name__)
r = Redis()
app.set_seo_connection('redis', r)
```


``` python
# default Connection
from flask import Flask
from Flask_Seo.Seo import Flask

app = FlaskSeo(Flask ,__name__)
app.set_seo_connection('default', True)
```



### /robots.txt view automatically generate all urls text file and return robots.txt file for search engines


# Note: this extension only overload some functions in flask.Flask Class to add some functionality for keep watching on every url endpoint in app



  
