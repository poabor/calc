import math
import sys
import argparse


def calc_diff(credit_principal, periods, interest):
    i = interest / 12 / 100
    m = 0
    paid_sum = 0
    while credit_principal > paid_sum:
        m += 1
        dm = math.ceil(credit_principal / periods + i * (credit_principal - (credit_principal * (m - 1) / periods)))
        paid_sum += dm
        print('Month ' + str(m) + ': paid out ' + str(dm))
    print()
    print("Overpayment = " + str(paid_sum - credit_principal))


def calc_annuity(credit_principal, monthly_payment, credit_interest, periods):
    # print(credit_principal, monthly_payment, credit_interest, periods)
    answer = None
    if monthly_payment is None:
        answer = 'a'
    elif credit_principal is None:
        answer = 'p'
    elif periods is None:
        answer = 'n'
    if answer is None:
        answer = input('''
        type "n" - for count of months,
        type "a" - for annuity monthly payment,
        type "p" - for credit principal:''').strip()
    if answer == "n":
        # credit_principal = int(input("Enter credit principal:"))
        # monthly_payment = int(input("Enter monthly payment:"))
        # credit_interest = float(input("Enter credit interest:"))

        i = credit_interest / (12 * 100)
        periods = math.ceil(math.log(monthly_payment / (monthly_payment - i * credit_principal), 1 + i))
        years = periods // 12
        m = periods - years * 12
        v_and = "and" if years != 0 and m != 0 else ""
        v_years = str(years) + " years " if years != 0 else ""
        v_months = str(m) + " months" if m != 0 else ""
        print("You need {years}{v_and}{months} to repay this credit!".format(years=v_years,
                                                                             v_and=str(v_and),
                                                                             months=v_months))
        print("Overpayment = " + str(monthly_payment * periods - credit_principal))
    elif answer == "a":
        # credit_principal = int(input("Enter credit principal:"))
        # count_of_periods = int(input("Enter count of periods:"))
        # credit_interest = float(input("Enter credit interest:"))

        i = credit_interest / (12 * 100)
        annuity_payment = math.ceil(credit_principal * (i * pow(1 + i, periods)) /
                                    (pow(1 + i, periods) - 1))
        print("Your annuity payment = {}!".format(annuity_payment))
        print("Overpayment = " + str(annuity_payment * periods - credit_principal))
    elif answer == 'p':
        # monthly_payment = float(input("Enter monthly payment:"))
        # count_of_periods = int(input("Enter count of periods:"))
        # credit_interest = float(input("Enter credit interest:"))

        i = credit_interest / (12 * 100)
        credit_principal = math.floor(monthly_payment /
                                      (i * pow(1 + i, periods) / (pow(1 + i, periods) - 1)))
        print("Your credit principal = {}!".format(credit_principal))
        print("Overpayment = " + str(monthly_payment * periods - credit_principal))


def args_correct(check_args, len_args):
    # print('len_args: ' + str(len_args))
    if int(len_args) < 4:
        print("It's not enough of args")
        return False
    elif check_args.interest is None:
        print('interest is empty')
        return False
    elif not (check_args.type == 'annuity' or check_args.type == 'diff'):
        print("It's not the correct type")
        return False
    elif check_args.type == 'diff' and not check_args.payment is None:
        print('diff and payment is not')
        return False
    elif not check_args.periods is None:
        if check_args.periods < 0:
            print('periods is negative')
            return False
    return True


parser = argparse.ArgumentParser()
parser.add_argument("--type", type=str)
parser.add_argument("--principal", type=int)
parser.add_argument("--payment", type=int)
parser.add_argument("--interest", type=float)
parser.add_argument("--periods", type=int)

args = parser.parse_args()
if args_correct(args, len(sys.argv)):
    if args.type == 'annuity':
        calc_annuity(args.principal, args.payment, args.interest, args.periods)
    else:
        calc_diff(args.principal, args.periods, args.interest)
else:
    print('Incorrect parameters')

