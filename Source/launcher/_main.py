from .subparsers.player import _
from .subparsers.server import _
from .subparsers.studio import _

from .subparsers.aux_tasks.clear_appdata import _
from .subparsers.aux_tasks.download import _

import launcher.routines._logic as routine_logic
import launcher.subparsers._logic as sub_logic
import argparse

MODE_ALIASES = {
    n: m
    for m in sub_logic.launch_mode
    if m != sub_logic.launch_mode.ALWAYS
    for n in [
        m.name.lower(),
    ]
}


def parse_args(parser: argparse.ArgumentParser) -> routine_logic.routine:
    mode_parser = parser.add_subparsers(
        dest='mode',
    )
    sub_parsers = {
        m: mode_parser.add_parser(n)
        for n, m in MODE_ALIASES.items()
    }

    args = parser.parse_known_args()[0]
    mode = MODE_ALIASES[args.mode]
    chosen_sub_parser = sub_parsers[mode]

    sub_logic.ADD_MODE_ARGS.call_subparser(
        mode,
        parser,
        chosen_sub_parser,
    )
    sub_logic.ADD_MODE_ARGS.call_auxs(
        mode,
        parser,
        chosen_sub_parser,
    )
    args = parser.parse_args()
    routine = routine_logic.routine(
        *sub_logic.SERIALISE_ARGS.call_subparser(
            mode,
            parser,
            args,
        )
    )
    sub_logic.SERIALISE_ARGS.call_auxs(
        mode,
        parser,
        args,
        routine,
    )
    return routine


def process(parser: argparse.ArgumentParser):
    routine = parse_args(parser)
    try:
        routine.wait()
    except KeyboardInterrupt:
        pass
    finally:
        del routine
