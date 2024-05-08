package main

import (
	"context"

	pb "gitlab.com/aiops-principle-platform/onlineboutique/src/frontend/genproto"

	"gitlab.com/aiops-principle-platform/onlineboutique/src/frontend/money"
)

func cartSize(c []*pb.CartItem) int {
	cartSize := 0
	for _, item := range c {
		cartSize += int(item.GetQuantity())
	}
	return cartSize
}

func (fe *frontendServer) HomeGrpc(ctx context.Context, req *pb.HomeGrpcRequest) (*pb.HomeGrpcResponse, error) {
	log.WithField("currency", req.Currency).Info("home")

	currencies, err := fe.getCurrencies(ctx)
	if err != nil {
		resp := &pb.HomeGrpcResponse{
			Message: "currencyError",
		}
		return resp, err
	}

	products, err := fe.getProducts(ctx)
	if err != nil {
		resp := &pb.HomeGrpcResponse{
			Message: "productError",
		}
		return resp, err
	}

	cart, err := fe.getCart(ctx, req.Session)
	if err != nil {
		resp := &pb.HomeGrpcResponse{
			Message: "cartError",
		}
		return resp, err
	}
	ps := make([]*pb.ProductView, len(products))
	for i, p := range products {
		price, err := fe.convertCurrency(ctx, p.GetPriceUsd(), req.Currency)
		if err != nil {
			resp := &pb.HomeGrpcResponse{
				Message: "convertCurrencyError",
			}
			return resp, err
		}
		ps[i] = &pb.ProductView{
			Item:  p,
			Price: price,
		}
	}

	resp := &pb.HomeGrpcResponse{
		Currencies: currencies,
		Ps:         ps,
		Cart:       int32(cartSize(cart)),
	}
	return resp, nil
}

func (fe *frontendServer) ProductGrpc(ctx context.Context, req *pb.ProductGrpcRequest) (*pb.ProductGrpcResponse, error) {
	id := req.Id

	p, err := fe.getProduct(ctx, id)
	if err != nil {
		resp := &pb.ProductGrpcResponse{
			Message: "getProductError",
		}
		return resp, err
	}
	currencies, err := fe.getCurrencies(ctx)
	if err != nil {
		resp := &pb.ProductGrpcResponse{
			Message: "currencyError",
		}
		return resp, err
	}

	cart, err := fe.getCart(ctx, req.Session)
	if err != nil {
		resp := &pb.ProductGrpcResponse{
			Message: "retrieveCartError",
		}
		return resp, err
	}

	price, err := fe.convertCurrency(ctx, p.GetPriceUsd(), req.Currency)
	if err != nil {
		resp := &pb.ProductGrpcResponse{
			Message: "convertCurrencyError",
		}
		return resp, err
	}

	// ignores the error retrieving recommendations since it is not critical
	recommendations, err := fe.getRecommendations(ctx, req.Session, []string{id})
	if err != nil {
		resp := &pb.ProductGrpcResponse{
			Message: "recommendationError",
		}
		return resp, err
	}

	product := pb.ProductView{
		Item:  p,
		Price: price,
	}

	resp := &pb.ProductGrpcResponse{
		Currencies:      currencies,
		Product:         &product,
		Cart:            int32(cartSize(cart)),
		Recommendations: recommendations,
	}
	return resp, nil
}

func (fe *frontendServer) AddToCartGrpc(ctx context.Context, req *pb.AddToCartGrpcRequest) (*pb.AddToCartGrpcResponse, error) {
	quantity := req.Quantity
	productID := req.ProductId

	p, err := fe.getProduct(ctx, productID)
	if err != nil {
		resp := &pb.AddToCartGrpcResponse{
			Message: "productError",
		}
		return resp, err
	}

	if err := fe.insertCart(ctx, req.Session, p.GetId(), int32(quantity)); err != nil {
		resp := &pb.AddToCartGrpcResponse{
			Message: "addToCartError",
		}
		return resp, err
	}
	resp := &pb.AddToCartGrpcResponse{
		Message: "addToCartSuccess",
	}
	return resp, nil
}

func (fe *frontendServer) EmptyCartGrpc(ctx context.Context, req *pb.EmptyCartGrpcRequest) (*pb.EmptyCartGrpcResponse, error) {
	if err := fe.emptyCart(ctx, req.Session); err != nil {
		resp := &pb.EmptyCartGrpcResponse{
			Message: "emptyCartError",
		}
		return resp, err
	}
	resp := &pb.EmptyCartGrpcResponse{
		Message: "emptyCartSuccess",
	}
	return resp, nil
}

func cartIDs(c []*pb.CartItem) []string {
	out := make([]string, len(c))
	for i, v := range c {
		out[i] = v.GetProductId()
	}
	return out
}

func (fe *frontendServer) ViewCartGrpc(ctx context.Context, req *pb.ViewCartGrpcRequest) (*pb.ViewCartGrpcResponse, error) {
	currencies, err := fe.getCurrencies(ctx)
	if err != nil {
		resp := &pb.ViewCartGrpcResponse{
			Message: "currencyError",
		}
		return resp, err
	}
	cart, err := fe.getCart(ctx, req.Session)
	if err != nil {
		resp := &pb.ViewCartGrpcResponse{
			Message: "retrieveCartError",
		}
		return resp, err
	}

	// ignores the error retrieving recommendations since it is not critical
	recommendations, err := fe.getRecommendations(ctx, req.Session, cartIDs(cart))
	if err != nil {
		resp := &pb.ViewCartGrpcResponse{
			Message: "recommendationError",
		}
		return resp, err
	}

	shippingCost, err := fe.getShippingQuote(ctx, cart, req.Currency)
	if err != nil {
		resp := &pb.ViewCartGrpcResponse{
			Message: "getShippingError",
		}
		return resp, err
	}

	items := make([]*pb.CartItemView, len(cart))
	totalPrice := pb.Money{CurrencyCode: req.Currency}
	for i, item := range cart {
		p, err := fe.getProduct(ctx, item.GetProductId())
		if err != nil {
			resp := &pb.ViewCartGrpcResponse{
				Message:   "retrieveProductError",
				ProductId: item.GetProductId(),
			}
			return resp, err
		}
		price, err := fe.convertCurrency(ctx, p.GetPriceUsd(), req.Currency)
		if err != nil {
			resp := &pb.ViewCartGrpcResponse{
				Message:   "convertCurrencyError",
				ProductId: item.GetProductId(),
			}
			return resp, err
		}

		multPrice := money.MultiplySlow(*price, uint32(item.GetQuantity()))
		items[i] = &pb.CartItemView{
			Item:     p,
			Quantity: item.GetQuantity(),
			Price:    &multPrice}
		totalPrice = money.Must(money.Sum(totalPrice, multPrice))
	}
	totalPrice = money.Must(money.Sum(totalPrice, *shippingCost))

	resp := &pb.ViewCartGrpcResponse{
		Currencies:      currencies,
		Recommendations: recommendations,
		Cart:            int32(cartSize(cart)),
		ShippingCost:    shippingCost,
		TotalPrice:      &totalPrice,
		Items:           items,
	}
	return resp, nil
}

func (fe *frontendServer) PlaceOrderGrpc(ctx context.Context, req *pb.PlaceOrderGrpcRequest) (*pb.PlaceOrderGrpcResponse, error) {
	order, err := pb.NewCheckoutServiceClient(fe.checkoutSvcConn).
		PlaceOrder(ctx, &pb.PlaceOrderRequest{
			Email: req.Email,
			CreditCard: &pb.CreditCardInfo{
				CreditCardNumber:          req.CcNumber,
				CreditCardExpirationMonth: req.CcMonth,
				CreditCardExpirationYear:  req.CcYear,
				CreditCardCvv:             req.CcCVV},
			UserId:       req.Session,
			UserCurrency: req.Currency,
			Address: &pb.Address{
				StreetAddress: req.StreetAddress,
				City:          req.City,
				State:         req.State,
				ZipCode:       req.ZipCode,
				Country:       req.Country},
		})
	if err != nil {
		resp := &pb.PlaceOrderGrpcResponse{
			Message: "completeOrderError",
		}
		return resp, err
	}
	log.WithField("order", order.GetOrder().GetOrderId()).Info("order placed")

	order.GetOrder().GetItems()
	recommendations, _ := fe.getRecommendations(ctx, req.Session, nil)

	totalPaid := *order.GetOrder().GetShippingCost()
	for _, v := range order.GetOrder().GetItems() {
		multPrice := money.MultiplySlow(*v.GetCost(), uint32(v.GetItem().GetQuantity()))
		totalPaid = money.Must(money.Sum(totalPaid, multPrice))
	}

	currencies, err := fe.getCurrencies(ctx)
	if err != nil {
		resp := &pb.PlaceOrderGrpcResponse{
			Message: "currencyError",
		}
		return resp, err
	}

	resp := &pb.PlaceOrderGrpcResponse{
		Currencies:      currencies,
		Recommendations: recommendations,
		Order:           order.GetOrder(),
		TotalPaid:       &totalPaid,
	}
	return resp, nil
}
