// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title MultiSigApprovalDemo
/// @notice 教学用多级多签审批合约（Sepolia 测试网部署，非生产 OA 系统）
contract MultiSigApprovalDemo {
    address[] public owners;
    uint256 public required;

    mapping(bytes32 => mapping(address => bool)) public confirmations;
    mapping(bytes32 => uint256) public confirmationCount;
    mapping(bytes32 => bool) public executed;

    event Confirmation(bytes32 indexed proposalId, address indexed owner);
    event Execution(bytes32 indexed proposalId);

    error NotOwner();
    error AlreadyConfirmed();
    error InsufficientConfirmations();
    error AlreadyExecuted();

    modifier onlyOwner() {
        if (!_isOwner(msg.sender)) revert NotOwner();
        _;
    }

    constructor(address[] memory _owners, uint256 _required) {
        require(_required > 0 && _required <= _owners.length, "bad threshold");
        owners = _owners;
        required = _required;
    }

    function confirm(bytes32 proposalId) external onlyOwner {
        if (confirmations[proposalId][msg.sender]) revert AlreadyConfirmed();
        confirmations[proposalId][msg.sender] = true;
        confirmationCount[proposalId]++;
        emit Confirmation(proposalId, msg.sender);
    }

    function execute(bytes32 proposalId) external onlyOwner {
        if (executed[proposalId]) revert AlreadyExecuted();
        if (confirmationCount[proposalId] < required) revert InsufficientConfirmations();
        executed[proposalId] = true;
        emit Execution(proposalId);
    }

    function isConfirmed(bytes32 proposalId) external view returns (bool) {
        return confirmationCount[proposalId] >= required;
    }

    function _isOwner(address account) internal view returns (bool) {
        for (uint256 i = 0; i < owners.length; i++) {
            if (owners[i] == account) return true;
        }
        return false;
    }
}
