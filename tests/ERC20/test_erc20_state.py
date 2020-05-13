#!/usr/bin/python3

import brownie
from brownie.test import strategy
from brownie import accounts, web3, Wei, rpc

from settings import *


class StateMachine:
    st_eth = strategy('uint256', min_value="1 ether", max_value="100 ether")
    st_owner = strategy('address')
    st_alice = strategy('address')
    st_bob = strategy('address')
    st_charlie = strategy('address')


    def __init__(cls, accounts, contract):
        # deploy the contract at the start of the test
        cls.accounts = accounts
        cls.contract = contract

    def setup(self):
        # zero the deposit amounts at the start of each test run
        self.total_supply = SUPPLY

    def rule_transfer(self, st_owner, st_alice, st_eth):
        balance =  self.contract.balanceOf(st_owner, {'from': st_owner})
        if balance >= st_eth :
            self.contract.transfer(st_alice, st_eth, {'from': st_owner}) 

    def invariant(self):
        # compare the contract deposit amounts with the local record
        assert self.contract.totalSupply() == self.total_supply


def test_state_minimal_erc20(minimal_erc20, accounts, state_machine):
    settings = {"stateful_step_count": 20, "max_examples": 50}
    state_machine(StateMachine, accounts[0:5], minimal_erc20, settings=settings)
