import importlib

from nebulakit.core.tracker import extract_task_module


def test_dont_use_wrapper_location():
    m = importlib.import_module("tests.nebulakit.unit.core.nebula_functools.decorator_usage")
    get_data_task = getattr(m, "get_data")
    assert "decorator_source" not in get_data_task.name
    assert "decorator_usage" in get_data_task.name

    a, b, c, _ = extract_task_module(get_data_task)
    assert (a, b, c) == (
        "tests.nebulakit.unit.core.nebula_functools.decorator_usage.get_data",
        "tests.nebulakit.unit.core.nebula_functools.decorator_usage",
        "get_data",
    )
