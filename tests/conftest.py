import pytest
from script.deploy import deploy_coffee
from script.deploy_mocks import deploy_feed
from moccasin.config import get_active_network
from eth_utils import to_wei
import boa

SEND_VALUE = to_wei(1, "ether")


@pytest.fixture(scope="session")
def account():
    return get_active_network().get_default_account().address


@pytest.fixture(scope="session")
def price_feed():
    return deploy_feed()


@pytest.fixture(scope="function")
def coffee(price_feed):
    return deploy_coffee(price_feed)


@pytest.fixture(scope="function")
def coffee_funded(coffee, account):
    boa.env.set_balance(account, SEND_VALUE * 10)
    with boa.env.prank(account):
        coffee.fund(value=SEND_VALUE)
    return coffee
