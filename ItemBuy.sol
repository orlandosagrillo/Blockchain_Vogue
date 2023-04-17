pragma solidity ^0.5.0;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC721/ERC721Full.sol";

contract ShopRegistry is ERC721Full {
    constructor() public ERC721Full("ShopRegistryToken", "VOGUE") {}

    struct Item {
        string name;
        string brand;
        uint256 itemAmount;
        string vogueJson;
}

    mapping(uint256 => Item) public vogueCollection;

    event Buy(uint256 tokenId, uint256 itemAmount, string reportURI, string vogueJson);
    
    function imageUri(
        uint256 tokenId

    ) public view returns (string memory imageJson){
        return vogueCollection[tokenId].vogueJson;
    }


    function buyItem(
        address owner,
        string memory name,
        string memory brand,
        uint256 itemCost,
        string memory tokenURI,
        string memory tokenJSON
    ) public returns (uint256) {
        uint256 tokenId = totalStock();

        _mint(owner, tokenId);
        _setTokenURI(tokenId, tokenURI);

        vogueCollection[tokenId] = Item(name, brand, itemCost, tokenJSON);

        return tokenId;
    } 
}
