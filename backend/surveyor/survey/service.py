
from collections import defaultdict
from typing import Dict, List, Optional, Sequence, Tuple, Union
from sqlite3.dbapi2 import Connection
from sqlite3 import IntegrityError
from datetime import datetime
import json

from werkzeug.exceptions import HTTPException

from auth.service import User
from dataclasses import dataclass
import dataclasses


@dataclass
class Survey(object):
    id: int
    name: str
    admin_id: int
    created_at: datetime
    updated_at: datetime
    # admin: Optional[User] = None  # will be None, if not loaded from db yet
    fields: Optional[List["SurveyField"]] = None


@dataclass
class SurveyField(object):
    id: int
    survey_id: int
    label: str
    input_type: str
    options: "SurveyFieldOptions"
    position: int
    created_at: datetime
    updated_at: datetime


@dataclass
class SurveyFieldOptions(object):
    min: Union[int, str, None] = None
    max: Union[int, str, None] = None
    values: Union[List[str], None] = None


SURVEY_FIELD_TYPE_TEXT = 'text'
SURVEY_FIELD_TYPE_NUMBER = 'number'
SURVEY_FIELD_TYPE_SINGLE_SELECT = 'single-select'
VALID_INPUT_TYPES = (SURVEY_FIELD_TYPE_NUMBER,
                     SURVEY_FIELD_TYPE_TEXT, SURVEY_FIELD_TYPE_SINGLE_SELECT,)


def _validate_metadata_of_input_type(data: dict):
    """
    For the current `input_type`, check that the metadata JSON string contains
    all the info required for that `input_type`
    """
    if data['input_type'] not in VALID_INPUT_TYPES:
        raise Exception(
            f"Invalid input_type '{data['input_type']}'. Must be one of {VALID_INPUT_TYPES}")

    metadata, error = (data['options'], None)
    if not isinstance(metadata, dict):
        raise HTTPException('Metadata is not a JSON object')

    if data['input_type'] == SURVEY_FIELD_TYPE_NUMBER:
        if not isinstance(metadata.get('max'), int):
            error = HTTPException(
                f"For {data['input_type']}, metadata.max must be an integer")
        if not isinstance(metadata.get('min'), int):
            error = HTTPException(
                f"For {data['input_type']}, metadata.min must be an integer")
    elif data['input_type'] == SURVEY_FIELD_TYPE_TEXT:
        if not isinstance(metadata.get('max'), int):
            error = HTTPException(
                f"For {data['input_type']}, metadata.max_length must be an integer")
    elif data['input_type'] == SURVEY_FIELD_TYPE_NUMBER:
        if not isinstance(metadata.get('values'), list):
            error = HTTPException(
                f"For {data['input_type']}, metadata.options must be an array")

        first_non_string_option = next(
            (f for f in metadata.get('options', []) if not isinstance(f, str)),
            None
        )
        if first_non_string_option is not None:
            error = HTTPException(
                f"For {data['input_type']}, metadata.options must be an array of strings")
    else:
        error = None

    if error is not None:
        error.code = 400
        raise error

    return metadata


class SurveyService(object):
    @staticmethod
    def create_survey(db: Connection, admin_id: str, data: dict):
        try:
            survey_id: int = db.execute(
                'INSERT INTO survey (name, admin_id) VALUES (?, ?)',
                (data['name'], admin_id)
            ).lastrowid
        except IntegrityError as error:
            http_error = HTTPException(str(error))
            http_error.code = 400
            raise http_error
        SurveyService._insert_survey_fields_into_db(
            db, survey_id, data['fields'])

        survey = SurveyService.get_survey_by_id(db, admin_id, survey_id)
        return survey

    @staticmethod
    def _insert_survey_fields_into_db(db: Connection, survey_id: int, fields: List[dict]):
        db.executemany(
            '''
                INSERT INTO survey_field (survey_id, label, input_type, options, position)
                VALUES (:survey_id, :label, :input_type, :options, :position)
            ''',
            [
                {
                    **field,
                    'position': i + 1,
                    'survey_id': survey_id,
                    # validate 'options', to ensure data integrity
                    'options': json.dumps(_validate_metadata_of_input_type(field))
                }
                for i, field in enumerate(fields)
            ]
        )

    @staticmethod
    def get_survey_by_id(db: Connection, admin_id: int, survey_id: int):
        data = SurveyService.get_surveys(db, admin_id, survey_id)
        try:
            return data[0]
        except IndexError:
            return None

    @staticmethod
    def get_surveys(db: Connection, admin_id: int, survey_id: Optional[int] = None):
        query_string = '''
            SELECT  *,
            
            survey.created_at AS survey_created_at,
            survey.updated_at AS survey_updated_at,
            
            survey_field.id AS survey_field_id,
            survey_field.created_at AS survey_field_created_at,
            survey_field.updated_at AS survey_field_updated_at

            FROM survey JOIN survey_field ON survey.id=survey_field.survey_id
            WHERE survey.admin_id=:admin_id
        '''
        if survey_id:
            query_string += ' AND survey.id=:survey_id'
        query_string += ' ORDER BY survey.updated_at DESC, survey_field.position ASC'

        db_result: List[dict] = db.execute(
            query_string,  {'admin_id': admin_id, 'survey_id': survey_id}
        ).fetchall()

        surveys: Dict[str, Survey] = {}
        for row in db_result:
            _id = row['survey_id']

            if _id not in surveys:
                surveys[_id] = \
                    SurveyService._parse_survey_db_result_to_dataclass(row)
                surveys[_id].fields = []

            surveys[_id].fields.append(
                SurveyService._parse_survey_field_db_result_to_dataclass(row)
            )

        return tuple(surveys.values())

    @staticmethod
    def update_survey(db: Connection, admin_id: int, survey_id: int, data: dict):
        '''
        TODO: Implement adding/removing/repositioning of survey fields
        '''
        if SurveyService.get_survey_by_id(db, admin_id, survey_id) is None:
            return None

        db.execute(
            'UPDATE survey SET name=:name WHERE id=:id',
            {'id': survey_id, 'name': data['name']}
        )
        db.executemany(
            ''' 
                UPDATE survey_field
                SET label=:label, input_type=:input_type, options=:options
                -- position=:position -- update of position is not implemented
                WHERE id=:id 
            ''',
            [
                {
                    **field,
                    # validate 'options', to ensure data integrity
                    'options': json.dumps(_validate_metadata_of_input_type(field))
                }
                for field in data['fields']
            ]
        )

        survey = SurveyService.get_survey_by_id(db, admin_id, survey_id)
        return survey

    # @staticmethod
    # def _validate_survey_field_positions(survey: Survey):
    #     mispositioned_field: Optional[SurveyField] = next(
    #         (field for i, field in enumerate(survey.fields) if field.position != i + 1), None)
    #     if mispositioned_field is not None:
    #         error = HTTPException(
    #             f"Error in field 'position' at index: {mispositioned_field.position}")
    #         error.code = 400
    #         raise error

    @staticmethod
    def _parse_survey_field_db_result_to_dataclass(row: dict) -> SurveyField:
        allowed_fields = set(f.name for f in dataclasses.fields(SurveyField))
        return SurveyField(**{
            **{k: row[k] for k in row.keys() if k in allowed_fields},
            'options': SurveyFieldOptions(**json.loads(row['options'])),

            'id': row['survey_field_id'],
            'created_at': row['survey_field_created_at'],
            'updated_at': row['survey_field_updated_at'],
        })

    @staticmethod
    def _parse_survey_db_result_to_dataclass(row: dict) -> Survey:
        allowed_fields = set(f.name for f in dataclasses.fields(Survey))
        return Survey(**{
            **{k: row[k] for k in row.keys() if k in allowed_fields},

            'id': row['survey_id'],
            'created_at': row['survey_created_at'],
            'updated_at': row['survey_updated_at'],
        })
