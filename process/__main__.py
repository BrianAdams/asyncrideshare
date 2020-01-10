#!/usr/bin/env python3
import sys
import os
import asyncio
import click
import json
from loguru import logger

# pylint: disable=no-name-in-module
import process.fastapi as httpsrv
from process.controller import Controller
from process.repository import Repository
from process.leaderboard import LeaderBoard


# init
repository = None
leaderboard = None
controller = None
file_watcher = None


@click.group()
@click.option("--raw_data_path")
@click.option("--incomming_data_path")
def cli(raw_data_path=None, incomming_data_path="data/incomming"):
    """
    This applciation will process ride share/taxi raiting and make a leaderboard that is avaiable via web services.
    """
    if raw_data_path:
        os.environ["raw_data_path"] = raw_data_path

    if incomming_data_path:
        os.environ["incomming_data_path"] = incomming_data_path

    global repository
    global leaderboard
    global controller

    repository = Repository(file=raw_data_path)
    leaderboard = LeaderBoard(repository)
    controller = Controller(leaderboard)


@click.command(help="Start the API server")
@click.option("--service_port")
def server(service_port):
    if service_port:
        os.environ["SERVICE_PORT"] = service_port
    httpsrv.start(controller)
    return True


async def lb_async(controller):
    result = await controller.get_leaderboard()
    print(json.dumps(result["stats"], indent=4, sort_keys=True))


@click.command(help="Dump the leaderboard")
def lb():
    asyncio.run(lb_async(controller))


def main():
    # pylint: disable=no-value-for-parameter
    cli()
    return True


cli.add_command(server)
cli.add_command(lb)

if __name__ == "__main__":
    sys.exit(main())
