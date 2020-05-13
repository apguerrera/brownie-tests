from brownie import *
import pytest

# From settings file
from settings import *

######################################
# Deploy Contracts
######################################


@pytest.fixture(scope='module', autouse=True)
def minimal_erc20(BokkyPooBahsMinimalERC20):

    deployer = accounts[0]
    token_owner = accounts[1]
    symbol = 'BTN'
    name = 'BASE TOKEN'
    decimals = 18
    fixed_supply = '1000 ether'

    minimal_erc20 = BokkyPooBahsMinimalERC20.deploy({'from': deployer})

    tx = minimal_erc20.init(token_owner, symbol, name, decimals, fixed_supply, {'from': deployer})

    assert tx.events['Transfer'] == {'from': ZERO_ADDRESS, 'to': token_owner, 'tokens': fixed_supply}

    return minimal_erc20
