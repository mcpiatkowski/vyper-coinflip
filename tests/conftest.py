import pytest

from typing import List
from contract_typing import CoinSide, PlayerStatus, CoinflipStatus

from ape import accounts
from ape.managers.project.manager import ProjectManager
from ape.contracts.base import ContractInstance
from ape.api import AccountAPI


@pytest.fixture
def coin_side() -> CoinSide:
    """Numeric representation of the coin side."""
    return CoinSide(unknown=1, heads=2, tails=4)


@pytest.fixture
def player_status() -> PlayerStatus:
    """Numeric representation of the player status."""
    return PlayerStatus(unknown=0, coward=1, joined=2)


@pytest.fixture
def coinflip_status() -> CoinflipStatus:
    """Numeric representation of the game status."""
    return CoinflipStatus(done=1, open=2, flipping=4)


@pytest.fixture
def owner() -> AccountAPI:
    """Owner/deployer of the contract."""
    return accounts.test_accounts[0]


@pytest.fixture
def hacker() -> AccountAPI:
    """Contract hacker."""
    return accounts.test_accounts[9]


@pytest.fixture
def player_one() -> AccountAPI:
    "Player number one."
    return accounts.test_accounts[1]


@pytest.fixture
def player_two() -> AccountAPI:
    "Player number two."
    return accounts.test_accounts[2]


@pytest.fixture
def player_three() -> AccountAPI:
    "Player number three."
    return accounts.test_accounts[3]


@pytest.fixture
def players(player_one, player_two, player_three) -> List[AccountAPI]:
    """Players to join the game."""
    return [
        player_one,
        player_two,
        player_three
    ]


@pytest.fixture
def rng(project: ProjectManager, owner: AccountAPI) -> ContractInstance:
    """Mocked random number generator."""
    return owner.deploy(project.VRFConsumerMock)


@pytest.fixture
def coinflip(project: ProjectManager, owner: AccountAPI, rng: ContractInstance) -> ContractInstance:
    """Coinflip contract instance."""
    return owner.deploy(project.Coinflip, rng.address)


@pytest.fixture
def middle_game(coinflip: ContractInstance, coin_side: CoinSide, players: List[AccountAPI]):
    """Coinflip contract with game opened."""
    coinflip.start(coin_side.heads, sender=players[0], value=10)
    coinflip.join(coin_side.tails, sender=players[1], value=10)
    coinflip.join(coin_side.heads, sender=players[2], value=10)
    return coinflip


@pytest.fixture
def resolved(middle_game: ContractInstance, player_one: AccountAPI):
    """Resolved coinflip contract."""
    middle_game.resolve(sender=player_one)
    return middle_game
