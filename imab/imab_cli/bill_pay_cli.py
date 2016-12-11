from imab.core.bill_pay import BillPay
from imab.core.line_item import LineItem
from cli_helpers import (
    get_int,
    get_choice
)

class BillPayCLI(object):
    def __init__(self, balance):
        self.bill_pay = BillPay(balance)

    def option_menu(self, options, operations):
        choices = [-1]

        print "Enter your choice:"
        print "-1: Abort Operation"
        for i, item in enumerate(options):
            print i, ":", item
            choices.append(i)

        choice = get_choice(choices)
        if choice == -1:
            print "Operation Aborted"
            return -1
        else:
            return operations[choice]()

    def main_menu(self):
        picks = ["Add Line Item", "Print Report"]
        ops = [self.create_line_item, self.report]

        while True:
            result = self.option_menu(picks, ops)

            if result == -1:
                return

    def create_line_item(self):
        invalid = "Invalid Entry, try again.  You can always use -1 to exit"
        while True:
            res = raw_input("Create Item using this format: Name:amount:paid\n-Name can be anything\n-Amount must be a number\n-Paid can be 'true' or 'false'\n")
            if res == "-1":
                return 0
            elif res.count(":") == 2:
                print res

                if not self.pasre_line_item(res):
                    print invalid
                    continue

            else:
                print invalid

    def pasre_line_item(self, input_string):
        try:
            items = input_string.split(":")
            name = items[0]
            amount = float(items[1])
            paid = items[2]

            if paid == 'true':
                paid = True
            elif paid == 'false':
                paid = False
            else:
                raise InvalidInputException

            line = LineItem(name, amount, paid)

            self.bill_pay.add_line_item(line)

            print "Added: {}".format(line)
            return True
        except InvalidInputException:
            return False

    def report(self):
        sep = "+" + "-"*50 + "+"
        real = self.bill_pay.real_balance
        theo = self.bill_pay.theoretical_balance
        paid = self.sort_list_items(self.bill_pay.get_paid())
        unpaid = self.sort_list_items(self.bill_pay.get_unpaid())

        print sep
        print "|-Report:" + "-"*42 + "|"
        print sep
        print "|-{:<38}{:>10}-|".format("Money Remaining:", real)
        print "|-{:<38}{:>10}-|".format("Money Remaining After All Paid:", theo)
        print sep
        print "+-Paid:" + "-"*44 + "+"
        for i, item in enumerate(paid):
            print "|-{:<2}: {}|".format(i, item)

        print sep
        print "+-Unpaid:" + "-"*42 + "+"
        for i, item in enumerate(unpaid):
            print "|-{:<2}: {}|".format(i, item)

        print sep

    def sort_list_items(self, items):
        def sort_key(item):
            return item.value

        return sorted(items, key=sort_key)


def InvalidInputException(Exception):
    def __init__(self, msg):
        self.super(msg)


if __name__ == "__main__":
    current_balance = get_int("What is your current cumulative bank balance?:\n")

    bpc = BillPayCLI(current_balance)
    bpc.main_menu()
