from nebulakitplugins.flyin import vscode
from nebulakit import task


@task()
@vscode(run_task_first=True)
def t1(a: int, b: int) -> int:
    return a // b
