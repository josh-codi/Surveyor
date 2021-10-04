from flask import Flask
from .views import SurveySubmissionView


def init_app(app: Flask):
    SurveySubmissionView.register(app, route_base='/surveys')
