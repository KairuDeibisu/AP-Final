"""
cli.py

user commands
"""
import sys
import argparse
from Note.executor import Executor, ListMenuExecutor


def list_menu(parser):
    pass


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="Note")

    menus_parser = parser.add_subparsers(dest="menu", title="Commands")

    list_menu_parser = build_list_menu(menus_parser)
    list_menu_parser.set_defaults(func=ListMenuExecutor)

    args = parser.parse_args(argv)

    Executor(vars(args)).execute()

    return 0


def build_list_menu(menus_parser):
    list_parser = menus_parser.add_parser(name="list", help="View Notes")
    list_parser.add_argument(
        "-l",
        "--limit",
        type=int,
        default=5,
        help="Limit list output, defaults to 5"
    )
    list_parser_filter_group = list_parser.add_argument_group(
        "filters")
    list_parser_filter_group.add_argument(
        "-t",
        "--tag",
        type=str,
        nargs=1,
        default=None,
        help="Filter list output by tag"
    )
    return list_parser
