from eth_utils import to_wei
import boa
from tests.conftest import SEND_VALUE

RANDOM_USER = boa.env.generate_address("non_owner")


def test_price_feed_is_correct(coffee, price_feed):
    assert coffee.PRICE_FEED() == price_feed.address


def test_starting_values(coffee, account):
    assert coffee.MINIMUM_USD() == to_wei(5, "ether")
    assert coffee.OWNER() == account


def test_fund_fails_without_enough_eth(coffee):
    with boa.reverts("You must spend more ETH!"):
        coffee.fund()


def test_fund_with_money(coffee, account):
    # Arrange
    boa.env.set_balance(account, SEND_VALUE * 3)
    # Act
    coffee.fund(value=SEND_VALUE)
    # Assert
    funder = coffee.funders(0)
    assert funder == account
    assert coffee.funder_to_amount_funded(funder) == SEND_VALUE


def test_non_owner_cannot_withdraw(coffee_funded, account):
    # Act/Assert
    with boa.env.prank(RANDOM_USER):
        with boa.reverts("Not the contract owner!"):
            coffee_funded.withdraw()


def test_owner_can_withdraw(coffee_funded, account):
    # Act/Assert
    with boa.env.prank(coffee_funded.OWNER()):
        coffee_funded.withdraw()
    assert boa.env.get_balance(coffee_funded.address) == 0


# Mid section workshop
# def test_multiple_funders_owner_can_withdraw(coffee):
#     # Arrange
#     number_of_funders = 10
#     # On pyevm the account might have some balance
#     print(boa.env.get_balance(coffee.OWNER()))
#     for funder_seed in range(number_of_funders):
#         # Generating 10 random funders
#         funder = boa.env.generate_address(funder_seed)
#         boa.env.set_balance(funder, SEND_VALUE)
#         with boa.env.prank(funder):
#             coffee.fund(value=SEND_VALUE)
#     starting_fund_me_balance = boa.env.get_balance(coffee.address)
#     starting_owner_balance = boa.env.get_balance(coffee.OWNER())

#     # Act
#     with boa.env.prank(coffee.OWNER()):
#         coffee.withdraw()

#     # Assert
#     assert boa.env.get_balance(coffee.address) == 0
#     assert starting_fund_me_balance + starting_owner_balance == boa.env.get_balance(
#         coffee.OWNER()
#     )


def test_get_rate(coffee):
    assert coffee.get_eth_to_usd_rate(SEND_VALUE) > 0
