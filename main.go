// main.go

package main

import (
	"fmt"
	"log"
	"os"
	"github.com/gin-gonic/gin"
	"github.com/Spark-Networks/gotrygo/healthz"
)

var version = "0.1.0"

func index(c *gin.Context) {
	hostname, _ := os.Hostname()
	content := gin.H{"application":"GoTryGo", "version": version, "host": hostname}
	c.JSON(200, content)
}

func main() {
	log.Println("Starting GoTryGo... ")
	gin.SetMode(gin.ReleaseMode)
	httpAddr = "8080"
	router := gin.Default()

	router.GET("/", index)
	router.GET("/healthz", healthz.Status)
	fmt.Printf("HTTP service listening on %s\n", httpAddr)
	router.Run(":" + httpAddr)
}
