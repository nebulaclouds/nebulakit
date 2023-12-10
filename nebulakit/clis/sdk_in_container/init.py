import rich_click as click
from cookiecutter.main import cookiecutter


@click.command("init")
@click.option(
    "--template",
    default="simple-example",
    help="cookiecutter template folder name to be used in the repo - https://github.com/nebulaclouds/nebulakit-python-template.git",
)
@click.argument("project-name")
def init(template, project_name):
    """
    Create nebula-ready projects.
    """
    config = {
        "project_name": project_name,
        "app": "nebula",
        "workflow": "my_wf",
    }
    cookiecutter(
        "https://github.com/nebulaclouds/nebulakit-python-template.git",
        checkout="main",
        no_input=True,
        # We do not want to clobber existing files/directories.
        overwrite_if_exists=False,
        extra_context=config,
        # By specifying directory we can have multiple templates in the same repository,
        # as described in https://cookiecutter.readthedocs.io/en/1.7.2/advanced/directories.html.
        # The idea is to extend the number of templates, each in their own subdirectory, for example
        # a tensorflow-based example.
        directory=template,
    )

    click.echo(
        f"Visit the {project_name} directory and follow the next steps in the Getting started guide (https://docs.nebula.org/en/latest/getting_started.html) to proceed."
    )
