import os
import typing

import rich_click as click

from nebulakit import configuration
from nebulakit.clis.sdk_in_container.backfill import backfill
from nebulakit.clis.sdk_in_container.build import build
from nebulakit.clis.sdk_in_container.constants import CTX_CONFIG_FILE, CTX_PACKAGES, CTX_VERBOSE
from nebulakit.clis.sdk_in_container.fetch import fetch
from nebulakit.clis.sdk_in_container.get import get
from nebulakit.clis.sdk_in_container.init import init
from nebulakit.clis.sdk_in_container.launchplan import launchplan
from nebulakit.clis.sdk_in_container.local_cache import local_cache
from nebulakit.clis.sdk_in_container.metrics import metrics
from nebulakit.clis.sdk_in_container.package import package
from nebulakit.clis.sdk_in_container.register import register
from nebulakit.clis.sdk_in_container.run import run
from nebulakit.clis.sdk_in_container.serialize import serialize
from nebulakit.clis.sdk_in_container.serve import serve
from nebulakit.clis.sdk_in_container.utils import ErrorHandlingCommand, validate_package
from nebulakit.clis.version import info
from nebulakit.configuration.file import NEBULACTL_CONFIG_ENV_VAR, NEBULACTL_CONFIG_ENV_VAR_OVERRIDE
from nebulakit.configuration.internal import LocalSDK
from nebulakit.loggers import cli_logger


@click.group("pynebula", invoke_without_command=True, cls=ErrorHandlingCommand)
@click.option(
    "--verbose", required=False, default=False, is_flag=True, help="Show verbose messages and exception traces"
)
@click.option(
    "-k",
    "--pkgs",
    required=False,
    multiple=True,
    callback=validate_package,
    help="Dot-delineated python packages to operate on. Multiple may be specified (can use commas, or specify the "
    "switch multiple times. Please note that this "
    "option will override the option specified in the configuration file, or environment variable",
)
@click.option(
    "-c",
    "--config",
    required=False,
    type=str,
    help="Path to config file for use within container",
)
@click.pass_context
def main(ctx, pkgs: typing.List[str], config: str, verbose: bool):
    """
    Entrypoint for all the user commands.
    """
    ctx.obj = dict()

    # Handle package management - get from the command line, the environment variables, then the config file.
    pkgs = pkgs or LocalSDK.WORKFLOW_PACKAGES.read() or []
    if config:
        ctx.obj[CTX_CONFIG_FILE] = config
        cfg = configuration.ConfigFile(config)
        # Set here so that if someone has Config.auto() in their user code, the config here will get used.
        if NEBULACTL_CONFIG_ENV_VAR in os.environ:
            cli_logger.info(
                f"Config file arg {config} will override env var {NEBULACTL_CONFIG_ENV_VAR}: {os.environ[NEBULACTL_CONFIG_ENV_VAR]}"
            )
        os.environ[NEBULACTL_CONFIG_ENV_VAR_OVERRIDE] = config
        if not pkgs:
            pkgs = LocalSDK.WORKFLOW_PACKAGES.read(cfg)
            if pkgs is None:
                pkgs = []
    ctx.obj[CTX_PACKAGES] = pkgs
    ctx.obj[CTX_VERBOSE] = verbose


main.add_command(serialize)
main.add_command(package)
main.add_command(local_cache)
main.add_command(init)
main.add_command(run)
main.add_command(register)
main.add_command(backfill)
main.add_command(serve)
main.add_command(build)
main.add_command(metrics)
main.add_command(launchplan)
main.add_command(fetch)
main.add_command(info)
main.add_command(get)
main.epilog

if __name__ == "__main__":
    main()
