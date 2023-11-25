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
    coinflip = _coinflip()
    print("Account Gorilla")
    print(f"Balance: {gorilla.balance}")
    print(f"Address: {gorilla.address}")

    bag_of_players = coinflip.get_all_players(sender=gorilla)
    bag_of_winners = coinflip.get_all_winners(sender=gorilla)
    print(f"Bag of players: {bag_of_players}")
    print(f"Bag of winners: {bag_of_winners}")

    random_number = coinflip.random_number(sender=gorilla)
    coinflip_status = coinflip.coinflip_status(sender=gorilla)
    pot = coinflip.pot(sender=gorilla)
    print(f"Random number: {random_number}")
    print(f"Coinflip status: {coinflip_status}")
    print(f"Pot: {pot}")
