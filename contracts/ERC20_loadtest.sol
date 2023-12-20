//SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.19;
import {IERC20} from "./IERC20.sol";

contract ERC20 is IERC20 {
    mapping(address account => uint256) private balances;

    mapping(address spender => mapping(address account => uint256)) private allowances;

    uint256 private total_supply;

    string private _name = "lambdacoin";
    string private _symbol = "LBDC";

    constructor(address[] memory rich_accounts) {
        for (uint i = 0; i < rich_accounts.length; i = i+1){
            balances[rich_accounts[i]] = 1000000;
        }
    }

    function name() public view virtual returns (string memory) {
        return _name;
    }

    function symbol() public view virtual returns (string memory) {
        return _symbol;
    }

    function totalSupply() public view virtual returns (uint256) {
        return total_supply;
    }

    function balanceOf(address _owner) public view returns (uint256 balance) {
        return balances[_owner];
    }

    function transfer(address _to, uint256 _value) public returns (bool success) {
        address from = msg.sender;
        require(balances[from] >= _value);
        balances[from] -= _value;
        balances[_to] += _value;
        success = true;
        emit Transfer(from, _to, _value);
    }

    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success) {
        address spender = msg.sender;
        require(allowances[spender][_from] >= _value);
        require(balances[_from] >= _value);
        allowances[spender][_from] -= _value;
        balances[_from] -= _value;
        balances[_to] += _value;
        success = true;
        emit Transfer(_from, _to, _value);
    }

    function approve(address _spender, uint256 _value) public returns (bool success) {
        allowances[_spender][msg.sender] = _value;
        success = true;
    }

    function allowance(address _owner, address _spender) public view returns (uint256 remaining) {
        return allowances[_spender][_owner];
    }
}
