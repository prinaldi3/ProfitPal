import argparse
import os
import json 
import pprint
from datetime import date 

json_path = 'financial_data.json'
MEE = 2500 #Monthly expenses estimate


SavingsAccounts = {
    "liquid": 9000, 
    "ira": 8750,
    "schwab": 16000
}

OnHand = {
    "cash": 100,
    "checking": 500
}

MonthlyEarnings = {
    1: 0, 
    2: 0,
    3: 0, 
    4: 0, 
    5: 0, 
    6: 0, 
    7: 0, 
    8: 0, 
    9: 0,
    10: 0, 
    11: 0, 
    12: 0
}

GigDiary = {
    1: [],
    2: [],
    3: [],
    4: [],
    5: [],
    6: [],
    7: [],
    8: [],
    9: [],
    10: [],
    11: [],
    12: []
}

def save_gig_info(args):
    GigDiary[args.month].append( (args.day, args.amt) )
    MonthlyEarnings[args.month] += args.amt

    date_str = str(args.month) + "/" + str(args.day) + "/" + str(date.today().year)
    return "Logged a gig on " + date_str + " for $" + str(args.amt)
    
def update_account(args):
    chg = 0
    if args.op == "+":
        chg = args.amt
    if args.op == "-":
        chg = 0 - args.amt

    if args.savings:
        SavingsAccounts[args.acc] += chg
    else:
        OnHand[args.acc] += chg

def single_projection(args):
    #get_current_month
    current_month = date.today().month

    expenses = MEE * (args.month - current_month)

    #use minimum nonzero monthly earning to project (FIX)
    ME = min(list(MonthlyEarnings.values())) #monthly earnings
    
    proj_revenue = MonthlyEarnings[current_month] + ME * (args.month - current_month - 1)
    return "Projected profits in _____: " + str(proj_revenue - expenses)

def quickprint(args):
    pprint.pprint(data)

def display_profit_summary_td():
    pass

def display_profit_summary_proj():
    pass

def generate_gig_diary():
    pass

def parse():
    parser = argparse.ArgumentParser()

    global_parser = argparse.ArgumentParser(prog="pp")

    subparsers = global_parser.add_subparsers(

        dest="command", help="Available commands: log, project, view, update, summarize. Log gigs, make projections, view earnings summaries, store/organize/consolidate tax-relevant info")
    
    arg_template = {

        "dest": "",
        "type": int,
        "nargs": "*",
        "metavar": "",
        "help": ""
    }

    #Log a gig
    log_parser = subparsers.add_parser("log", help="Log a gig. Requires a month (int), day (int), and amount earned (float)")
    log_parser.add_argument("-m", "--month", type=int, choices=range(1,13), default=1)
    log_parser.add_argument("-d", "--day", type=int, choices=range(1, 32), default=1)
    log_parser.add_argument("--amt", type=float, default=0)
    log_parser.set_defaults(func=save_gig_info)

    #Make a projection
    proj_parser = subparsers.add_parser("project", help="Project profit a number of months in the future")
    proj_parser.add_argument("-m", "--month", type=int,choices=range(1, 13), default=12)
    proj_parser.set_defaults(func=single_projection)

    #Quickview contents of financial_data.json
    quickview_parser = subparsers.add_parser("quickview", help="Pretty prints data in financial_data.json file")
    quickview_parser.set_defaults(func=quickprint)
    
    
    #Set estimate parameters
    set_params_parser = subparsers.add_parser("set")

    #Update accounts
    update_parser = subparsers.add_parser("update")
    update_parser.add_argument("-s", "--savings", action="store_true")
    update_parser.add_argument("--amt", type=float)
    update_parser.add_argument("--acc", type=str, choices=['liquid', 'ira', 'schwab', 'cash', 'checking'])
    update_parser.add_argument("--op", type=str, choices=["+", "-"])
    update_parser.set_defaults(func=update_account)


    #Summarize info
    summary_parser = subparsers.add_parser("summarize", help="Summarize profits to date, or a proj")
    group = summary_parser.add_mutually_exclusive_group(required=True)


    group.add_argument("-t", "--to_date", action="store_true")
    group.add_argument("-p", "--projection", action="store_true")


    args = global_parser.parse_args()
    return args, global_parser


if __name__ == "__main__":

    data = []

    """
    Retrieve local financial data, stored as financial_data.json in this directory?
    """
    if not os.path.exists(json_path):
        # Create the file with an empty JSON object if it doesn't exist
        with open(json_path, 'w') as f:
            data = [SavingsAccounts, OnHand, MonthlyEarnings, GigDiary]
            json.dump(data, f)
        print(f"'{json_path}' created as it did not exist.")
    else:
        print(f"'{json_path}' already exists.")

        with open(json_path, 'r') as f:
            data = json.loads(f.read())
            SavingsAccounts = data[0]
            OnHand = data[1]
            MonthlyEarnings = {int(k): data[2][k] for k in data[2]}
            GigDiary = {int(k): data[3][k] for k in data[3]}

    args, parser = parse()

    if hasattr(args, "func"):
        print(args.func(args))  # Call the associated function
    else:
        parser.print_help()  # Print help if no subcommand is given

    
    with open(json_path, 'w') as f:
        json.dump([SavingsAccounts, OnHand, MonthlyEarnings, GigDiary], f)

    