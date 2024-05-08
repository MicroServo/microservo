// Copyright 2018 Google LLC
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

package main

import (
	"context"
	"fmt"
	"html/template"
	"math/rand"
	"net/http"
	"os"
	"strconv"
	"strings"
	"time"

	"github.com/gorilla/mux"
	"github.com/pkg/errors"
	"github.com/sirupsen/logrus"

	pb "gitlab.com/aiops-principle-platform/onlineboutique/src/frontend/genproto"
)

type platformDetails struct {
	css      string
	provider string
}

var (
	isCymbalBrand = "true" == strings.ToLower(os.Getenv("CYMBAL_BRANDING"))
	templates     = template.Must(template.New("").
			Funcs(template.FuncMap{
			"renderMoney":        renderMoney,
			"renderCurrencyLogo": renderCurrencyLogo,
		}).ParseGlob("templates/*.html"))
	plat platformDetails
)

var validEnvs = []string{"local", "gcp", "azure", "aws", "onprem", "alibaba"}

func (fe *frontendServer) homeHandler(w http.ResponseWriter, r *http.Request) {
	log := r.Context().Value(ctxKeyLog{}).(logrus.FieldLogger)
	resp, err := pb.NewFrontendServiceClient(fe.frontendSvcConn).
		HomeGrpc(r.Context(), &pb.HomeGrpcRequest{
			Currency: currentCurrency(r),
			Session:  sessionID(r),
		})
	if resp.Message == "currencyError" {
		renderHTTPError(log, r, w, errors.Wrap(err, "could not retrieve currencies"), http.StatusInternalServerError)
		return
	}

	if resp.Message == "productError" {
		renderHTTPError(log, r, w, errors.Wrap(err, "could not retrieve products"), http.StatusInternalServerError)
		return
	}

	if resp.Message == "cartError" {
		renderHTTPError(log, r, w, errors.Wrap(err, "could not retrieve cart"), http.StatusInternalServerError)
		return
	}

	if resp.Message == "convertCurrencyError" {
		renderHTTPError(log, r, w, errors.Wrapf(err, "failed to do currency conversion for product"), http.StatusInternalServerError)
		return
	}

	// Set ENV_PLATFORM (default to local if not set; use env var if set; otherwise detect GCP, which overrides env)_
	var env = os.Getenv("ENV_PLATFORM")
	// Only override from env variable if set + valid env
	if env == "" || stringinSlice(validEnvs, env) == false {
		fmt.Println("env platform is either empty or invalid")
		env = "local"
	}

	log.Debugf("ENV_PLATFORM is: %s", env)
	plat = platformDetails{}
	plat.setPlatformDetails(strings.ToLower(env))

	if err := templates.ExecuteTemplate(w, "home", map[string]interface{}{
		"session_id":        sessionID(r),
		"request_id":        r.Context().Value(ctxKeyRequestID{}),
		"user_currency":     currentCurrency(r),
		"show_currency":     true,
		"currencies":        resp.Currencies,
		"products":          resp.Ps,
		"cart_size":         resp.Cart,
		"banner_color":      os.Getenv("BANNER_COLOR"), // illustrates canary deployments
		"ad":                fe.chooseAd(r.Context(), []string{}, log),
		"platform_css":      plat.css,
		"platform_name":     plat.provider,
		"is_cymbal_brand":   isCymbalBrand,
		"deploymentDetails": deploymentDetailsMap,
	}); err != nil {
		log.Error(err)
	}
}

func (plat *platformDetails) setPlatformDetails(env string) {
	if env == "aws" {
		plat.provider = "AWS"
		plat.css = "aws-platform"
	} else if env == "onprem" {
		plat.provider = "On-Premises"
		plat.css = "onprem-platform"
	} else if env == "azure" {
		plat.provider = "Azure"
		plat.css = "azure-platform"
	} else if env == "gcp" {
		plat.provider = "Google Cloud"
		plat.css = "gcp-platform"
	} else if env == "alibaba" {
		plat.provider = "Alibaba Cloud"
		plat.css = "alibaba-platform"
	} else {
		plat.provider = "local"
		plat.css = "local"
	}
}

func (fe *frontendServer) productHandler(w http.ResponseWriter, r *http.Request) {
	log := r.Context().Value(ctxKeyLog{}).(logrus.FieldLogger)
	id := mux.Vars(r)["id"]
	if id == "" {
		renderHTTPError(log, r, w, errors.New("product id not specified"), http.StatusBadRequest)
		return
	}
	log.WithField("id", id).WithField("currency", currentCurrency(r)).
		Debug("serving product page")

	resp, err := pb.NewFrontendServiceClient(fe.frontendSvcConn).
		ProductGrpc(r.Context(), &pb.ProductGrpcRequest{
			Currency: currentCurrency(r),
			Session:  sessionID(r),
			Id:       id,
		})
	if resp.Message == "getProductError" {
		renderHTTPError(log, r, w, errors.Wrap(err, "could not retrieve product"), http.StatusInternalServerError)
		return
	}
	if resp.Message == "currencyError" {
		renderHTTPError(log, r, w, errors.Wrap(err, "could not retrieve currencies"), http.StatusInternalServerError)
		return
	}
	if resp.Message == "retrieveCartError" {
		renderHTTPError(log, r, w, errors.Wrap(err, "could not retrieve cart"), http.StatusInternalServerError)
		return
	}
	if resp.Message == "convertCurrencyError" {
		renderHTTPError(log, r, w, errors.Wrap(err, "failed to convert currency"), http.StatusInternalServerError)
		return
	}
	if resp.Message == "recommendationError" {
		log.WithField("error", err).Warn("failed to get product recommendations")
	}

	if err := templates.ExecuteTemplate(w, "product", map[string]interface{}{
		"session_id":        sessionID(r),
		"request_id":        r.Context().Value(ctxKeyRequestID{}),
		"ad":                fe.chooseAd(r.Context(), []string{}, log),
		"user_currency":     currentCurrency(r),
		"show_currency":     true,
		"currencies":        resp.Currencies,
		"product":           resp.Product,
		"recommendations":   resp.Recommendations,
		"cart_size":         resp.Cart,
		"platform_css":      plat.css,
		"platform_name":     plat.provider,
		"is_cymbal_brand":   isCymbalBrand,
		"deploymentDetails": deploymentDetailsMap,
	}); err != nil {
		log.Println(err)
	}
}

func (fe *frontendServer) addToCartHandler(w http.ResponseWriter, r *http.Request) {
	log := r.Context().Value(ctxKeyLog{}).(logrus.FieldLogger)
	quantity, _ := strconv.ParseUint(r.FormValue("quantity"), 10, 32)
	productID := r.FormValue("product_id")
	if productID == "" || quantity == 0 {
		renderHTTPError(log, r, w, errors.New("invalid form input"), http.StatusBadRequest)
		return
	}
	log.WithField("product", productID).WithField("quantity", quantity).Debug("adding to cart")
	resp, err := pb.NewFrontendServiceClient(fe.frontendSvcConn).
		AddToCartGrpc(r.Context(), &pb.AddToCartGrpcRequest{
			Session:   sessionID(r),
			Quantity:  int32(quantity),
			ProductId: productID,
		})
	if resp.Message == "productError" {
		renderHTTPError(log, r, w, errors.Wrap(err, "could not retrieve product"), http.StatusInternalServerError)
		return
	}

	if resp.Message == "addToCartError" {
		renderHTTPError(log, r, w, errors.Wrap(err, "failed to add to cart"), http.StatusInternalServerError)
		return
	}
	w.Header().Set("location", "/cart")
	w.WriteHeader(http.StatusFound)
}

func (fe *frontendServer) emptyCartHandler(w http.ResponseWriter, r *http.Request) {
	log := r.Context().Value(ctxKeyLog{}).(logrus.FieldLogger)
	log.Debug("emptying cart")

	resp, err := pb.NewFrontendServiceClient(fe.frontendSvcConn).
		EmptyCartGrpc(r.Context(), &pb.EmptyCartGrpcRequest{
			Session: sessionID(r),
		})
	if resp.Message == "emptyCartError" {
		renderHTTPError(log, r, w, errors.Wrap(err, "failed to empty cart"), http.StatusInternalServerError)
		return
	}
	w.Header().Set("location", "/")
	w.WriteHeader(http.StatusFound)
}

func (fe *frontendServer) viewCartHandler(w http.ResponseWriter, r *http.Request) {
	log := r.Context().Value(ctxKeyLog{}).(logrus.FieldLogger)
	log.Debug("view user cart")
	resp, err := pb.NewFrontendServiceClient(fe.frontendSvcConn).
		ViewCartGrpc(r.Context(), &pb.ViewCartGrpcRequest{
			Session:  sessionID(r),
			Currency: currentCurrency(r),
		})
	if resp.Message == "currencyError" {
		renderHTTPError(log, r, w, errors.Wrap(err, "could not retrieve currencies"), http.StatusInternalServerError)
		return
	}
	if resp.Message == "retrieveCartError" {
		renderHTTPError(log, r, w, errors.Wrap(err, "could not retrieve cart"), http.StatusInternalServerError)
		return
	}
	if resp.Message == "recommendationError" {
		log.WithField("error", err).Warn("failed to get product recommendations")
	}
	if resp.Message == "getShippingError" {
		renderHTTPError(log, r, w, errors.Wrap(err, "failed to get shipping quote"), http.StatusInternalServerError)
		return
	}
	if resp.Message == "retrieveProductError" {
		renderHTTPError(log, r, w, errors.Wrapf(err, "could not retrieve product #%s", resp.ProductId), http.StatusInternalServerError)
		return
	}
	if resp.Message == "convertCurrencyError" {
		renderHTTPError(log, r, w, errors.Wrapf(err, "could not convert currency for product #%s", resp.ProductId), http.StatusInternalServerError)
		return
	}
	year := time.Now().Year()

	if err := templates.ExecuteTemplate(w, "cart", map[string]interface{}{
		"session_id":        sessionID(r),
		"request_id":        r.Context().Value(ctxKeyRequestID{}),
		"user_currency":     currentCurrency(r),
		"currencies":        resp.Currencies,
		"recommendations":   resp.Recommendations,
		"cart_size":         resp.Cart,
		"shipping_cost":     resp.ShippingCost,
		"show_currency":     true,
		"total_cost":        resp.TotalPrice,
		"items":             resp.Items,
		"expiration_years":  []int{year, year + 1, year + 2, year + 3, year + 4},
		"platform_css":      plat.css,
		"platform_name":     plat.provider,
		"is_cymbal_brand":   isCymbalBrand,
		"deploymentDetails": deploymentDetailsMap,
	}); err != nil {
		log.Println(err)
	}
}

func (fe *frontendServer) placeOrderHandler(w http.ResponseWriter, r *http.Request) {
	log := r.Context().Value(ctxKeyLog{}).(logrus.FieldLogger)
	log.Debug("placing order")

	var (
		email         = r.FormValue("email")
		streetAddress = r.FormValue("street_address")
		zipCode, _    = strconv.ParseInt(r.FormValue("zip_code"), 10, 32)
		city          = r.FormValue("city")
		state         = r.FormValue("state")
		country       = r.FormValue("country")
		ccNumber      = r.FormValue("credit_card_number")
		ccMonth, _    = strconv.ParseInt(r.FormValue("credit_card_expiration_month"), 10, 32)
		ccYear, _     = strconv.ParseInt(r.FormValue("credit_card_expiration_year"), 10, 32)
		ccCVV, _      = strconv.ParseInt(r.FormValue("credit_card_cvv"), 10, 32)
	)

	resp, err := pb.NewFrontendServiceClient(fe.frontendSvcConn).
		PlaceOrderGrpc(r.Context(), &pb.PlaceOrderGrpcRequest{
			Session:       sessionID(r),
			Currency:      currentCurrency(r),
			Email:         email,
			StreetAddress: streetAddress,
			ZipCode:       int32(zipCode),
			City:          city,
			State:         state,
			Country:       country,
			CcNumber:      ccNumber,
			CcMonth:       int32(ccMonth),
			CcYear:        int32(ccYear),
			CcCVV:         int32(ccCVV),
		})
	if resp.Message == "completeOrderError" {
		renderHTTPError(log, r, w, errors.Wrap(err, "failed to complete the order"), http.StatusInternalServerError)
		return
	}
	if resp.Message == "currencyError" {
		renderHTTPError(log, r, w, errors.Wrap(err, "could not retrieve currencies"), http.StatusInternalServerError)
		return
	}

	if err := templates.ExecuteTemplate(w, "order", map[string]interface{}{
		"session_id":        sessionID(r),
		"request_id":        r.Context().Value(ctxKeyRequestID{}),
		"user_currency":     currentCurrency(r),
		"show_currency":     false,
		"currencies":        resp.Currencies,
		"order":             resp.Order,
		"total_paid":        resp.TotalPaid,
		"recommendations":   resp.Recommendations,
		"platform_css":      plat.css,
		"platform_name":     plat.provider,
		"is_cymbal_brand":   isCymbalBrand,
		"deploymentDetails": deploymentDetailsMap,
	}); err != nil {
		log.Println(err)
	}
}

func (fe *frontendServer) logoutHandler(w http.ResponseWriter, r *http.Request) {
	log := r.Context().Value(ctxKeyLog{}).(logrus.FieldLogger)
	log.Debug("logging out")
	for _, c := range r.Cookies() {
		c.Expires = time.Now().Add(-time.Hour * 24 * 365)
		c.MaxAge = -1
		http.SetCookie(w, c)
	}
	w.Header().Set("Location", "/")
	w.WriteHeader(http.StatusFound)
}

func (fe *frontendServer) setCurrencyHandler(w http.ResponseWriter, r *http.Request) {
	log := r.Context().Value(ctxKeyLog{}).(logrus.FieldLogger)
	cur := r.FormValue("currency_code")
	log.WithField("curr.new", cur).WithField("curr.old", currentCurrency(r)).
		Debug("setting currency")

	if cur != "" {
		http.SetCookie(w, &http.Cookie{
			Name:   cookieCurrency,
			Value:  cur,
			MaxAge: cookieMaxAge,
		})
	}
	referer := r.Header.Get("referer")
	if referer == "" {
		referer = "/"
	}
	w.Header().Set("Location", referer)
	w.WriteHeader(http.StatusFound)
}

// chooseAd queries for advertisements available and randomly chooses one, if
// available. It ignores the error retrieving the ad since it is not critical.
func (fe *frontendServer) chooseAd(ctx context.Context, ctxKeys []string, log logrus.FieldLogger) *pb.Ad {
	ads, err := fe.getAd(ctx, ctxKeys)
	if err != nil {
		log.WithField("error", err).Warn("failed to retrieve ads")
		return nil
	}
	return ads[rand.Intn(len(ads))]
}

func renderHTTPError(log logrus.FieldLogger, r *http.Request, w http.ResponseWriter, err error, code int) {
	log.WithField("error", err).Error("request error")
	errMsg := fmt.Sprintf("%+v", err)

	w.WriteHeader(code)

	if templateErr := templates.ExecuteTemplate(w, "error", map[string]interface{}{
		"session_id":        sessionID(r),
		"request_id":        r.Context().Value(ctxKeyRequestID{}),
		"error":             errMsg,
		"status_code":       code,
		"status":            http.StatusText(code),
		"is_cymbal_brand":   isCymbalBrand,
		"deploymentDetails": deploymentDetailsMap,
	}); templateErr != nil {
		log.Println(templateErr)
	}
}

func currentCurrency(r *http.Request) string {
	c, _ := r.Cookie(cookieCurrency)
	if c != nil {
		return c.Value
	}
	return defaultCurrency
}

func sessionID(r *http.Request) string {
	v := r.Context().Value(ctxKeySessionID{})
	if v != nil {
		return v.(string)
	}
	return ""
}

func renderMoney(money pb.Money) string {
	currencyLogo := renderCurrencyLogo(money.GetCurrencyCode())
	return fmt.Sprintf("%s%d.%02d", currencyLogo, money.GetUnits(), money.GetNanos()/10000000)
}

func renderCurrencyLogo(currencyCode string) string {
	logos := map[string]string{
		"USD": "$",
		"CAD": "$",
		"JPY": "¥",
		"EUR": "€",
		"TRY": "₺",
		"GBP": "£",
	}

	logo := "$" //default
	if val, ok := logos[currencyCode]; ok {
		logo = val
	}
	return logo
}

func stringinSlice(slice []string, val string) bool {
	for _, item := range slice {
		if item == val {
			return true
		}
	}
	return false
}
