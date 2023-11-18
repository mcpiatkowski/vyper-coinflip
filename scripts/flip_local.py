from ape import accounts, project

HEADS = 2
TAILS = 4


def owner():
    return accounts.test_accounts[0]


def deploy(account: str):
    print(f"Account balance: {account.balance}")

    rng = account.deploy(project.VRFConsumerMock)
    contract = account.deploy(project.Coinflip, rng.address)
    return contract

    
def play(coinflip):
    player_one = accounts.test_accounts[1]
    player_two = accounts.test_accounts[2]
    player_three = accounts.test_accounts[3]

    # One gwei is 10^9 wei.
    # One eth is 10^9 gwei. 
    start_txn = coinflip.start(HEADS, sender=player_one, value="1 gwei")
    join_txn = coinflip.join(TAILS, sender=player_two, value="1 gwei")
    join_txn = coinflip.join(HEADS, sender=player_three, value="1 gwei")

    txn_cost = coinflip.resolve.estimate_gas_cost(sender=player_one)
    print(txn_cost)

    resolve_txn = coinflip.resolve(sender=player_one)

    print(start_txn.decode_logs(coinflip.Join)[0])
    [print(joined) for joined in join_txn.decode_logs(coinflip.Join)]
    print(start_txn.decode_logs(coinflip.Bet)[0])
    [print(bet) for bet in join_txn.decode_logs(coinflip.Bet)]
    print(resolve_txn.decode_logs(coinflip.WinningSide))
    [print(winner) for winner in resolve_txn.decode_logs(coinflip.Winner)]
    [print(payout) for payout in resolve_txn.decode_logs(coinflip.Payout)]


def main():
    coinflip = deploy(owner())
    play(coinflip)



