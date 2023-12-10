import rich
import rich_click as click
from rich.panel import Panel

from nebulakit.clis.sdk_in_container.helpers import get_and_save_remote_with_click_context
from nebulakit.remote import NebulaRemote

Content = """
This CLI is meant to be used within a virtual environment that has Nebulakit installed. Ideally it is used to iterate on your Nebula workflows and tasks.

Nebulakit Version: [cyan]{version}[reset]
Nebula Backend Endpoint: [cyan]{endpoint}
"""


@click.command("info")
@click.pass_context
def info(ctx: click.Context):
    """
    Print out information about the current Nebula Python CLI environment - like the version of Nebulakit, backend endpoint
    currently configured, etc.
    """
    import nebulakit

    remote: NebulaRemote = get_and_save_remote_with_click_context(ctx, project="nebulasnacks", domain="development")
    c = Content.format(version=nebulakit.__version__, endpoint=remote.client.url)
    rich.print(Panel(c, title="Nebulakit CLI Info", border_style="purple", padding=(1, 1, 1, 1)))
