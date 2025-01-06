from moccasin.config import get_active_network
from src import buy_me_a_coffee
from moccasin.boa_tools import VyperContract

# from script.deploy_mocks import deploy_feed


def deploy_coffee(price_feed: VyperContract):
    coffee: VyperContract = buy_me_a_coffee.deploy(price_feed)
    active_network = get_active_network()
    if (
        active_network.has_explorer()
        and active_network.is_local_or_forked_network() is False
    ):
        result = active_network.moccasin_verify(coffee)
        result.wait_for_verification()
    return coffee


def moccasin_main():
    active_network = get_active_network()
    price_feed: VyperContract = active_network.manifest_named("price_feed")
    print(
        f"On network: {active_network.name}, using price_feed at {price_feed.address}"
    )
    return deploy_coffee(price_feed)

    # price_feed: VyperContract = deploy_feed()
    # coffee = buy_me_a_coffee.deploy(price_feed)
    # print(f"Deployed to {coffee.address}")

    # print(coffee.get_eth_to_usd_rate(1000))
