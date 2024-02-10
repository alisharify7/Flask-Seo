# -*- coding: utf-8 -*-

"""
    Flask-Seo
     Copyright (c) 2023-2023 Alisharify,
     Author: alisharify <lisharifyofficial@gmail.com>
 """

import re
import json
import datetime
import logging
from redis import Redis
from flask import Flask as OriginalFlask, make_response
from functools import wraps
from flask.scaffold import setupmethod
from .logger import get_logger


WarningLogger = get_logger(logging.WARNING)
InfoLogger = get_logger(logging.INFO)


class Values:
    SEO_ALLOW = "SEO-ALLOWED"
    SEO_DISALLOW = "SEO-DISALLOWED"
    STATUS = "STATUS"


def FlaskSeo(app: OriginalFlask, name: str):
    """ Wrapper For SeoFlasky Class """
    class SeoFlasky(app):
        """ 
        class FlaskSeo: Base Class 
        """
        @setupmethod
        def route(self, rule: str, SeoCheck: bool = True, SeoForce: bool = False, UserAgent: str = "*", SitemapCheck: bool = True, SitemapForce: bool = False, Sitemappriority: int = 1, *args, **kwargs):
            """ OverLoad Flask.scaffold.route Function """
            content = super().route(rule=rule, *args, **kwargs)

            if self.config.get('ROBOTS_TXT', False):

                if re.search("<\w+\:\w+>", rule) and not SeoForce:
                    WarningLogger.warning(
                        f"Url `{rule}` by security reassons is not added to robots.txt file. Use `SeoForce=True` to Force it to adding in robots.txt")
                    return content

                data = {
                    "agent": UserAgent,
                    "url": rule,
                    "status": SeoCheck
                }
                match self.connection_type:
                    case "default":
                        if SeoCheck:
                            if not self.config.get(Values.SEO_ALLOW, False):
                                self.config[Values.SEO_ALLOW] = set()
                                self.config[Values.SEO_ALLOW].add(
                                    json.dumps(data))
                            else:
                                self.config[Values.SEO_ALLOW].add(
                                    json.dumps(data))
                        else:
                            if not self.config.get(Values.SEO_DISALLOW, False):
                                self.config[Values.SEO_DISALLOW] = set()
                                self.config[Values.SEO_DISALLOW].add(
                                    json.dumps(data))
                            else:
                                self.config[Values.SEO_DISALLOW].add(
                                    json.dumps(data))
                    case "redis":
                        self.connection.set(
                            name=f"FLASK_SEO:{rule}", value=json.dumps(data))

            return content

        __SEO_CONNECTION_TYPE = ('default', 'redis')

        def set_seo_connection(self, connection_type: str, connection=None):
            """ Set Seo Connection for Seo Storage"""
            if connection_type not in self.__SEO_CONNECTION_TYPE:
                raise ValueError(
                    f"Invalid connection type. valid connections are {self.__SEO_CONNECTION_TYPE}")

            if connection_type == 'default':
                if not connection is True:
                    raise ValueError("connection Be True.")

                self.connection_type = connection_type
                self.config['ROBOTS_TXT'] = True
                WarningLogger.warning(
                    "Note: Seo Type is `default`, this connection is not for production enviroment.Use this for development only. Use Redis.redis connection for production")
            else:
                if not isinstance(connection, Redis):
                    raise ValueError(
                        "connection must be an instance of redis.Redis class.")

                # test connection
                connection.set(name="test", value="123654")

                result = connection.get(name="test")
                if not result:
                    raise ValueError("Connection is not valid...")
                if str(result.decode('utf-8')) != "123654":
                    raise ValueError("Connection is not valid...")
                connection.delete("test")

                self.connection_type = connection_type
                self.connection = connection
                self.config['ROBOTS_TXT'] = True

        def __init__(self, *args, **kwargs):
            content = super().__init__(*args, **kwargs)

            @self.route(rule="/robots.txt", SeoCheck=False)
            def robots_txt_view():
                InfoLogger.info("Serving Robots.txt.")

                message = f"# Auto Generated robots.txt\n# Version:2.0.0\t\n\n\n"

                if not self.config.get("ROBOTS_TXT"):
                    response = make_response(message)
                    response.headers["Content-Type"] = "text/plain"
                    return response

                records = {}
                if self.connection_type == "default":

                    for each in self.config.get(Values.SEO_ALLOW, {}):
                        each = json.loads(each)

                        if each['url'] == '/robots.txt':
                            continue
                        record = (
                            f"Allow: " if each['status'] else 'Disallow') + f"{each['url']}\n"
                        if not records.get(each['agent'], False):
                            records[each['agent']] = [record]
                        else:
                            records[each['agent']].append(record)

                    for each in self.config.get(Values.SEO_DISALLOW, {}):
                        each = json.loads(each)

                        if each['url'] == '/robots.txt':
                            continue
                        record = (
                            f"Allow: " if each['status'] else f"Disallow: ") + f"{each['url']}\n"
                        if not records.get(each['agent'], False):
                            records[each['agent']] = [record]
                        else:
                            records[each['agent']].append(record)
                else:
                    # check robots.txt is in redis serve it from redis
                    if result := self.connection.get('robots.txt'):
                        result = str(result.decode('utf-8'))
                        response = make_response(result)
                        response.headers["Content-Type"] = "text/plain"
                        return response

                    for each in self.connection.keys("FLASK_SEO:*"):
                        each = str(each.decode('utf-8'))
                        each = self.connection.get(each)
                        each = json.loads(str(each.decode("utf-8")))
                        record = f"{'Disallow: ' if not each['status'] else 'Allow: '} {each['url']}\n"
                        if not records.get(each['agent'], False):
                            records[each['agent']] = [record]
                        else:
                            records[each['agent']].append(record)

                for each in records:
                    message += f"User-agent: {each}\n"
                    message += "".join(records[each]) + "\n"

                self.connection.set(
                    name="robots.txt", value=message, ex=((60*60)*24)*7)  # one week

                response = make_response(message)
                response.headers["Content-Type"] = "text/plain"
                return response

            return content

    return SeoFlasky(name)
