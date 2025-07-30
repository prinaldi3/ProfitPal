import argparse
import json
import os
import pp
from .core import parse_data, parse_args
from .config import MEE, JSON_PATH
from .data_bud import DataBud


def main():

    json_path = JSON_PATH

    finDB = parse_data()
    args, parser = parse_args()

    if hasattr(args, "func"):
        args.databud = finDB
        print(args.func(args))  # Call the associated function
    else:
        parser.print_help()  # Print help if no subcommand is given

    
    with open(json_path, 'w') as f:
        json.dump(finDB.data, f)

    return 0

if __name__ == '__main__':
    main()