# -*- coding: utf-8 -*-

"""
    Flask-Seo
     Copyright (c) 2023-2023 Alisharify, GPL-3 license
     Author: alisharify <lisharifyofficial@gmail.com>
 """
# build in
import re
import json

import redis
# lib
from redis import Redis
from flask import Flask as OriginalFlaskObject, make_response, current_app
from flask.sansio.app import setupmethod

# flask-seo
from FlaskSeo import excep



class BaseConfig:
    SEO_ENABLE = True
    SEO_LOG = True

    CONFIG_ROBOTS_KEY_NAME = "FLASK_SEO_ROBOTS_TXT_STORAGE" # app.config key name
    REDIS_ROBOTS_KEY_NAME =  "FLASK_SEO:" # redis KEY NAME

    __SEO_BACKEND_CONNECTION_TYPE = ('default', 'redis')
    SEO_CONNECTION_TYPE = 'default' # default value

    SEO_REDIS_URL = "redis://localhost:6379"

def FlaskSeo(flask_cls: OriginalFlaskObject, name: str, *args, **kwargs):
    """ Factory Function for creating Flask-Seo Object
    Wrapper For SeoFlasky Class
    """

    if not flask_cls or not isinstance(flask_cls, OriginalFlaskObject):
        excep.NotFlaskInstance(f"{flask_cls} is not a Flask instance!")
    if not name:
        excep.FlaskAppNameRequired("Please provide a name for flask application, __name__ can be used as flask app.")

    class SeoFlasky(BaseConfig, flask_cls):
        """ 
        class FlaskSeo: Base Class 
        """

        def __init__(self, *args, **kwargs):
            content = super().__init__(*args, **kwargs)

            @self.route(rule="/robots.txt/", SeoCheck=False)
            def FLASK_SEO_ROBOTS_TXT_VIEW():
                self.logger.info("Serving Robots.txt.")

                message = f"# Auto generated robots.txt\n\n\n"

                if self.SEO_CONNECTION_TYPE == "default":
                    for each in self.get_robots_txt_from_default_storage():
                        message += "\n"
                        for user_agent in each['user-agent']:
                            message += f"User-agent: {user_agent}\n"
                        message += f"{'Allow: ' if each['status'] else 'Disallow: '}{each['url']}\n"
                        message += "\n"


                elif self.SEO_CONNECTION_TYPE == "redis":
                    message += "\n"

                    for each in self.get_robots_txt_from_redis_storage():
                        for user_agent in each['user-agent']:
                            message += f"User-agent: {user_agent}:\n"
                        message += f"{'Allow: ' if each['status'] else 'Disallow: '}{each['url']}\n"
                        message += "\n"

                response = make_response(message)
                response.headers["Content-Type"] = "text/plain"
                return response


            return content


        def update_seo_config(self, config:dict) -> None:
            self.SEO_ENABLE = config.get("SEO_ENABLE", self.SEO_ENABLE)
            self.SEO_LOG = config.get("SEO_LOG", self.SEO_LOG)
            self.SEO_CONNECTION_TYPE = config.get("CONNECTION_TYPE", self.SEO_CONNECTION_TYPE)
            self.SEO_REDIS_URL = config.get("REDIS_URL", self.SEO_REDIS_URL)

            if not self.SEO_CONNECTION_TYPE in self.__SEO_BACKEND_CONNECTION_TYPE:
                raise excep.InvalidConnectionType(f"Invalid SEO_CONNECTION_TYPE {self.SEO_CONNECTION_TYPE}\n available connection types are: {self.__SEO_BACKEND_CONNECTION_TYPE}")

            self.logger.info(f"SEO_CONNECTION_TYPE {self.SEO_CONNECTION_TYPE}")
            if self.SEO_CONNECTION_TYPE == "redis":
                # check connection
                try:
                    self.SEO_REDIS_INTERFACE = redis.Redis.from_url(self.SEO_REDIS_URL)
                    if not self.SEO_REDIS_INTERFACE.ping():
                        raise ValueError("invalid redis url")

                except (ValueError, redis.exceptions.ConnectionError):
                    raise ValueError(f"invalid redis url: {self.SEO_REDIS_URL}.")
                else:
                    self.logger.info(f"REDIS CONNECTION IS OK. {self.SEO_REDIS_URL}")

            self.logger.info(f"SEO_LOG IS {self.SEO_LOG}")
            self.logger.info(f"SEO_ENABLE IS {self.SEO_ENABLE}")




        @setupmethod
        def route(self, rule: str,
                  SeoCheck: bool = True, #robots.txt
                  SeoForce: bool = False, #robots.txt
                  UserAgents: list = ["*"],#robots.txt
                  SitemapCheck: bool = True, #sitemap
                  SitemapForce: bool = False, #sitemap
                  Sitemappriority: int = 1, #sitemap
                  *args, **kwargs):
            """Overwriting flask route method view for keep tracking of each url in application """
            content = super().route(rule=rule, *args, **kwargs) # call super route method

            if rule == "/robots.txt/":
                return content

            if re.search("<\w+\:\w+>", rule) and not SeoForce:
                if self.SEO_LOG:
                    self.logger.warning(
                        f"Url `{rule}` by security reassons is not added to robots.txt file. Use `SeoForce=True` to Force it to adding in robots.txt")
                return content

            if not isinstance(UserAgents, list):
                raise ValueError(f"UserAgents {UserAgents} must be a list not {type(UserAgents)}")

            data = {
                "user-agent": UserAgents,
                "url": rule,
                "status": SeoCheck
            }

            self.__add_url_to_seo_storage(url_dict=data)
            return content


        def __add_url_to_seo_storage(self, url_dict:dict) -> bool:
            """This Method get a dictionary that contain all the url info for seo and sitemap information
            then base on seo_connection type that user provided in app.config added data to storage"""
            match self.SEO_CONNECTION_TYPE:
                case "default":
                    self.add_url_to_seo_storage_default(url_dict=url_dict)
                    return True
                case "redis":
                    self.add_url_to_seo_storage_redis(url_dict=url_dict)
                    return True

                case _:
                    if self.SEO_LOG:
                        self.logger.warning("invalid seo_connection_type")
                    return False

        def add_url_to_seo_storage_default(self, url_dict:dict) -> bool:
            if self.CONFIG_ROBOTS_KEY_NAME not in self.config:
                self.config[self.CONFIG_ROBOTS_KEY_NAME] = []

            self.config[self.CONFIG_ROBOTS_KEY_NAME].append(url_dict)
            if self.SEO_LOG:
                self.logger.info(f"url {url_dict.get('url')} added to default<app.config> backend storage.")


        def add_url_to_seo_storage_redis(self, url_dict:dict) -> bool:
            s = self.SEO_REDIS_INTERFACE.set(name=self.REDIS_ROBOTS_KEY_NAME+url_dict.get("url"), value=json.dumps(url_dict))
            if self.SEO_LOG:
                if s:
                    self.logger.info(f"url {url_dict.get('url')} added to redis backend storage.")
                else:
                    self.logger.error(f"url {url_dict.get('url')} was not added to redis backend storage.")
                    return s


        def get_robots_txt_from_redis_storage(self):
            keys = self.SEO_REDIS_INTERFACE.get(name=self.REDIS_ROBOTS_KEY_NAME+"*")
            for each in keys:
                each = json.loads(str(each.decode("utf-8"))) # normalize
                yield each

        def get_robots_txt_from_default_storage(self):
            for each in self.config.get(self.CONFIG_ROBOTS_KEY_NAME):
                yield each
    return SeoFlasky(import_name=name, *args, **kwargs)
