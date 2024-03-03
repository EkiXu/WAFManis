package main

import (
	"io"
	"log"
	"net"
	"os"
	"path/filepath"
	"time"

	"github.com/BurntSushi/toml"
)

// Config holds the proxy and target server configurations
type Config struct {
	Proxy struct {
		ListenAddress string `toml:"listenAddress"`
	} `toml:"proxy"`
	Target struct {
		Address       string `toml:"address"`
		SaveDirectory string `toml:"saveDirectory"`
	} `toml:"target"`
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

	log.Printf("Listening on %s, forwarding to %s", config.Proxy.ListenAddress, config.Target.Address)

	for {
		conn, err := listener.Accept()
		if err != nil {
			log.Printf("Failed to accept connection: %v", err)
			continue
		}

		go handleConnection(conn, config)
	}
}

func handleConnection(srcConn net.Conn, config Config) {
	defer srcConn.Close()

	targetConn, err := net.Dial("tcp", config.Target.Address)
	if err != nil {
		log.Printf("Failed to connect to target %s: %v", config.Target.Address, err)
		return
	}
	defer targetConn.Close()

	// Save path for raw data
	savePath := filepath.Join(config.Target.SaveDirectory, time.Now().Format("20060102_150405")+".tcpbin")
	saveFile, err := os.Create(savePath)
	if err != nil {
		log.Printf("Failed to create save file: %v", err)
		return
	}
	defer saveFile.Close()

	// Use TeeReader to read data from srcConn and write it to saveFile simultaneously
	tee := io.TeeReader(srcConn, saveFile)

	// Copy data between src and target, saving data to file
	go io.Copy(targetConn, tee)
	io.Copy(srcConn, targetConn)
}
