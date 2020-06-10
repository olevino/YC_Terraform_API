import os

from concepts.workspaces.actions import create_workspace
from concepts.workspaces.actions import generate_workspace_id
from concepts.workspaces.actions import workspace_exists
from constants import PATH_TO_TEMPLATES_REPOSITORY
from constants import PATH_TO_TERRAFORM_DIRECTORY
from constants import PATH_TO_TERRAFORM_WORKSPACES_DIRECTORY


def terraform_apply(workspace_id, form):
    workspace_dir = os.path.join(PATH_TO_TERRAFORM_WORKSPACES_DIRECTORY, workspace_id)

    command = "cd {terraform_dir};" + \
              "terraform workspace select {workspace_id};" + \
              "echo {template_id} > {template_id_file};" + \
              "terraform apply -auto-approve {variables} {template} 1> {output} 2> {errors} &"

    for variable in form.template["terraform_variables"]:
        if variable["type"] == "file":
            file_path = os.path.join(workspace_dir, variable["name"])
            with open(file_path, "w") as f:
                f.write(getattr(form, variable["name"]).data)
            getattr(form, variable["name"]).data = file_path

    command = command.format(
        terraform_dir=PATH_TO_TERRAFORM_DIRECTORY,
        workspace_id=workspace_id,
        template=os.path.join(PATH_TO_TEMPLATES_REPOSITORY, form.template_id, "terraform"),
        output=os.path.join(workspace_dir, "output"),
        errors=os.path.join(workspace_dir, "errors"),
        variables=' '.join(["-var '{}={}'".format(var["name"], getattr(form, var["name"]).data) for var in form.template["terraform_variables"]]),
        template_id=form.template_id,
        template_id_file=os.path.join(workspace_dir, "template_id")
    )
    print(command)
    os.system(command)


def run_terraform(form):
    workspace = generate_workspace_id(form.folder_id.data, form.operation_id.data)
    if workspace_exists(workspace):
        return

    create_workspace(workspace)

    terraform_apply(workspace, form)
