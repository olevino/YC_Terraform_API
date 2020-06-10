from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import SubmitField
from wtforms.validators import DataRequired

from concepts.templates.actions import get_template_full_info
from constants import FORM_TYPES_MAPPING


def generate_variable_form(template_id):
    template_data = get_template_full_info(template_id)

    class NewForm(FlaskForm):
        submit = SubmitField("Run template!")

        operation_id = StringField("operation_id", validators=[DataRequired()])
        operation_id_description = "Generate it yourself and remember"
        template = template_data

        fields = ["operation_id"] + [variable["name"] for variable in template_data["terraform_variables"]]

        render_field = lambda self, field_name: getattr(self, field_name)
        render_description = lambda self, field_name: getattr(self, field_name + "_description")
        render_errors = lambda self, field_name: self.errors.get(field_name) or []

    NewForm.template_id = template_id

    for variable in template_data["terraform_variables"]:
        cls = FORM_TYPES_MAPPING[variable["type"]]
        name = variable["name"]
        field = cls(name, validators=[DataRequired()])
        setattr(NewForm, name, field)
        setattr(NewForm, name + "_description", variable["description"])

    return NewForm


class FolderIdForm(FlaskForm):
    folder_id = StringField("folder_id", validators=[DataRequired()])
    submit = SubmitField("Submit")
