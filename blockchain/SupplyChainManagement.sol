// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SupplyChain {

    struct Product {
        uint sku;
        string name;
        string description;
        string productType;
        uint price;
        address owner;
        string location;
        bool isSold;
        uint revenueGenerated;
        string shippingCarrier;
        string customerDemographics;
        Review[] reviews;
        Transaction[] transactions;
    }
    
    struct Review {
        address customer;
        string feedback;
        uint8 rating; // Rating out of 5
    }
    
    struct Transaction {
        address from;
        address to;
        uint timestamp;
        string details;
    }
    
    mapping(uint => Product) public products;
    uint public productCount = 0;
    
    event ProductAdded(uint sku, string name, string description, string productType, address owner, string location, uint price);
    event OwnershipTransferred(uint sku, address previousOwner, address newOwner, string newLocation);
    event RevenueGenerated(uint sku, uint revenue);
    event ProductSold(uint sku, address buyer);
    event ReviewAdded(uint sku, address customer, uint8 rating, string feedback);
    event TransactionLogged(uint sku, address from, address to, string details);

    // Add a new product to the supply chain
    function addProduct(string memory name, string memory description, string memory productType, uint price, string memory location, string memory shippingCarrier, string memory customerDemographics) public {
        productCount++;
        Product storage newProduct = products[productCount];
        newProduct.sku = productCount;
        newProduct.name = name;
        newProduct.description = description;
        newProduct.productType = productType;
        newProduct.price = price;
        newProduct.owner = msg.sender;
        newProduct.location = location;
        newProduct.isSold = False;
        newProduct.revenueGenerated = 0;
        newProduct.shippingCarrier = shippingCarrier;
        newProduct.customerDemographics = customerDemographics;
        emit ProductAdded(productCount, name, description, productType, msg.sender, location, price);
    }
    
    // Transfer ownership of a product
    function transferOwnership(uint sku, address newOwner, string memory newLocation) public {
        Product storage product = products[sku];
        require(msg.sender == product.owner, "Only current owner can transfer ownership.");
        require(!product.isSold, "Product is already sold.");
        
        // Log transaction
        product.transactions.push(Transaction(msg.sender, newOwner, block.timestamp, "Ownership Transfer"));
        
        emit OwnershipTransferred(sku, product.owner, newOwner, newLocation);
        product.owner = newOwner;
        product.location = newLocation;
        emit TransactionLogged(sku, msg.sender, newOwner, "Ownership Transfer");
    }
    
    // Log revenue for a product
    function logRevenue(uint sku, uint revenue) public {
        Product storage product = products[sku];
        require(msg.sender == product.owner, "Only owner can log revenue.");
        
        product.revenueGenerated += revenue;
        emit RevenueGenerated(sku, revenue);
    }

    // Mark product as sold and log revenue
    function markAsSold(uint sku, uint revenue) public {
        Product storage product = products[sku];
        require(msg.sender == product.owner, "Only owner can mark as sold.");
        require(!product.isSold, "Product is already sold.");
        
        product.isSold = true;
        product.revenueGenerated += revenue;
        emit ProductSold(sku, msg.sender);
    }

    // Add a product review by a customer
    function addReview(uint sku, string memory feedback, uint8 rating) public {
        require(rating >= 1 && rating <= 5, "Rating should be between 1 and 5.");
        
        Product storage product = products[sku];
        product.reviews.push(Review(msg.sender, feedback, rating));
        emit ReviewAdded(sku, msg.sender, rating, feedback);
    }

    // Retrieve product details, including reviews and transactions
    function getProductDetails(uint sku) public view returns (
        string memory name, 
        string memory description, 
        address owner, 
        bool isSold, 
        uint revenueGenerated, 
        string memory location,
        uint reviewCount,
        uint transactionCount
    ) {
        Product memory product = products[sku];
        return (
            product.name, 
            product.description, 
            product.owner, 
            product.isSold, 
            product.revenueGenerated, 
            product.location,
            product.reviews.length,
            product.transactions.length
        );
    }

    // Retrieve reviews for a specific product
    function getProductReviews(uint sku) public view returns (Review[] memory) {
        return products[sku].reviews;
    }

    // Retrieve transaction history for a specific product
    function getTransactionHistory(uint sku) public view returns (Transaction[] memory) {
        return products[sku].transactions;
    }
}
