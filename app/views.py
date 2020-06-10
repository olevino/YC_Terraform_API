from flask import redirect
from flask import render_template

from app import app
from concepts.templates.actions import get_template_short_info
from concepts.templates.actions import get_templates
from concepts.terraform.actions import run_terraform
from concepts.workspaces.actions import check_operation_status
from concepts.workspaces.actions import get_operations
from forms import FolderIdForm
from forms import generate_variable_form


@app.route('/')
def main():
    return render_template("main.html")

@app.route('/templates')
def templates_list():
    templates = get_templates()
    return render_template("templates_list.html", templates=templates)


@app.route('/template/<template_id>', methods=['GET', 'POST'])
def run_request(template_id):
    form = generate_variable_form(template_id)
    form = form()

    if form.validate_on_submit():
        run_terraform(form)
        return render_template("operation_in_process.html",
                               operation_id=form.operation_id.data,
                               folder_id=form.folder_id.data)

    name = get_template_short_info(template_id)["name"]
    return render_template("template_variables_form.html", template_name=name, form=form, )


@app.route('/check_state', methods=['GET', 'POST'])
def check_state():
    form = FolderIdForm()
    if form.validate_on_submit():
        return redirect("/check_state/{}".format(form.folder_id.data))

    return render_template("check_result.html", form=form)


@app.route('/check_state/<folder_id>')
def list_operations(folder_id):
    return render_template("get_operations.html", folder_id=folder_id, operations=get_operations(folder_id))


@app.route('/check_state/<folder_id>/<operation_id>')
def check_operation_state(folder_id, operation_id):
    result = check_operation_status(folder_id, operation_id)
    if result["status"] == "error":
        return render_template("operation_failed.html",
                               operation_id=operation_id,
                               folder_id=folder_id,
                               errors=result["errors"])
    if result["status"] == "process":
        return render_template("operation_in_process.html",
                               operation_id=operation_id,
                               folder_id=folder_id,
                               outputs=result["outputs"])


    if result["status"] == "success":
        return render_template("operation_success.html",
                               operation_id=operation_id,
                               folder_id=folder_id,
                               outputs=result["outputs"])

    raise Exception("Logical error. Invalid operation status: {}".format(result["status"]))
