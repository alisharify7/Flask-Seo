# Flask-Seo
Flask Seo is an extension for Flask that helps you optimize your web pages for search engines (SEO). It does this by adding various features to your web pages, such as:
- Title tags
- Meta descriptions
- Keywords
- Sitemap

By adding these features, Flask Seo can help your web pages rank higher in search engine results pages (SERPs), which can lead to increased traffic and engagement.




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



  
