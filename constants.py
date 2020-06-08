import os

from wtforms import BooleanField
from wtforms import IntegerField
from wtforms import TextField

PATH_TO_TEMPLATES_REPOSITORY = "/Users/olevino999/YC_Terraform_templates"

PATH_TO_TEMPLATES_LIST = os.path.join(PATH_TO_TEMPLATES_REPOSITORY, "projects.yaml")

FORM_TYPES_MAPPING = {
    "string": TextField,
    "file": TextField,
    "output": None,
    "bool": BooleanField,
    "int": IntegerField
}
