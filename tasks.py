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


@task
def build_images(ctx):
    """
    Build application docker images
    """
    ctx.run("docker build --file Dockerfile-web --tag web .")
