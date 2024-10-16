package main

import (
	"encoding/json"
	"fmt"
	"github.com/hyperledger/fabric-contract-api-go/contractapi"
)

// SmartContract defines the contract structure
type SmartContract struct {
	contractapi.Contract
}

// Order struct includes more product details
type Order struct {
	OrderID        string  `json:"orderId"`
	ManufacturerID string  `json:"manufacturerId"`
	ProductDetails Product `json:"productDetails"`
	Status         string  `json:"status"`
}

// Product struct holds detailed product information
type Product struct {
	Title           string   `json:"title"`
	Price           float64  `json:"price"`
	CustomerReviews []string `json:"customerReviews"`
	Sales           int      `json:"sales"`
	AdditionalInfo  string   `json:"additionalInfo"`
}

// CreateOrder function creates a new order
func (s *SmartContract) CreateOrder(ctx contractapi.TransactionContextInterface, orderId string, manufacturerId string, title string, price float64, customerReviews []string, sales int, additionalInfo string) error {
	if orderId == "" || manufacturerId == "" || title == "" {
		return fmt.Errorf("orderId, manufacturerId, and title must not be empty")
	}

	product := Product{
		Title:           title,
		Price:           price,
		CustomerReviews: customerReviews,
		Sales:           sales,
		AdditionalInfo:  additionalInfo,
	}

	order := Order{
		OrderID:        orderId,
		ManufacturerID: manufacturerId,
		ProductDetails: product,
		Status:         "Created",
	}

	orderAsBytes, err := json.Marshal(order)
	if err != nil {
		return fmt.Errorf("failed to marshal order: %w", err)
	}
	return ctx.GetStub().PutState(orderId, orderAsBytes)
}

// GetOrder function retrieves an order by ID
func (s *SmartContract) GetOrder(ctx contractapi.TransactionContextInterface, orderId string) (*Order, error) {
	orderAsBytes, err := ctx.GetStub().GetState(orderId)
	if err != nil {
		return nil, fmt.Errorf("failed to get order: %w", err)
	}
	if orderAsBytes == nil {
		return nil, fmt.Errorf("order not found")
	}

	order := new(Order)
	if err := json.Unmarshal(orderAsBytes, order); err != nil {
		return nil, fmt.Errorf("failed to unmarshal order: %w", err)
	}
	return order, nil
}

// UpdateOrderStatus function updates the status of an order
func (s *SmartContract) UpdateOrderStatus(ctx contractapi.TransactionContextInterface, orderId string, status string) error {
	order, err := s.GetOrder(ctx, orderId)
	if err != nil {
		return err
	}
	order.Status = status

	orderAsBytes, err := json.Marshal(order)
	if err != nil {
		return fmt.Errorf("failed to marshal updated order: %w", err)
	}
	return ctx.GetStub().PutState(orderId, orderAsBytes)
}

// InitLedger function can be used to initialize the ledger with sample data
func (s *SmartContract) InitLedger(ctx contractapi.TransactionContextInterface) error {
	// Sample data initialization can be done here if needed
	return nil
}

func main() {
	chaincode, err := contractapi.NewChaincode(new(SmartContract))
	if err != nil {
		fmt.Printf("Error creating supply chain chaincode: %s", err.Error())
		return
	}

	if err := chaincode.Start(); err != nil {
		fmt.Printf("Error starting supply chain chaincode: %s", err.Error())
	}
}