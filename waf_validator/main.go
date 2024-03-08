package main

import (
	b64 "encoding/base64"
	"encoding/json"
	"log"
	"net"
	"strconv"

	"github.com/BurntSushi/toml"
)

// Config holds the proxy and target server configurations
type Config struct {
	Proxy struct {
		ListenAddress string `toml:"listenAddress"`
	} `toml:"proxy"`
}

type ResponseData struct {
	RawRequestData string `json:"req"`
}

func main() {
	// Load configuration
	var config Config
	if _, err := toml.DecodeFile("config.toml", &config); err != nil {
		log.Fatal(err)
	}

	listener, err := net.Listen("tcp", config.Proxy.ListenAddress)
	if err != nil {
		log.Fatalf("Failed to listen on %s: %v", config.Proxy.ListenAddress, err)
	}
	defer listener.Close()

	log.Printf("Listening on %s ", config.Proxy.ListenAddress)

	for {
		conn, err := listener.Accept()

		if err != nil {
			log.Printf("Failed to accept connection: %v", err)
			continue
		}

		log.Printf("Accept connection")
		go handleConnection(conn, config)
	}
}

func handleConnection(srcConn net.Conn, config Config) {
	defer srcConn.Close()

	requestData := make([]byte, 4096)

	// Copy data between src and target, saving data to file
	//for {
	// Read the incoming connection into the buffer.

	// Read data from the connection
	readLen, err := srcConn.Read(requestData)
	if err != nil {
		log.Println("Error reading response from target:", err)
		return
	}

	reqData := b64.StdEncoding.EncodeToString(requestData[:readLen])

	respData := ResponseData{
		RawRequestData: reqData,
	}

	jsonData, _ := json.Marshal(respData)

	// Send a response back to the person contacting us.
	srcConn.Write([]byte("HTTP/1.1 299 OK\r\nContent-Type: application/json\r\nContent-Length:"))
	srcConn.Write([]byte(strconv.Itoa(len(jsonData))))
	srcConn.Write([]byte("\r\n\r\n"))
	srcConn.Write(jsonData)
}
