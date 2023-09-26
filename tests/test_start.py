import pytest

from ape.contracts.base import ContractInstance
from ape.exceptions import ContractLogicError
from ape.api import AccountAPI

from contract_typing import CoinSide, PlayerStatus


def test_successful_start(
        coinflip: ContractInstance,
        coin_side: CoinSide,
        player_status: PlayerStatus,
        player_one: AccountAPI
    ):
    """Test successfull start."""
    assert coinflip.players(player_one.address).status == player_status.unknown
    txn = coinflip.start(coin_side.heads, value=1, sender=player_one)
    player = coinflip.players(player_one.address)
    assert coinflip.bag_of_players(0) == player_one
    assert player.status == player_status.joined
    assert player.side == coin_side.heads
    join_event = txn.decode_logs(coinflip.Join)[0]
    bet_event = txn.decode_logs(coinflip.Bet)[0]
    assert join_event.sender == player_one
    assert join_event.status == player_status.joined
    assert bet_event.sender == player_one
    assert bet_event.value == 1
    assert coinflip.pot() == 1


def test_start_without_bet(coinflip: ContractInstance, coin_side: CoinSide, player_one: AccountAPI):
    """Test starting the game with less value than a minimal bet."""
    with pytest.raises(ContractLogicError) as err:
        coinflip.start(coin_side.heads, value=0, sender=player_one)
    assert err.value.args[0] == "Gimme moar coins! Minimal bet is 1$."


def test_start_while_open(middle_game: ContractInstance, coin_side: CoinSide, owner: AccountAPI):
    """Test starting the game while the other one is open."""
    with pytest.raises(ContractLogicError) as err:
        middle_game.start(coin_side.heads, sender=owner, value=10)
    assert err.value.args[0] == "Coinflip is in progress. Try to join the game."
