class BillPay(object):

    def __init__(self, bank_balance):
        self.real_balance = bank_balance
        self.theoretical_balance = bank_balance
        self.unpaid = {}
        self.paid = {}

    def pay(self, item_id):
        item = self.unpaid.get(item_id, None)

        if item:
            item.pay_item()
            self.transfer_item_to_paid(item.item_id)
            self.real_balance -= item.value

    def unpay(self, item_id):
        item = self.paid.get(item_id, None)

        if item:
            item.unpay_item()
            self.transfer_item_to_unpaid(item.item_id)
            self.real_balance += item.value

    def transfer_item_to_paid(self, item_id):
        item = self.unpaid.pop(item_id)
        self.paid[item_id] = item

    def transfer_item_to_unpaid(self, item_id):
        item = self.paid.pop(item_id)
        self.unpaid[item_id] = item

    def reduce_balances(self, item):
        self.theoretical_balance -= item.value

        if item.paid:
            self.real_balance -= item.value

    def increase_balances(self, item):
        self.theoretical_balance += item.value
        if item.paid:
            self.real_balance += item.value

    def add_item(self, item):
        self.reduce_balances(item)

        if item.paid:
            self.paid[item.item_id] = item
        else:
            self.unpaid[item.item_id] = item

    def get_item(self, lid):
        p_item = self.paid.get(lid, None)
        up_item = self.unpaid.get(lid, None)

        if p_item:
            return p_item
        elif up_item:
            return up_item

    def remove_item(self, lid):
        p_item = self.paid.pop(lid, None)
        up_item = self.unpaid.pop(lid, None)

        if p_item:
            self.increase_balances(p_item)
        elif up_item:
            self.increase_balances(up_item)

    def update_item_value(self, lid, val):
        item = self.get_item(lid)
        if item:
            self.increase_balances(item)
            item.update_value(val)
            self.reduce_balances(item)

    def get_paid(self):
        return self.paid.values()

    def get_unpaid(self):
        return self.unpaid.values()
