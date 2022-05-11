// SPDX-License-Identifier: MIT
pragma solidity =0.8.13;
pragma abicoder v2;

import "../interfaces/ISwapRouter.sol";

contract Swapper {
    ISwapRouter public constant swapRouter =
        ISwapRouter(0xE592427A0AEce92De3Edee1F18E0157C05861564);

    address private constant WETH9 = 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2;
    address private constant USDC = 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48;

    error Error_ValueMustBeNonZero();

    ///@notice swap native ETH for a token
    function swapETHforToken(address _token) external payable {
        if (msg.value == 0) {
            revert Error_ValueMustBeNonZero();
        }

        uint256 deadline = block.timestamp + 15;
        address tokenIn = WETH9;
        address tokenOut = _token;
        uint24 fee = 3000;
        address recipient = msg.sender;
        uint256 amountIn = msg.value;
        uint256 amountOutMinimum = 1;
        uint160 sqrtPriceLimitX96 = 0;

        ISwapRouter.ExactInputSingleParams memory params = ISwapRouter
            .ExactInputSingleParams(
                tokenIn,
                tokenOut,
                fee,
                recipient,
                deadline,
                amountIn,
                amountOutMinimum,
                sqrtPriceLimitX96
            );

        swapRouter.exactInputSingle{value: msg.value}(params);
    }
}
