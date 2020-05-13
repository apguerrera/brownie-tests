from brownie import *
import pytest

# From settings file
from settings import *

######################################
# Deploy Contracts
######################################


@pytest.fixture(scope='module', autouse=True)
def minimal_erc20(BokkyPooBahsMinimalERC20):

    minimal_erc20 = BokkyPooBahsMinimalERC20.deploy({'from': accounts[DEPLOYER]})
    tx = minimal_erc20.init(accounts[OWNER], SYMBOL, NAME, DECIMALS, SUPPLY, {'from': accounts[DEPLOYER]})
  
    assert tx.events['Transfer'] == {'from': ZERO_ADDRESS, 'to': accounts[OWNER], 'tokens': SUPPLY}
    return minimal_erc20
