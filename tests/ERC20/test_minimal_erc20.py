from brownie import *
from brownie.network.transaction import TransactionReceipt
from brownie.convert import to_address
import pytest

# From settings file
from settings import *



# reset the chain after every test case
@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass


######################################
# ERC20 Tests
######################################

def test_erc20_transfer(minimal_erc20):
    receiver = accounts[2]
    transfer_amount = Wei('2 ether')
    tx = minimal_erc20.transfer(receiver, transfer_amount, {'from': accounts[OWNER]})

    assert minimal_erc20.balanceOf(accounts[OWNER]) == SUPPLY - transfer_amount
    assert minimal_erc20.balanceOf(receiver) == transfer_amount

    assert 'Transfer' in tx.events
    assert tx.events['Transfer'] == {'from': accounts[OWNER], 'to': receiver, 'tokens': transfer_amount}
