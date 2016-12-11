class BillPay(object):

    def __init__(self, bank_balance):
        self.real_balance = bank_balance
        self.theoretical_balance = bank_balance
        self.not_paid = {}
        self.paid = {}

    def pay(self, item):
        if item.pay():
            self.transfer_item(item.item_id)
            self.real_balance -= item.value()

    def transfer_item(self, item_id):
        item = self.not_paid.pop(item_id)
        self.paid[item_id] = item

    def reduce_balances(self, item):
        self.theoretical_balance -= item.value

        if item.get_paid():
            self.real_balance -= item.value

    def add_line_item(self, item):
        self.reduce_balances(item)

        if item.get_paid():
            self.paid[item.item_id] = item
        else:
            self.not_paid[item.item_id] = item
