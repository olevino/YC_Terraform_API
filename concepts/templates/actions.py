import os

from flask_wtf import Form
from wtforms.validators import DataRequired

from constants import FORM_TYPES_MAPPING
from constants import PATH_TO_TEMPLATES_LIST
from constants import PATH_TO_TEMPLATES_REPOSITORY
from helpers import dict_union
from helpers import get_data_from_yaml


def get_templates():
    data = get_data_from_yaml(PATH_TO_TEMPLATES_LIST)
    return [
        dict_union({"short_name": template_name}, get_template_short_info(template_name))
        for template_name in data["projects"]
    ]


def get_template_short_info(template_name):
    data = get_template_full_info(template_name)
    return {
        "full_name": data["name"],
        "description": data["description"]
    }


def get_template_full_info(template_name):
    template_path = os.path.join(PATH_TO_TEMPLATES_REPOSITORY, template_name, "info.yaml")
    data = get_data_from_yaml(template_path)
    return data


def get_template_terraform_variables(template_name):
    return get_template_full_info(template_name)["terraform_variables"]


def get_template_packer_variables(template_name):
    return get_template_full_info(template_name)["packer_variables"]


def generate_variable_form(template_name):
    DESCRIPTION_SUFFIX = "_description"

    class NewForm(Form):
        pass

    def render_field(self, field_name):
        return getattr(self, field_name)

    def render_description(self, field_name):
        return getattr(self, field_name + DESCRIPTION_SUFFIX)

    def render_errors(self, field_name):
        return self.errors.get(field_name) or []

    NewForm.render_field = render_field
    NewForm.render_description = render_description
    NewForm.render_errors = render_errors

    variables = {}
    for variable in get_template_terraform_variables(template_name) + get_template_packer_variables(template_name):
        variables[variable["name"]] = variable

    variables = [v for k, v in variables.items()]

    variable_list = []

    for variable in variables:
        cls = FORM_TYPES_MAPPING[variable["type"]]
        if cls is None:
            continue
        name = variable["name"]
        field = cls(name, validators=[DataRequired()])
        setattr(NewForm, name, field)
        setattr(NewForm, name + DESCRIPTION_SUFFIX, variable["description"])
        variable_list.append(name)

    setattr(NewForm, "fields", variable_list)

    return NewForm
