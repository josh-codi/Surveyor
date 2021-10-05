from datetime import datetime

from auth import get_current_user
from auth.decorators import login_required
from database import autocommit_db_changes, get_db
from flask import request
from flask.json import jsonify
from flask_classy import FlaskView, route
from werkzeug.exceptions import HTTPException

from .service import DEFAULT_PAGE_SIZE, SurveySubmissionService


class SurveySubmissionView(FlaskView):
    decorators = [autocommit_db_changes]

    def __init__(self) -> None:
        super().__init__()
        self.service = SurveySubmissionService()

    @login_required
    @route('/<string:survey_id>/submissions', methods=['GET'])
    def get(self, survey_id: int):
        admin = get_current_user()

        page = request.args.get('page', None)
        page = int(page) if page is not None else page

        page_size = request.args.get('page-size', DEFAULT_PAGE_SIZE)
        page_size = int(page_size)

        after = request.args.get('after', None)
        after = datetime.fromisoformat(after) if after is not None else after

        submissions = self.service.get_survey_submissions(
            get_db(),
            admin_id=admin.id, survey_id=survey_id,
            page=page, page_size=page_size, after=after
        )
        return jsonify(submissions), 200

    @login_required
    @route('/<string:survey_id>/submissions/summary', methods=['GET'])
    def get_submissions_summary(self, survey_id: int):
        # TODO: Implement endpoint - for populating dashboard sort of with graphs, and charts data
        error = HTTPException('Not implemented yet')
        error.code = 500
        raise error

    @route('/<string:survey_id>/submissions', methods=['POST'])
    def post(self, survey_id: int):
        self.service.submit_answers_for_survey(
            get_db(), survey_id, data=request.json)
        return jsonify({'message': 'OK'}), 201
