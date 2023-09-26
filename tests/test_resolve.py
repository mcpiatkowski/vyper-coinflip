from typing import List

import pytest

from ape.contracts.base import ContractInstance
from ape.exceptions import ContractLogicError
from ape.api import AccountAPI

from contract_typing import CoinSide, PlayerStatus, CoinflipStatus


def test_successful_resolve(
        middle_game: ContractInstance,
        player_one: AccountAPI,
        player_status: PlayerStatus,
        coinflip_status: CoinflipStatus
    ):
    """Successful game resolve."""
    assert middle_game.players(player_one.address).status == player_status.joined
    middle_game.resolve(sender=player_one)
    assert middle_game.coinflip_status() == coinflip_status.done
    assert middle_game.get_all_players() == []
    assert middle_game.get_all_winners() == []


def test_flip(middle_game: ContractInstance, coin_side: CoinSide, player_one: AccountAPI):
    """Test flip.
    
    Middle game has three players.
    Random number mock returns fixed number equal to ten. This will always be resolved with heads winning.
    """
    txn = middle_game.resolve(sender=player_one)
    winning_side_event = txn.decode_logs(middle_game.WinningSide)[0]
    assert winning_side_event.side == coin_side.heads


def test_send_payout(middle_game: ContractInstance, coin_side: CoinSide, players: List[AccountAPI]):
    """Test send.
    
    Winning side: heads.
    Player one: heads.
    Player two: tails.
    Player three: heads.
    """
    txn = middle_game.resolve(sender=players[0])
    winner_event = txn.decode_logs(middle_game.Winner)
    payout_event = txn.decode_logs(middle_game.Payout)
    assert len(winner_event) == 2
    assert winner_event[0].side == coin_side.heads
    assert winner_event[0].winner == players[0].address
    assert winner_event[1].side == coin_side.heads
    assert winner_event[1].winner == players[2].address
    assert len(payout_event) == 2
    assert payout_event[0].player == players[0].address
    assert payout_event[0].amount == 15
    assert payout_event[1].player == players[2].address
    assert payout_event[1].amount == 15


def test_reset_game(
        resolved: ContractInstance,
        players: List[AccountAPI],
        coin_side: CoinSide,
        player_status: PlayerStatus,
        coinflip_status: CoinflipStatus
    ):
    """Test game reset."""
    assert resolved.coinflip_status() == coinflip_status.done
    assert resolved.get_all_players() == []
    assert resolved.get_all_winners() == []
    for _player in players:
        player = resolved.players(_player.address)
        assert player.status == player_status.coward
        assert player.side == coin_side.unknown


def test_force_resolve(
        middle_game: ContractInstance,
        coinflip_status: CoinflipStatus,
        owner: AccountAPI,
        player_status: PlayerStatus
    ):
    """Test forced resolve.
    
    Owner is not part of the game.
    """
    assert middle_game.players(owner.address).status == player_status.unknown
    middle_game.force_resolve(sender=owner)
    assert middle_game.coinflip_status() == coinflip_status.done
    assert middle_game.get_all_players() == []
    assert middle_game.get_all_winners() == []


def test_hacker_force_resolve(middle_game: ContractInstance, hacker: AccountAPI):
    """Hacker trying to force resolve the game."""
    with pytest.raises(ContractLogicError) as err:
        middle_game.force_resolve(sender=hacker)
    assert err.value.args[0] == "You must be owner of the contract to force resolve."
