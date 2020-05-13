pragma solidity ^0.6.2;

import "./ERC20Interface.sol";


// ----------------------------------------------------------------------------
// Token Interface = ERC20 + symbol + name + decimals 
// ----------------------------------------------------------------------------
interface TokenInterface is ERC20Interface {
    function symbol() external view returns (string memory);
    function name() external view returns (string memory);
    function decimals() external view returns (uint8);
}
