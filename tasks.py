from invoke import task


ECR_REPOSITORY = "434425786344.dkr.ecr.us-east-2.amazonaws.com"


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
    ctx.run("docker build --file Dockerfile-web --tag accountant-web .")
    ctx.run("docker build --file Dockerfile-worker --tag accountant-worker .")
    ctx.run(f"docker tag accountant-web {ECR_REPOSITORY}/accountant-web:latest")
    ctx.run(f"docker tag accountant-worker {ECR_REPOSITORY}/accountant-worker:latest")


@task(build_images)
def push_images(ctx):
    """
    Build application docker images and push them to docker registry
    """
    ctx.run(f"docker push {ECR_REPOSITORY}/accountant-web:latest")
    ctx.run(f"docker push {ECR_REPOSITORY}/accountant-worker:latest")
