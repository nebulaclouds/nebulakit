from nebulakit import task, workflow
from nebulakit.image_spec import ImageSpec

image_spec = ImageSpec(packages=["numpy", "pandas"], apt_packages=["git"], registry="", builder="test")


@task(container_image=image_spec)
def t2() -> str:
    return "nebula"


@task(container_image=image_spec)
def t1() -> str:
    return "nebula"


@workflow
def wf():
    t1()
    t2()
