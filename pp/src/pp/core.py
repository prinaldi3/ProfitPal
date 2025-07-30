import pp.data_bud as data_bud
from .config import MEE, JSON_PATH
from .data_bud import DataBud
import json
from datetime import date 
import pprint
import argparse
import os



def save_gig_info(args):
    db = args.databud
    db.GigDiary[args.month].append( (args.day, args.amt) )
    db.MonthlyEarnings[args.month] += args.amt

    date_str = str(args.month) + "/" + str(args.day) + "/" + str(date.today().year)
    return "Logged a gig on " + date_str + " for $" + str(args.amt)
    
def update_account(args):
    db = args.databud
    chg = 0
    if args.op == "+":
        chg = args.amt
    if args.op == "-":
        chg = 0 - args.amt

    if args.savings:
        db.SavingsAccounts[args.acc] += chg
    else:
        db.OnHand[args.acc] += chg

def single_projection(args):
    db = args.databud
    
    #get_current_month
    current_month = date.today().month

    expenses = MEE * (args.month - current_month)

    #use minimum nonzero monthly earning to project (FIX)
    ME = min(list(db.MonthlyEarnings.values())) #monthly earnings
    
    proj_revenue = db.MonthlyEarnings[current_month] + ME * (args.month - current_month - 1)
    return "Projected profits in _____: " + str(proj_revenue - expenses)

def quickprint(args):
    db = args.databud
    pprint.pprint(db.data)

def set_param(args):
    MEE = args.mee

def parse_data():

    data = []
    DB = None
    json_path = JSON_PATH
    """
    Retrieve local financial data, stored as financial_data.json in this directory?
    """

    if not os.path.exists(json_path):
        # Create the file with an empty JSON object if it doesn't exist
        with open(json_path, 'w') as f:
            DB = DataBud()
            json.dump([DB.data], f)
        print(f"'{json_path}' created as it did not exist.")
    else:

        with open(json_path, 'r') as f:
            data = json.loads(f.read())
            DB = DataBud(data)
    
    return DB

def parse_args():
    parser = argparse.ArgumentParser()

    global_parser = argparse.ArgumentParser(prog="pp")
    global_parser.add_argument('-d', '--databud', type=DataBud)

    subparsers = global_parser.add_subparsers(

        dest="command", help="Available commands: log, project, view, update, summarize.")
    
    arg_template = {

        "dest": "",
        "type": "",
        "nargs": "*",
        "metavar": "",
        "help": ""
    }

    #Log a gig
    log_parser = subparsers.add_parser("log", help="Log a gig. Requires a month (-m int), day (-d int), and amount earned (--amt float)")
    log_parser.add_argument("-m", "--month", type=int, choices=range(1,13), default=1)
    log_parser.add_argument("-d", "--day", type=int, choices=range(1, 32), default=1)
    log_parser.add_argument("--amt", type=float, default=0)
    log_parser.set_defaults(func=save_gig_info)

    #Make a projection
    proj_parser = subparsers.add_parser("project", help="Project profit a number of (-m) months in the future")
    proj_parser.add_argument("-m", "--month", type=int,choices=range(1, 13), default=12)
    proj_parser.set_defaults(func=single_projection)

    #Quickview contents of financial_data.json
    quickview_parser = subparsers.add_parser("quickview", help="Pretty prints data in financial_data.json file")
    quickview_parser.set_defaults(func=quickprint)
    
    #Set estimate parameters
    set_params_parser = subparsers.add_parser("set", help="Set a parameter, like Monthly expense estimate (MEE)")
    set_params_parser.add_argument("--mee", help="Monthly expense estimate")
    set_params_parser.set_defaults(func=set_param)

    #Update accounts
    update_parser = subparsers.add_parser("update", help="Update a savings/on hand account by (--op) +/- (--amt) amount.")
    update_parser.add_argument("-s", "--savings", action="store_true")
    update_parser.add_argument("--amt", type=float)
    update_parser.add_argument("--acc", type=str, choices=['liquid', 'ira', 'schwab', 'cash', 'checking'])
    update_parser.add_argument("--op", type=str, choices=["+", "-"])
    update_parser.set_defaults(func=update_account)

    #Summarize info
    summary_parser = subparsers.add_parser("summarize", help="Summarize profits and earnings over the past 3/6/12 months, or project profits 3/6/12 months into the future")
    group = summary_parser.add_mutually_exclusive_group(required=True)

    group.add_argument("-t", "--to_date", action="store_true")
    group.add_argument("-p", "--projection", action="store_true")

    args = global_parser.parse_args()
    return args, global_parser

def display_profit_summary_td():
    pass

def display_profit_summary_proj():
    pass

def generate_gig_diary():
    pass
