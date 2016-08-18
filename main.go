// main.go

package main

import (
	"fmt"
	"log"
	"os"
	"time"
	"github.com/gin-gonic/gin"
	"github.com/Spark-Networks/gotrygo/healthz"
)

var version = "v0.1.0"

func index(c *gin.Context) {
	hostname, _ := os.Hostname()
	t := time.Now().UTC()
	content := gin.H{"application":"GoTryGo", "version": version, "host": hostname, "current_time": t.Format("Monday, 02-Jan-06 15:04:05 MST")}
	c.JSON(200, content)
}

func main() {
	log.Println("Starting GoTryGo... ")
	gin.SetMode(gin.ReleaseMode)
	httpAddr := "8080"
	router := gin.Default()

	router.GET("/", index)
	router.GET("/healthz", healthz.Status)
	fmt.Printf("HTTP service listening on %s\n", httpAddr)
	router.Run(":" + httpAddr)
}
