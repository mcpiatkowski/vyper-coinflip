from ape import accounts, project

HEADS = 2
TAILS = 4


def gorilla():
    return accounts.load("gorilla")


def chimp():
    return accounts.load("chimp")


def coinflip():
    return project.Coinflip.at("0x63cBA955ADA0504e87fB6E8f3141c58E1d5f307f")


def main():
    player = gorilla()
    game = coinflip()
    print("Account Chimp")
    print(f"Balance: {player.balance}")
    print(f"Address: {player.address}")

    txn_cost = game.resolve.estimate_gas_cost(sender=player)
    print(txn_cost)

    # txn = game.join(HEADS, sender=chimp, value="0.01 ether")

    # resolve_txn = game.resolve(sender=chimp)
    #
    # print(resolve_txn.decode_logs(game.WinningSide))
    # [print(winner) for winner in resolve_txn.decode_logs(game.Winner)]


