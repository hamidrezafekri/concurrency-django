import pytest

from concurrency.credit.selectors.product import check_product_avaliblity

from concurrency.credit.services.transaction import approve_request, sell_product
from concurrency.users.services import InsufficientFundsError


@pytest.mark.django_db
def test_buy_zero_balance(seller_one_product_1000):
    result = check_product_avaliblity(id=seller_one_product_1000.id)
    assert result == False


@pytest.mark.django_db
def test_increase_credit_buy_product(customer, seller1, seller_one_credit_2000, seller_one_product_1000):
    approve_request(id=seller_one_credit_2000.id)
    seller1.refresh_from_db()
    assert seller1.account_balance == seller_one_credit_2000.amount
    sell_product(customer=customer, product_id=seller_one_product_1000.id)
    seller1.refresh_from_db()
    assert customer.account_balance == seller_one_product_1000.amount
    assert seller1.account_balance == seller_one_product_1000.amount


@pytest.mark.django_db
class TestCase:

    # --------------------------------------------------
    @pytest.fixture(autouse=True)
    def setup_method(self, customer, seller1, seller2, seller_one_product_1000, seller_one_credit_2000,
                     seller_one_product_10000, seller_one_credit_100000,
                     seller_two_product_1000, seller_two_credit_5000 , seller_two_product_3000):
        self.customer = customer
        self.seller1 = seller1
        self.seller2 = seller2
        self.seller_one_product_1000 = seller_one_product_1000
        self.seller_one_credit_2000 = seller_one_credit_2000
        self.seller_one_product_10000 = seller_one_product_10000
        self.seler_one_credit_10000 = seller_one_credit_100000
        self.seller_two_product_1000 = seller_two_product_1000
        self.seller_two_credit_5000 = seller_two_credit_5000
        self. seller_two_product_3000 =  seller_two_product_3000

    def test_buy_zero_balance_seller_one(self):
        with pytest.raises(InsufficientFundsError) as error:
            sell_product(customer=self.customer, product_id=self.seller_one_product_1000.id)
        assert str(error.value) == "Cannot sell because amount exceeds user's account balance."

    def test_increase_seller_one_credit(self):
        approve_request(id=self.seller_one_credit_2000.id)
        self.seller1.refresh_from_db()
        assert self.seller1.account_balance == self.seller_one_credit_2000.amount

    def test_buy_product_seller_one(self):
        approve_request(id=self.seller_one_credit_2000.id)
        self.seller1.refresh_from_db()
        self.customer.refresh_from_db()
        sell_product(customer=self.customer, product_id=self.seller_one_product_1000.id)
        self.customer.refresh_from_db()
        self.seller1.refresh_from_db()
        assert self.customer.account_balance == self.seller_one_product_1000.amount
        assert self.seller1.account_balance == 1000.00

    def test_buy_product_with_higher_that_balance(self):
        approve_request(id=self.seller_one_credit_2000.id)
        self.seller1.refresh_from_db()
        self.customer.refresh_from_db()
        with pytest.raises(InsufficientFundsError) as error:
            sell_product(customer=self.customer, product_id=self.seller_one_product_10000.id)
        assert str(error.value) == "Cannot sell because amount exceeds user's account balance."

    def test_multiple_product_and_check_balance(self):
        approve_request(id=self.seller_one_credit_2000.id)
        approve_request(id = self.seller_two_credit_5000.id)
        self.seller1.refresh_from_db()
        self.seller2.refresh_from_db()
        assert self.seller1.account_balance == self.seller_one_credit_2000.amount
        assert self.seller2.account_balance == self.seller_two_credit_5000.amount
        with pytest.raises(InsufficientFundsError) as error:
            sell_product(customer  = self.customer , product_id= self.seller_one_product_10000.id)
        assert str(error.value) == "Cannot sell because amount exceeds user's account balance."
        self.seller1.refresh_from_db()
        assert self.seller1.account_balance == self.seller_one_credit_2000.amount
        assert self.customer.account_balance == 0.00
        assert self.seller1.account_balance == 2000.00
        sell_product(customer = self.customer , product_id=self.seller_one_product_1000.id)
        self.customer.refresh_from_db()
        self.seller1.refresh_from_db()
        assert self.customer.account_balance == 1000.00
        assert self.seller1.account_balance == 1000.00
        sell_product(customer = self.customer ,product_id = self.seller_two_product_1000.id)
        self.customer.refresh_from_db()
        self.seller2.refresh_from_db()
        self.seller1.refresh_from_db()
        assert self.customer.account_balance == 2000
        assert self.seller1.account_balance ==1000
        assert self.seller2.account_balance == 4000
        sell_product(customer = self.customer ,product_id = self.seller_two_product_1000.id)
        self.customer.refresh_from_db()
        self.seller2.refresh_from_db()
        self.seller1.refresh_from_db()
        assert self.customer.account_balance == 3000
        assert self.seller1.account_balance == 1000
        assert self.seller2.account_balance == 3000
        sell_product(customer = self.customer ,product_id = self.seller_two_product_1000.id)
        self.customer.refresh_from_db()
        self.seller2.refresh_from_db()
        self.seller1.refresh_from_db()
        assert self.customer.account_balance == 4000
        assert self.seller1.account_balance == 1000
        assert self.seller2.account_balance == 2000
        sell_product(customer = self.customer ,product_id = self.seller_two_product_1000.id)
        self.customer.refresh_from_db()
        self.seller2.refresh_from_db()
        self.seller1.refresh_from_db()
        assert self.customer.account_balance == 5000
        assert self.seller1.account_balance == 1000
        assert self.seller2.account_balance == 1000
        with pytest.raises(InsufficientFundsError) as error:
            sell_product(customer=self.customer, product_id=self.seller_two_product_3000.id)
        assert str(error.value) == "Cannot sell because amount exceeds user's account balance."







