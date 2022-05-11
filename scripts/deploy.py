from brownie import ZERO_ADDRESS, Swapper, accounts, Contract
from web3 import Web3
import json
from sys import exit

admin = accounts[0]
user = accounts[1]
WETH = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
UniswapFactory = "0x1F98431c8aD98523631AE4a59f267346ea31F984"
f = open("./FactoryAbi.json")
abi = json.load(f)


def deploySwapper():
    swapper = Swapper.deploy({"from": admin})
    return swapper


def fetchingContract(tokenAddress):
    tokenContract = Contract.from_explorer(tokenAddress)
    factoryContract = Contract.from_abi(
        "UniswapFactory", "0x1F98431c8aD98523631AE4a59f267346ea31F984", abi)
    return tokenContract, factoryContract


def fetchPool(factoryContract, tokenAddress, tokenContract):
    poolAddress = factoryContract.getPool(
        WETH, tokenAddress, 3000, {"from": user})
    if poolAddress == ZERO_ADDRESS:
        print(f"There is no pool for {tokenContract.name()} on uniswap-V3")
        exit()
    return poolAddress


def fetchPoolLiquidity(tokenContract, poolAddress):
    nTokenInPool = round(tokenContract.balanceOf(
        poolAddress) / (10**tokenContract.decimals()))
    print(
        f"There is {nTokenInPool} {tokenContract.name()} in UNI-v3 pool at {poolAddress}")


def swapToken(swapper, ethAmount, tokenAddress):
    swapper.swapETHforToken(tokenAddress, {"from": user, "value": ethAmount})


def main():
    swapper = deploySwapper()
    tokenAddress = input("Enter the address of the token you want to swap : ")
    tokenContract, factoryContract = fetchingContract(tokenAddress)
    poolAddress = fetchPool(factoryContract, tokenAddress, tokenContract)
    fetchPoolLiquidity(tokenContract, poolAddress)
    choice = input("Do you want to swap token [y/n] : ")
    if choice == 'y':
        ethIn = input("Enter how many ETH you want to swap : ")
        swapToken(swapper, Web3.toWei(ethIn, "Ether"), tokenAddress)
        print(
            f"Swap {ethIn} ETH for {tokenContract.name()} {tokenContract.balanceOf(user) / (10**tokenContract.decimals())}")
