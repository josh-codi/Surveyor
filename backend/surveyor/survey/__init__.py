from flask.app import Flask

from .views import SurveyView


def init_app(app: Flask):
    SurveyView.register(app, route_base='/survey')
