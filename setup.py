from setuptools import setup, find_packages

__NAME__ = "FlaskSeo"
__version__ = "1.0.0"
__author__ = "ali sharify"
__author_mail__ = "alisharifyofficial@gmail.com"
__copyright__ = "ali sharify - 2023"
__license__ = "MIT"
__short_description__ = "Flask Seo is an extension for Flask that helps you optimize your web pages for search engines (SEO)"


with open("./README.rst", "r") as f:
    long_description = f.read()

setup(
    name=__NAME__,
    version=__version__,
    description=__short_description__,
    packages=find_packages(),
    author_email=__author_mail__,
    author=__author__,
    url="https://github.com/alisharify7/flask_captcha2",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    # long_description_content_type="text/markdown",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        "Environment :: Web Environment",
        "Framework :: Flask",
    ],
    license="MIT",
    install_requires=[
        "flask>=2.2.5",
        "redis>= 5.0.1",
    ],
    python_requires=">=3.8",
    keywords='flask-seo, flask-search-engine-optimize, flaskseo, flask-google-seo'

)