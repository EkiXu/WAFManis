package main

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

func main() {
	router := gin.Default()

	router.POST("/", func(c *gin.Context) {
		id := c.PostForm("id")
		taint := c.PostForm("taint")
		nick := c.DefaultPostForm("nick", "anonymous")

		c.JSON(http.StatusOK, gin.H{
			"status": "posted",
			"form": gin.H{
				"id":    id,
				"taint": taint,
			},
			"nick": nick,
		})
	})
	router.Run(":6000")
}
