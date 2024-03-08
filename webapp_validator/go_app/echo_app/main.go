package main

import (
	"net/http"

	"github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"
)

func main() {
	// Echo instance
	e := echo.New()

	// Middleware
	e.Use(middleware.Logger())
	e.Use(middleware.Recover())

	// Routes
	e.POST("/", index)

	// Start server
	e.Logger.Fatal(e.Start(":6000"))
}

type Response struct {
	Form map[string]string `json:"form"`
}

// Handler
func index(c echo.Context) error {
	//values, _ := c.FormParams()

	form := make(map[string]string, 0)

	form["taint"] = c.FormValue("taint")
	form["id"] = c.FormValue("id")

	return c.JSON(http.StatusOK, Response{
		Form: form,
	})
}
