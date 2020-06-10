import os

from wtforms import BooleanField
from wtforms import IntegerField
from wtforms import StringField

PATH_TO_TERRAFORM_DIRECTORY = "/Users/olevino999/terraform-tmp"
PATH_TO_TERRAFORM_WORKSPACES_DIRECTORY = os.path.join(PATH_TO_TERRAFORM_DIRECTORY, "terraform.tfstate.d")

PATH_TO_TEMPLATES_REPOSITORY = "/Users/olevino999/YC_Terraform_templates"

PATH_TO_TEMPLATES_LIST = os.path.join(PATH_TO_TEMPLATES_REPOSITORY, "projects.yaml")

FORM_TYPES_MAPPING = {
    "string": StringField,
    "file": StringField,
    "bool": BooleanField,
    "int": IntegerField
}
