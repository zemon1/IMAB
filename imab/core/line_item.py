gid = 0


class LineItem(object):
    def __init__(self, name, value, paid=False):
        global gid

        self.item_id = gid
        self.name = name
        self.value = value
        self.paid = paid

        gid += 1

    def pay(self):
        if not self.paid:
            self.paid = True
        return self.paid

    def __str__(self):
        return "{}:\t{}\t{}".format(self.name.title(), self.value, self.paid)
