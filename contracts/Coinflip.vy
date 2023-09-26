# @version >=0.3.2

interface VRFConsumer:
    def request_random_words(): nonpayable
    def random_words(index: uint256) -> uint256: view


enum Side:
    UNKNOWN
    HEADS
    TAILS


enum PlayerStatus:
    COWARD
    JOINED


enum CoinflipStatus:
    DONE
    OPEN
    FLIPPING


event Bet:
    value: uint256
    sender: address


event Join:
    status: PlayerStatus
    sender: address


event WinningSide:
    side: Side


event Winner:
    side: Side
    winner: address
    

event Payout:
    player: address
    amount: uint256


struct Player:
    side: Side
    status: PlayerStatus


owner: public(address)
max_players: public(uint256)
vrf_consumer: public(VRFConsumer)

min_bet: public(uint256)
bet_amount: public(uint256)
pot: public(uint256)
jackpot: public(uint256)

winning_side: public(Side)
coinflip_status: public(CoinflipStatus)
players: public(HashMap[address, Player])
bag_of_players: public(DynArray[address, 20])
bag_of_winners: public(DynArray[address, 20])


@external
def __init__(vrf_consumer_address: address):
    """
    @dev For development purpose vrf functionality is mocked.
         VRF Cosumer address with subscription on Sepolia: 0x08930eaF022D25B6D8A0B4E298D7DF68063d3778
    @param vrf_consumer_address Adress of Chainlink VRF consumer contract.
    """
    self.min_bet = 1
    self.max_players = 20
    self.owner = msg.sender
    self.coinflip_status = CoinflipStatus.DONE
    self.vrf_consumer = VRFConsumer(vrf_consumer_address)


@external
def set_max_players(max_players: uint256):
    """
    @param max_players Set maximum number of players to join the game.
    @dev If arrays are fixed is it a good idea to have this function?
    """
    assert msg.sender == self.owner, "Only owner can set maximum number of players."
    self.max_players = max_players


@external
def set_min_bet(min_bet: uint256):
    """
    @dev This has to be one dollar. Conversion at current eth price is yet to be implemented.
    @param min_bet Minimum amount to start the game with.
    """
    assert msg.sender == self.owner, "Only owner can set minimal bet amount."
    self.min_bet = min_bet


@view
@external
def get_all_players() -> DynArray[address, 20]:
    """Get all players."""
    return self.bag_of_players


@view
@external
def get_all_winners() -> DynArray[address, 20]:
    """Get all winners."""
    return self.bag_of_winners


@internal
def _bet(bet_amount: uint256, player: address):
    """
    @dev There is also jackpot variable which supposed to collect some part of the bet for streak wins.
    @param bet_amount Amount for current game.
    @param player Adress of the player.
    """
    self.pot += bet_amount
    log Bet(bet_amount, player)


@internal
def _join(player: address, side: Side):
    """
    @param player Address of the player.
    @param side Side of the coin to bet on.
    """
    self.bag_of_players.append(player)
    self.players[player] = Player({side: side, status: PlayerStatus.JOINED})
    log Join(PlayerStatus.JOINED, player)


@payable
@external
def start(side: Side):
    """
    @notice Starting a game makes you automatically a participant.
    @param side Side of the coin to bet on.
    """
    assert self.coinflip_status == CoinflipStatus.DONE, "Coinflip is in progress. Try to join the game."
    assert msg.value >= self.min_bet, "Gimme moar coins! Minimal bet is 1$."
    assert len(self.bag_of_winners) == 0, "There are still some winners to be paid."
    assert len(self.bag_of_players) == 0, "There are still some players from previous game."
    self.coinflip_status = CoinflipStatus.OPEN
    self.bet_amount = msg.value
    self._join(msg.sender, side)
    self._bet(msg.value, msg.sender)


@payable
@external
def join(side: Side):
    """
    @param side Side of the coin to bet on.
    """
    player: Player = self.players[msg.sender]
    assert self.coinflip_status == CoinflipStatus.OPEN, "Please start the game first."
    assert len(self.bag_of_players) < self.max_players, "Maximum number of players reached. Wait for the next game."
    assert player.status != PlayerStatus.JOINED, "You have already joined you greedy!"
    assert msg.value == self.bet_amount, "Your bet needs to match current game bet amount."
    self._join(msg.sender, side)
    self._bet(msg.value, msg.sender)
    

@internal
def _get_random_number() -> uint256:
    """
    @dev This functionality is mocked for development purpose.
    @return Random number from Chainlink VRF.
    """
    self.vrf_consumer.request_random_words()
    return self.vrf_consumer.random_words(0)


@internal
def _flip() -> Side:
    """
    @notice Only HEADS or TAILS can win.
    @return Winning side of the coin.
    """
    if self._get_random_number() % 2 == 0:
        log WinningSide(Side.HEADS)
        return Side.HEADS
    else:
        log WinningSide(Side.TAILS)
        return Side.TAILS


@internal
def _count_winners() -> uint256:
    """
    @return Number o players who won.
    """
    for _player in self.bag_of_players:
        player: Player = self.players[_player]
        if player.side == self.winning_side:
            self.bag_of_winners.append(_player)
            log Winner(player.side, _player)
            
    return len(self.bag_of_winners)


@internal
def _payout() -> uint256:
    """
    @return Amount to pay for a single winner.
    """
    return self.pot / self._count_winners()


@internal
def _send(payout: uint256):
    """
    @param payout Amount to pay for a single player.
    """
    for winner in self.bag_of_winners:
        player: Player = self.players[winner]
        assert player.side == self.winning_side
        log Payout(winner, payout)
        send(winner, payout)


@internal
def _reset_game():
    """
    @notice After a game all statuses need to be reset.
    """
    for _player in self.bag_of_players:
        player: Player = self.players[_player]
        player.side = Side.UNKNOWN
        player.status = PlayerStatus.COWARD
        self.players[_player] = player
        
    self.bag_of_winners = []
    self.bag_of_players = []
    self.coinflip_status = CoinflipStatus.DONE


@internal
def _resolve():
    """
    @notice Close the current game and send payout.
    """
    self.coinflip_status = CoinflipStatus.FLIPPING
    self.winning_side = self._flip()
    self._send(self._payout())


@external
def resolve():
    """
    @notice Only player who joined the game can flip a coin.
    """
    player: Player = self.players[msg.sender]
    assert player.status == PlayerStatus.JOINED
    self._resolve()
    self._reset_game()


@external
def force_resolve():
    """
    @notice In case the game is stuck allow owner to force resolve the coinflip.
    """
    assert msg.sender == self.owner, "You must be owner of the contract to force resolve."
    self._resolve()
    self._reset_game()
