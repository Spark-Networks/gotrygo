package healthz

import (
	"github.com/gin-gonic/gin"
)

func Status(c *gin.Context) {
	// Run Status checks and report
	content := gin.H{"status": "OK"}
	c.JSON(200, content)
}
