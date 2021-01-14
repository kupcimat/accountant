from invoke import task


@task
def upgrade_deps(ctx):
    """
    Upgrade application and development dependencies
    """
    ctx.run("pip-compile --generate-hashes requirements.in")
    ctx.run("pip-compile --generate-hashes requirements-dev.in")


@task
def install_deps(ctx):
    """
    Install application and development dependencies
    """
    ctx.run("pip-sync requirements.txt requirements-dev.txt")
