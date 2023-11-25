# Coinflip

Simple coinflip game written in Vyper using Ape test framework.  

Test Coinflip deployed to: [0x5b5B86b38eEcC921fcE89276C2a59d1f5cc774D3](https://sepolia.etherscan.io/address/0x5b5B86b38eEcC921fcE89276C2a59d1f5cc774D3)

## WARNING

The contract works but I **do not** recommend using it that way. VRF functionalites are splitted into separate transactions. Please refer to this [issue](https://ethereum.stackexchange.com/questions/156700/chainlink-vrf-contract-logic-error).

Ideally VRF consumer should be a part of the Coinflip contract.

# Resources

## Faucets

### Sepolia

- LINK https://faucets.chain.link/sepolia
- ETH https://faucetlink.to/sepolia

## Docs

- Vyper https://docs.vyperlang.org/en/stable/toctree.html
- Chainlink https://docs.chain.link/
- Ape https://docs.apeworx.io/ape/stable/index.html

### Other

- https://www.vyperexamples.com/
- https://github.com/smartcontractkit/apeworx-starter-kit