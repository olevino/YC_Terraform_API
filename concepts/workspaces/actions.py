import os

from concepts.templates.actions import get_template_outputs
from constants import PATH_TO_TERRAFORM_DIRECTORY
from constants import PATH_TO_TERRAFORM_WORKSPACES_DIRECTORY
from helpers import filter_error_log
from helpers import filter_output_log
from helpers import filter_outputs


def generate_workspace_id(folder_id, operation_id):
    return "{}_{}".format(folder_id, operation_id)


def workspace_exists(workspace_id):
    return os.path.exists(os.path.join(PATH_TO_TERRAFORM_WORKSPACES_DIRECTORY, workspace_id))


def create_workspace(workspace_id):
    command = "cd {}; terraform workspace new {}; terraform init; ".format(PATH_TO_TERRAFORM_DIRECTORY, workspace_id)
    os.system(command)


def get_operations(folder_id):
    result = []
    for file in os.listdir(PATH_TO_TERRAFORM_WORKSPACES_DIRECTORY):
        if file.startswith(folder_id):
            result.append(file.split('_')[1])
    return sorted(result)


def check_operation_status(folder_id, operation_id):
    workspace_dir = os.path.join(PATH_TO_TERRAFORM_WORKSPACES_DIRECTORY, generate_workspace_id(folder_id, operation_id))
    if os.path.exists(os.path.join(workspace_dir, ".terraform.tfstate.lock.info")):
        with open(os.path.join(workspace_dir, "output")) as f:
            output = filter_output_log(f.readlines()[-10:])
        return {"status": "process",
                "outputs": output}

    errors_path = os.path.join(workspace_dir, "errors")
    if os.path.exists(errors_path) and os.path.getsize(errors_path) > 0:
        with open(errors_path, "r") as f:
            errors = filter_error_log(f.readlines())
        return {"status": "error", "errors": errors}

    with open(os.path.join(workspace_dir, "template_id"), "r") as f:
        template_id = f.readline().strip()

    outputs = {name: False for name in get_template_outputs(template_id)}
    result = []
    with open(os.path.join(workspace_dir, "output"), "r") as f:
        for line in f.readlines():
            for output_name in outputs.keys():
                if not outputs[output_name] and line.strip().startswith(output_name + " = "):
                    value = line.split(" = ")[1]
                    result.append({"name": output_name, "value": value})

    return {"status": "success", "outputs": filter_outputs(result)}
