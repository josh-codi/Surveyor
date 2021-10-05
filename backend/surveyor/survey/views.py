from typing import Optional
from flask.json import jsonify
from flask_classy import FlaskView, route
from auth.decorators import login_required
from database import get_db, autocommit_db_changes
from .service import SurveyService
from flask import request, abort
from auth import get_current_user


class SurveyView(FlaskView):
    decorators = [login_required, autocommit_db_changes]

    def __init__(self) -> None:
        super().__init__()
        self.service = SurveyService()

    @route('/', methods=['POST'])
    def post(self):
        admin = get_current_user()
        created_survey = self.service.create_survey(
            get_db(), admin_id=admin.id, data=request.json)
        return jsonify(created_survey), 201

    @route('/', methods=['GET'])
    def list(self):
        admin = get_current_user()
        return jsonify(
            self.service.get_surveys(get_db(), admin.id)
        ), 200

    @route('/<string:survey_id>', methods=['GET'])
    def get_one(self,  survey_id: int):
        admin = get_current_user()
        survey = self.service.get_survey_by_id(
            get_db(), admin_id=admin.id, survey_id=survey_id)
        if not survey:
            abort(404)
        return jsonify(survey), 200

    @route('/<string:survey_id>', methods=['PUT'])
    def put(self, survey_id: int):
        admin = get_current_user()
        updated_survey = self.service.update_survey(
            get_db(), admin.id, survey_id, data=request.json)
        return jsonify(updated_survey), 202
