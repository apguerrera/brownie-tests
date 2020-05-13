from brownie import accounts, web3, Wei, reverts, rpc
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


def test_init_minimal_erc20(minimal_erc20):
    assert minimal_erc20.name() == NAME
    assert minimal_erc20.symbol() == SYMBOL
    assert minimal_erc20.totalSupply() == SUPPLY
    assert minimal_erc20.decimals() == DECIMALS
    assert minimal_erc20.balanceOf(accounts[OWNER]) == SUPPLY


# The intial Owner should have the total supply, and is able to transfer some tokens to Alice
def test_erc20_transfer(minimal_erc20):
    transfer_amount = Wei('2 ether')
    tx = minimal_erc20.transfer(accounts[ALICE], transfer_amount, {'from': accounts[OWNER]})

    assert minimal_erc20.balanceOf(accounts[OWNER]) == SUPPLY - transfer_amount
    assert minimal_erc20.balanceOf(accounts[ALICE]) == transfer_amount
    assert 'Transfer' in tx.events
    assert tx.events['Transfer'] == {'from': accounts[OWNER], 'to': accounts[ALICE], 'tokens': transfer_amount}

# The Owner should not be able to transfer more than he has
def test_erc20_transfer_not_enough_funds(minimal_erc20):
    with reverts():
        minimal_erc20.transfer(accounts[ALICE], SUPPLY + Wei('1 ether'), {'from': accounts[OWNER]})

# A token owner should be able to approve an amount to be spent
def test_erc20_approve(minimal_erc20):
    tx = minimal_erc20.approve(accounts[ALICE], '5 ether', {'from': accounts[OWNER]})

    assert minimal_erc20.allowance(accounts[OWNER], accounts[ALICE]) == '5 ether'
    assert 'Approval' in tx.events
    assert tx.events['Approval'] == {'tokenOwner': accounts[OWNER], 'spender': accounts[ALICE], 'tokens': '5 ether'}

# With an approval, a spender is able to transfer funds to an account of their choice
def test_erc20_transfer_from(minimal_erc20):
    minimal_erc20.approve(accounts[ALICE], '10 ether', {'from': accounts[OWNER]})
    tx = minimal_erc20.transferFrom(accounts[OWNER], accounts[BOB], '5 ether', {'from': accounts[ALICE]})

    assert minimal_erc20.balanceOf(accounts[OWNER]) == SUPPLY - Wei('5 ether')
    assert minimal_erc20.balanceOf(accounts[BOB]) == '5 ether'
    assert 'Transfer' in tx.events
    assert tx.events['Transfer'] == {'from': accounts[OWNER], 'to': accounts[BOB], 'tokens': '5 ether'}


def test_erc20_transfer_from_not_enough_funds(minimal_erc20):
    minimal_erc20.approve(accounts[ALICE], SUPPLY + Wei('1 ether'), {'from': accounts[OWNER]})
    with reverts():
        minimal_erc20.transferFrom(accounts[OWNER], accounts[BOB], SUPPLY + Wei('1 ether'), {'from': accounts[ALICE]})

def test_erc20_transfer_from_not_enough_approved(minimal_erc20):
    minimal_erc20.approve(accounts[ALICE], Wei('1 ether'), {'from': accounts[OWNER]})
    with reverts():
        minimal_erc20.transferFrom(accounts[OWNER], accounts[BOB],  Wei('2 ether'), {'from': accounts[ALICE]})
