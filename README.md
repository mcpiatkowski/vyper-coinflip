# Coinflip

Simple coinflip game written in Vyper using Ape test framework.  

Test Coinflip deployed to: [0x5b5B86b38eEcC921fcE89276C2a59d1f5cc774D3](https://sepolia.etherscan.io/address/0x5b5B86b38eEcC921fcE89276C2a59d1f5cc774D3)

## WARNING

The contract works but I **do not** recommend using it that way. VRF functionalites are splitted into separate transactions. Please refer to this [issue](https://ethereum.stackexchange.com/questions/156700/chainlink-vrf-contract-logic-error).

Ideally VRF consumer should be a part of the Coinflip contract.

Contract deployed on the above address does not reset the pot and does not assign requested random number to the internal random number. Code in the repo already contemplates both.

## Order of calls

To verify the coinflip works you can call the contract in the following order:
- start
- join
- flip
- get_random_number
- resolve

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