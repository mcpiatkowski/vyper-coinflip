import pytest

from ape.contracts.base import ContractInstance
from ape.exceptions import ContractLogicError
from ape.api import AccountAPI

from contract_typing import CoinSide, PlayerStatus, CoinflipStatus


def test_successful_join(
        middle_game: ContractInstance,
        coin_side: CoinSide,
        owner: AccountAPI,
        player_status: PlayerStatus
    ):
    """Test successful join.
    
    Middle game starts with 10$ bet.
    Three players are part of the middle game.
    """
    assert middle_game.players(owner.address).status == player_status.unknown
    txn = middle_game.join(coin_side.tails, sender=owner, value=10)
    player = middle_game.players(owner.address)
    assert len(middle_game.get_all_players()) < 20
    assert middle_game.bag_of_players(3) == owner
    assert player.status == player_status.joined
    assert player.side == coin_side.tails
    assert middle_game.pot() == 40
    join_event = txn.decode_logs(middle_game.Join)[0]
    bet_event = txn.decode_logs(middle_game.Bet)[0]
    assert join_event.sender == owner
    assert join_event.status == player_status.joined
    assert bet_event.sender == owner
    assert bet_event.value == 10


def test_join_with_wrong_bet_amount(
        middle_game: ContractInstance,
        coin_side: CoinSide, 
        owner: AccountAPI,
        player_status: PlayerStatus
    ):
    """Test joining the game with wrong bet amount.
    
    Bet amount must match the one set at the start of the current game.
    """
    assert middle_game.players(owner.address).status == player_status.unknown
    with pytest.raises(ContractLogicError) as err:
        middle_game.join(coin_side.heads, sender=owner, value=100)
    assert err.value.args[0] == "Your bet needs to match current game bet amount."


def test_join_second_time(
        middle_game: ContractInstance,
        coin_side: CoinSide,
        player_one: AccountAPI,
        player_status: PlayerStatus
    ):
    """Test a player joining again for the same game.
    
    Middle game starts with 10$ bet.
    Players one, two and three joined the middle game.
    """
    assert middle_game.players(player_one.address).status == player_status.joined
    with pytest.raises(ContractLogicError) as err:
        middle_game.join(coin_side.tails, sender=player_one, value=10)
    assert err.value.args[0] == "You have already joined you greedy!"


def test_join_when_coinflip_is_done(
        resolved: ContractInstance,
        player_one: AccountAPI,
        coin_side: CoinSide,
        coinflip_status: CoinflipStatus
    ):
    """Test joining when there is no game started."""
    assert resolved.coinflip_status() == coinflip_status.done
    with pytest.raises(ContractLogicError) as err:
        resolved.join(coin_side.heads, sender=player_one)
    assert err.value.args[0] == "Please start the game first."
