import os

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import SubmitField
from wtforms.validators import DataRequired

from constants import FORM_TYPES_MAPPING
from constants import PATH_TO_TEMPLATES_LIST
from constants import PATH_TO_TEMPLATES_REPOSITORY
from helpers import dict_union
from helpers import get_data_from_yaml


def get_templates():
    data = get_data_from_yaml(PATH_TO_TEMPLATES_LIST)
    return [
        dict_union({"id": id}, get_template_short_info(id))
        for id in data["projects"]
    ]


def get_template_short_info(template_id):
    data = get_template_full_info(template_id)
    return {
        "name": data["name"],
        "description": data["description"]
    }


def get_template_full_info(template_id):
    template_path = os.path.join(PATH_TO_TEMPLATES_REPOSITORY, template_id, "info.yaml")
    data = get_data_from_yaml(template_path)
    return data


def get_template_outputs(template_id):
    return get_template_full_info(template_id)["terraform_outputs"]