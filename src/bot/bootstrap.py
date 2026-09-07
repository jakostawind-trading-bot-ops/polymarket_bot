import argparse
from dataclasses import dataclass
from collections.abc import Sequence

@dataclass(frozen=True, slots=True)
class BootstrapSettings:
    nats_url: str
    
def parse_cli_args(cli_args: Sequence[str] | None = None) -> BootstrapSettings:
    
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    
    parser.add_argument(
        "--nats-url",
        type=str,
        required=True,
    )
    
    args = parser.parse_args(cli_args)
    
    return BootstrapSettings(
        nats_url=args.nats_url
    )