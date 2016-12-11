gid = 0


class LineItem(object):
    def __init__(self, name, value, paid=False):
        global gid

        self.item_id = gid
        self.name = name
        self.value = value
        self.paid = paid

        gid += 1

    def pay_item(self):
        self.paid = True

    def unpay_item(self):
        self.paid = False

    def update_value(self, value):
        self.value = value

    def __str__(self):
        return "{}: {}, {}".format(self.item_id, self.name.title(), self.value)
