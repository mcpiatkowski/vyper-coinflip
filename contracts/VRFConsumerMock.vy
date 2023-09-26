# @version ^0.3.7

owner: public(address)
random_words: public(uint256[10])


@external
def __init__():
    self.owner = msg.sender


@external
def request_random_words():
    """
    @notice Returns fixed number for testing purposes.
    @dev For simple randomnes you can use: `random_number: uint256 = convert(block.prevhash, uint256)`
    """
    self.random_words[0] = 10
