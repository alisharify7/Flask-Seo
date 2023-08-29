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

if you wanna an url indexed in Robots.txt File use SeoCheck=True in route function to saying to flask_seo add this url to robots.txt file
some urls by security reasons cannot added to robots.txt file if you wanna force Flask_seo to index these type of urls use SeoForce=True this means
add this url to robots.txt no matter if its not secure




  
