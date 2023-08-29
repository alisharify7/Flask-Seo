import re
import json
import datetime
from redis import Redis
from flask import Flask as OriginalFlask, jsonify, make_response
from functools import wraps
from flask.scaffold import setupmethod
from .logger import get_logger



Logger = get_logger()

class Flask(OriginalFlask):
    """ 
    Flsak Class
    this class inherite all funcs and attributes from actual Flask class but overite-Overload Some Functions 
    """
    @setupmethod
    def route(self, rule:str, SeoCheck:bool=True, SeoForce:bool=False, *args, **kwargs):
        """ OverLoad Flask.scaffold.route Function """
        content =  super().route(rule=rule, *args, **kwargs)
        
        
        if self.config.get('ROBOTS_TXT', False):
            if re.search("<\w+\:\w+>", rule) and not SeoForce:
                Logger.warning(f"Url `{rule}` by security reassons is not added to robots.txt file. Use `SeoForce=True` to Force it to adding in robots.txt")
                return content

            if self.connection_type == "default":
                    if SeoCheck:
                        if not self.config.get("SEO_ALLOWED", False):
                            self.config["SEO_ALLOWED"] = set()
                            self.config["SEO_ALLOWED"].add(rule)
                        else:
                            self.config["SEO_ALLOWED"].add(rule)
                    else:
                        if not self.config.get("SEO_DISALLOWED", False):
                            self.config["SEO_DISALLOWED"] = set()
                            self.config["SEO_DISALLOWED"].add(rule)
                        else:
                            self.config["SEO_DISALLOWED"].add(rule)
            else:
                if SeoCheck:
                    self.connection.set(name=rule, value=json.dumps({"status":True}))
                else:
                    self.connection.set(name=rule, value=json.dumps({"status":False}))

        return content


    __SEO_CONNECTION_TYPE = ('default', 'redis')
    def set_seo_connection(self, connection_type:str, connection=None):
        if connection_type not in self.__SEO_CONNECTION_TYPE:
            raise ValueError(f"Invalid connection type. valid connections are {self.__SEO_CONNECTION_TYPE}")
        
        if connection_type == 'default':
            self.connection_type = connection_type
            self.config['ROBOTS_TXT'] = True
            print("ok")
        else:
            if not isinstance(connection, Redis):
                raise ValueError("connection must be an instance of redis.Redis class.")
            
            # test connection
            connection.set(name="test", value="123654")

            result = connection.get(name="test")
            if not result:
                raise ValueError("Connection is not valid...")
            if  str(result.decode('utf-8')) != "123654":
                raise ValueError("Connection is not valid...")

            connection.delete("test")
            
            self.connection_type = connection_type
            self.connection = connection
            self.config['ROBOTS_TXT'] = True
        
            


    def __init__(self, *args, **kwargs):
        content = super().__init__(*args, **kwargs)

        @self.route(rule="/robots.txt", SeoCheck=False)
        def robots_txt_view():
            Logger.warning("Robots.txt file Served.")

            message = "# Auto Generated robots.txt file\n\n\n\nUser-agent: *\n"
            if self.connection_type == "default":

                for each in self.config.get("SEO_ALLOWED", {}):
                    if each == '/robots.txt':
                        continue
                    message += f"Allow: {each}\n"
                
                message += "\nUser-agent: *\n"
                for each in self.config.get("SEO_DISALLOWED", {}):
                    if each == '/robots.txt':
                        continue
                    message += f"Disallow: {each}\n"
            else:
                for each in self.connection.keys():
                    each = str(each.decode('utf-8'))
                    res = self.connection.get(each)
                    res = json.loads(str(res.decode("utf-8")))
                    print(res)
                    message += f"{'Disallow' if res['status'] else 'Allow'}: {each}\n"

                

            response = make_response(message)
            response.headers["Content-Type"] = "text/plain"
            return response

        return content





