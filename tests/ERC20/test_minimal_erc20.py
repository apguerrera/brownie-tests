from brownie import accounts, web3, Wei, reverts, Contract
from brownie.network.transaction import TransactionReceipt
from brownie.convert import to_address
import pytest

# From settings file
from settings import *

deployer = accounts[0]
token_owner = accounts[1]

# reset the chain after every test case
@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass


######################################
# ERC20 Tests
######################################

def test_erc20_transfer(minimal_erc20):
    tx = minimal_erc20.transfer(accounts[2], '2 ether', {'from': accounts[1]})

    assert minimal_erc20.balanceOf(accounts[1]) == '998 ether'
    assert minimal_erc20.balanceOf(accounts[2]) == '2 ether'

    assert 'Transfer' in tx.events
    assert tx.events['Transfer'] == {'from': accounts[1], 'to': accounts[2], 'tokens': '2 ether'}
