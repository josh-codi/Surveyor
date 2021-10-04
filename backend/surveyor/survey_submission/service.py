import dataclasses
from dataclasses import dataclass
from datetime import datetime
from sqlite3.dbapi2 import Connection
from typing import Dict, List, Optional, Sequence, Union

from survey.service import SurveyField, SurveyService
from werkzeug.exceptions import HTTPException


@dataclass
class SurveySubmission(object):
    id: int
    survey_id: int
    created_at: datetime
    answers: List['SurveySubmissionAnswer']


@dataclass
class SurveySubmissionAnswer(object):
    id: int
    survey_submission_id: int
    survey_field_id: int
    answer: Union[int, str]


DEFAULT_PAGE_SIZE = 500


class SurveySubmissionService(object):
    @classmethod
    def get_survey_submissions(
        cls, db: Connection, admin_id: int, survey_id: int,
        page: Optional[int] = 1, after: Optional[datetime] = None,
        page_size: Optional[int] = DEFAULT_PAGE_SIZE,
    ) -> Sequence[SurveySubmission]:
        query_string = '''
            SELECT survey_submission.*, survey_submission_answer.*,
                survey_submission.id AS survey_submission_id,            
                survey_submission_answer.id AS survey_submission_answer_id

            FROM 
                survey
                JOIN survey_field
                    ON survey.id = survey_field.survey_id
                JOIN survey_submission
                    ON survey.id = survey_submission.survey_id
                JOIN survey_submission_answer
                    ON survey_submission.id = survey_submission_answer.survey_submission_id
            WHERE survey.admin_id=:admin_id AND survey_submission.survey_id=:survey_id
        '''
        if after is not None:
            query_string += ' AND survey_submission.created_at > :after'
        query_string += '''
             ORDER BY survey_submission.created_at DESC, survey_field.position ASC
        '''
        if page is not None:
            query_string += ' LIMIT :limit OFFSET :offset '

        db_result: List[dict] = db.execute(
            query_string,
            {
                'admin_id': admin_id, 'survey_id': survey_id,
                'limit': page_size,
                'offset': ((page or 1) - 1) * (page_size or DEFAULT_PAGE_SIZE),
                'after': after
            }
        ).fetchall()

        submissions: Dict[str, SurveySubmission] = {}
        for row in db_result:
            _id: int = row['survey_submission_id']
            if _id not in submissions:
                submissions[_id] =  \
                    SurveySubmissionService._parse_survey_submission_db_row_to_dataclass(
                        row)
            submissions[_id].answers.append(
                cls._parse_survey_submission_answer_db_row_to_dataclass(row)
            )
        return tuple(submissions.values())

    @classmethod
    def get_survey_submissions_summary(cls, db: Connection, survey_id: int):
        pass

    @classmethod
    def submit_answers_for_survey(cls, db: Connection, survey_id: int, data: Dict[str, str]):
        survey = SurveyService().get_survey_by_id(db, survey_id=survey_id)
        if survey is None:
            error = HTTPException('survey not found')
            error.code = 404
            raise error
        fields_by_id = {field.id: field for field in survey.fields}

        for survey_field_id, answer in data.items():
            field = fields_by_id[int(survey_field_id)]
            SurveySubmissionService._validate_answer_for_field(
                field, str(answer))

        submission_id: int = db.execute(
            ''' INSERT INTO survey_submission (survey_id) VALUES (?) ''',
            (survey_id,)
        ).lastrowid

        db.executemany(
            ''' INSERT INTO survey_submission_answer 
                (survey_submission_id, survey_field_id, answer)
                VALUES 
                (?, ?, ?)
            ''',
            [
                (submission_id, survey_field_id, str(answer).strip())
                for survey_field_id, answer in data.items()
            ]
        )

    @classmethod
    def _validate_answer_for_field(cls, field: SurveyField, answer: str):
        error = None
        if field.options.required and (answer is None or answer.strip() == ''):
            error = HTTPException(f'Field {field.label} is required')
        elif field.input_type == 'text':
            if len(answer) > field.options.max:
                error = HTTPException(
                    f'Answer is too long - expected {field.options.max} chracters')
        elif field.input_type == 'number':
            if int(answer) > field.options.max:
                error = HTTPException(
                    f'Answer is greater than expected max: {field.options.max}')
            elif int(answer) < field.options.min:
                error = HTTPException(
                    f'Answer is less than expected max: {field.options.min}')
        elif field.input_type == 'single-select':
            allowed_values = set(field.options.values)
            if answer not in allowed_values:
                error = HTTPException(
                    f'Answer should be one of: {field.options.values}')
        else:
            error = None

        if error is not None:
            error.description = error.description + f'. field_id: {field.id}'
            error.code = 400
            raise error

    @classmethod
    def _parse_survey_submission_db_row_to_dataclass(cls, row: dict) -> SurveySubmission:
        allowed_fields = set(f.name for f in dataclasses.fields(SurveyField))
        return SurveySubmission(**{
            **{k: row[k] for k in row.keys() if k in allowed_fields},
            'id': row['survey_submission_id'],
            'answers': [],
        })

    @classmethod
    def _parse_survey_submission_answer_db_row_to_dataclass(cls, row: dict) -> SurveySubmissionAnswer:
        allowed_fields = set(
            f.name for f in dataclasses.fields(SurveySubmissionAnswer))
        return SurveySubmissionAnswer(**{
            **{k: row[k] for k in row.keys() if k in allowed_fields},
            'id': row['survey_submission_answer_id']
        })
