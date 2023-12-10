import typing

import rich_click as click
from rich import print
from rich.panel import Panel
from rich.pretty import Pretty

from nebulakit import Literal
from nebulakit.clis.sdk_in_container.helpers import get_and_save_remote_with_click_context
from nebulakit.core.type_engine import LiteralsResolver
from nebulakit.interaction.string_literals import literal_map_string_repr, literal_string_repr
from nebulakit.remote import NebulaRemote


@click.command("fetch")
@click.option(
    "--recursive",
    "-r",
    is_flag=True,
    help="Fetch recursively, all variables in the URI. This is not needed for directrories as they"
    " are automatically recursively downloaded.",
)
@click.argument("nebula-data-uri", type=str, required=True, metavar="NEBULA-DATA-URI (format nebula://...)")
@click.argument(
    "download-to", type=click.Path(), required=False, default=None, metavar="DOWNLOAD-TO Local path (optional)"
)
@click.pass_context
def fetch(ctx: click.Context, recursive: bool, nebula_data_uri: str, download_to: typing.Optional[str] = None):
    """
    Retrieve Inputs/Outputs for a Nebula Execution or any of the inner node executions from the remote server.

    The URI can be retrieved from the Nebula Console, or by invoking the get_data API.
    """

    remote: NebulaRemote = get_and_save_remote_with_click_context(ctx, project="nebulasnacks", domain="development")
    click.secho(f"Fetching data from {nebula_data_uri}...", dim=True)
    data = remote.get(nebula_data_uri)
    if isinstance(data, Literal):
        p = literal_string_repr(data)
    elif isinstance(data, LiteralsResolver):
        p = literal_map_string_repr(data.literals)
    else:
        p = data
    pretty = Pretty(p)
    panel = Panel(pretty)
    print(panel)
    if download_to:
        remote.download(data, download_to, recursive=recursive)
