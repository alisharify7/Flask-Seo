# Flask-Seo
a simple Flask Extension for Improving Seo(Search engine optimization)



installation:

      pip install flask_seo -U




## 0.0 How to Use:


```python
# from flask import Flask (Dont Use This instead Use Flask_Seo.Seo.Flask class)

from Flask_Seo.Seo import Flask

app = Flask(__name__)

app.set_seo_connection('redis', Redis) 
       or
app.set_seo_connection('default', True) 



@app.route("/", SeoCheck=True, ForceSeo=True)
def index():
     return "Index page"

```

### flask_seo.Seo.Flask class is actually flask.Flask Class But some Methods are overloaded for keep tracking of each url 

## This two attributes are added in route method 
  
        SeoCheck:bool=True, ForceSeo:bool=True

if you wanna an url indexed in Robots.txt File use `SeoCheck=True` in route function to saying to flask_seo add this url to robots.txt file
some urls by security reasons cannot added to robots.txt file if you wanna force Flask_seo to index these type of urls use `SeoForce=True` this means
add this url to robots.txt no matter if its not secure


### app.set_seo_connection('connector_type',  connector)
the set_seo_connection() has to connector redis, default 

in `default` mode all urls are stored in app.config variabe

in `redis` mode all urls are stored in redis database

```
# Redis Connection
from redis import Redis
from Flask_Seo.Seo import Flask

app = Flask(__name__)
r = Redis()
app.set_seo_connection('redis', r)
```


```
# default Connection
from Flask_Seo.Seo import Flask

app = Flask(__name__)
app.set_seo_connection('default', True)
```



## /robots.txt view  automatically generate all urls text file and return robots.txt file for search engines




  
