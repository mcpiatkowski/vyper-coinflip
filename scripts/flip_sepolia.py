from ape import accounts, project

HEADS = 2
TAILS = 4


def _gorilla():
    return accounts.load("gorilla")


def _chimp():
    return accounts.load("chimp")


def _coinflip():
    return project.Coinflip.at("0x5b5B86b38eEcC921fcE89276C2a59d1f5cc774D3")


def main():
    gorilla = _gorilla()
    chimp = _chimp()
    coinflip = _coinflip()
    print("Account Gorilla")
    print(f"Balance: {gorilla.balance}")
    print(f"Address: {gorilla.address}")

    print("Account Chimp")
    print(f"Balance: {chimp.balance}")
    print(f"Address: {chimp.address}")

    txn_start = coinflip.start(HEADS, value="0.01 ether", sender=gorilla)
    txn_join = coinflip.join(HEADS, sender=chimp, value="0.01 ether")
    txn_flip = coinflip.flip(sender=gorilla)
    txn_random_number = coinflip.get_random_number(sender=gorilla)
    txn_resolve = coinflip.resolve(sender=gorilla)

    print(txn_resolve.decode_logs(coinflip.WinningSide))
    [print(winner) for winner in txn_resolve.decode_logs(coinflip.Winner)]
