build:
	CGO_ENABLED=0 GOOS=linux go build -v -a -installsuffix cgo -o gotrygo .
