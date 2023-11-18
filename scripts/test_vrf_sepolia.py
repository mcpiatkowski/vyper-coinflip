from ape import accounts, project


def gorilla():
    return accounts.load("gorilla")


def coinflip():
    return project.Coinflip.at("0x63cBA955ADA0504e87fB6E8f3141c58E1d5f307f")


def main():
    player = gorilla()
    vrf = project.VRFConsumerV2.at("0x08930eaF022D25B6D8A0B4E298D7DF68063d3778")
    vrf.request_random_words(sender=player)

    random_words = vrf.random_words(0)
    print(random_words)
