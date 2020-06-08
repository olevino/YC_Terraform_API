from flask import render_template

from app import app
from concepts.templates.actions import generate_variable_form
from concepts.templates.actions import get_template_short_info
from concepts.templates.actions import get_templates


@app.route('/templates')
def templates_list():
    templates = get_templates()
    return render_template("templates_list.html", templates=templates)


@app.route('/template/<template_name>', methods=['GET', 'POST'])
def run_request(template_name):
    form = generate_variable_form(template_name)
    form = form()

    if form.validate_on_submit():
        pass

    full_name = get_template_short_info(template_name)["full_name"]
    return render_template("template_variables_form.html", template_name=full_name, form=form, )
