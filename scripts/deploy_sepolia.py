from ape import accounts, project


def deploy():
    """Deploy Coinflip on Sepolia.
    
    Chainlink VRF consumer tied to a subscription: 0x08930eaF022D25B6D8A0B4E298D7DF68063d3778.
    """
    account = accounts.load("gorilla")
    account.deploy(project.Coinflip, "0x08930eaF022D25B6D8A0B4E298D7DF68063d3778")


def main():
    """Main function to call."""
    deploy()
