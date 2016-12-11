import pytest
from imab.core.bill_pay import BillPay
from imab.core.line_item import LineItem


@pytest.fixture
def bill_pay():
    return BillPay(2000)


@pytest.fixture
def food_item():
    return LineItem("Food", 600, False)


@pytest.fixture
def dog_item():
    return LineItem("Olivia", 500, True)


def test_add_unpaid_item_only_reduces_theoretical_balance(bill_pay, food_item):
    assert bill_pay.real_balance == 2000
    assert bill_pay.theoretical_balance == 2000
    bill_pay.add_item(food_item)
    assert bill_pay.real_balance == 2000
    assert bill_pay.theoretical_balance == 1400


def test_add_paid_item_reduces_both_balances(bill_pay, dog_item):
    assert bill_pay.real_balance == 2000
    assert bill_pay.theoretical_balance == 2000
    bill_pay.add_item(dog_item)
    assert bill_pay.real_balance == 1500
    assert bill_pay.theoretical_balance == 1500


def test_pay_item_reduces_real_balance_and_moves_item_to_paid(bill_pay, food_item):
    bill_pay.add_item(food_item)
    assert len(bill_pay.paid.values()) == 0
    assert len(bill_pay.unpaid.values()) == 1
    assert bill_pay.real_balance == 2000

    bill_pay.pay(food_item.item_id)

    assert len(bill_pay.paid.values()) == 1
    assert len(bill_pay.unpaid.values()) == 0
    assert bill_pay.real_balance == 1400


def test_unpay_item_increases_real_balance_and_moves_item_to_unpaid(bill_pay, dog_item):
    bill_pay.add_item(dog_item)
    assert len(bill_pay.paid.values()) == 1
    assert len(bill_pay.unpaid.values()) == 0
    assert bill_pay.real_balance == 1500

    bill_pay.unpay(dog_item.item_id)

    assert len(bill_pay.paid.values()) == 0
    assert len(bill_pay.unpaid.values()) == 1
    assert bill_pay.real_balance == 2000


def test_remove_item_removes_item_and_restores_balances(bill_pay, dog_item):
    bill_pay.add_item(dog_item)
    assert bill_pay.real_balance == 1500
    assert bill_pay.theoretical_balance == 1500

    bill_pay.remove_item(dog_item.item_id)

    assert len(bill_pay.paid.values()) == 0
    assert len(bill_pay.unpaid.values()) == 0
    assert bill_pay.real_balance == 2000
    assert bill_pay.theoretical_balance == 2000


def test_update_item_changes_paid_item_value_and_balances(bill_pay, dog_item):
    bill_pay.add_item(dog_item)
    assert bill_pay.real_balance == 1500
    assert bill_pay.theoretical_balance == 1500

    bill_pay.update_item_value(dog_item.item_id, 1000)

    assert bill_pay.real_balance == 1000
    assert bill_pay.theoretical_balance == 1000


def test_update_item_changes_unpaid_item_value_and_balances(bill_pay, food_item):
    bill_pay.add_item(food_item)
    assert bill_pay.real_balance == 2000
    assert bill_pay.theoretical_balance == 1400

    bill_pay.update_item_value(food_item.item_id, 1000)

    assert bill_pay.real_balance == 2000
    assert bill_pay.theoretical_balance == 1000
