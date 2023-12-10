from __future__ import annotations

import typing

import click

from nebulakit.core.context_manager import NebulaContext
from nebulakit.core.type_engine import TypeEngine
from nebulakit.models.literals import Literal
from nebulakit.models.types import LiteralType


def parse_stdin_to_literal(
    ctx: NebulaContext, t: typing.Type, message: typing.Optional[str], lt: typing.Optional[LiteralType] = None
) -> Literal:
    """
    Parses the user input from stdin and converts it to a literal of the given type.
    """
    from nebulakit.interaction.click_types import NebulaLiteralConverter

    if not lt:
        lt = TypeEngine.to_literal_type(t)
    literal_converter = NebulaLiteralConverter(
        ctx,
        literal_type=lt,
        python_type=t,
        is_remote=False,
    )
    user_input = click.prompt(message, type=literal_converter.click_type)
    try:
        option = click.Option(["--input"], type=literal_converter.click_type)
        v = literal_converter.click_type.convert(user_input, option, click.Context(command=click.Command("")))
        return TypeEngine.to_literal(NebulaContext.current_context(), v, t, lt)
    except Exception as e:
        raise click.ClickException(f"Failed to parse input: {e}")
