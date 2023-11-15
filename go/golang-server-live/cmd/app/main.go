package main

import (
	"fmt"
	"log"
	"net/http"
	"path/filepath"

	"github.com/sound-org/radio-ai/server/internal/channel"
	"github.com/sound-org/radio-ai/server/internal/config"
)

func main() {

	dir := filepath.Join("..", "..", "music")

	channel1 := channel.CreateChannel(dir)
	cnf, err := config.Load(filepath.Join("..", "..", "..", "..", "radio_config.json"))
	if err != nil {
		panic(err)
	}

	log.Println(cnf)

	const port = 8080
	quit := make(chan bool)

	go channel.Run(channel1, &quit)

	http.Handle("/", addHeaders(http.FileServer(http.Dir(dir))))
	http.Handle("/channel1", addHeaders(readStreamming(channel1)))
	http.Handle("/quit", createShutDown(quit))
	http.Handle("/info", config.InfoHandler(cnf))
	fmt.Printf("Starting server on %v\n", port)
	log.Printf("Serving  music : '%s' on HTTP port: %v\n", dir, port)

	log.Fatal(http.ListenAndServe(fmt.Sprintf(":%v", port), nil))
}

func addHeaders(h http.Handler) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Access-Control-Allow-Origin", "*")
		h.ServeHTTP(w, r)
	}
}

func createShutDown(quit chan bool) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		log.Println("shuitting down")
		quit <- true
		w.WriteHeader(http.StatusOK)
	}
}

func readStreamming(channel *channel.Channel) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		hls := channel.Stream()
		hls.Save(w)
	}
}
