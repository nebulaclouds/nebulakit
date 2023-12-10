from typing import List

from nebulakit import task, workflow


@task
def t1(x: List[int]) -> int:
    return sum(x)


@workflow
def wf(x: List[int] = [1, 2, 3]) -> int:
    return t1(x=x)
