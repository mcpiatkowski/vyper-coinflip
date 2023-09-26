import pytest

from typing import List

from ape.contracts.base import ContractInstance
from ape.exceptions import ContractLogicError
from ape.types.address import AddressType


def test_deployed(coinflip: ContractInstance, owner: AddressType):
    """Test deployed contract.

    How to test vrf_consumer?
    """
    assert coinflip.min_bet() == 1
    assert coinflip.owner() == owner
    assert coinflip.max_players() == 20
    assert coinflip.coinflip_status() == 1


def test_set_max_players_by_owner(coinflip: ContractInstance, owner: AddressType):
    """Test max plyers set by the owner."""
    assert coinflip.max_players() == 20
    coinflip.set_max_players(25, sender=owner)
    assert coinflip.max_players() == 25


def test_set_max_players_by_player(coinflip: ContractInstance, players: List[AddressType]):
    """Test max plyers set by a player."""
    assert coinflip.max_players() == 20
    with pytest.raises(ContractLogicError) as err:
        coinflip.set_max_players(25, sender=players[0])
    assert err.value.args[0] == "Only owner can set maximum number of players."


def test_set_min_bet_by_owner(coinflip: ContractInstance, owner: AddressType):
    """Test min bet set by the owner."""
    assert coinflip.min_bet() == 1
    coinflip.set_min_bet(10, sender=owner)
    assert coinflip.min_bet() == 10


def test_set_min_bet_by_player(coinflip: ContractInstance, players: List[AddressType]):
    """Test min bet set by a player."""
    assert coinflip.min_bet() == 1
    with pytest.raises(ContractLogicError) as err:
        coinflip.set_min_bet(10, sender=players[0])
    assert err.value.args[0] == "Only owner can set minimal bet amount."