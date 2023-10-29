package main

import (
	"fmt"
	"log"
	"net/http"
	"time"
)

func main() {

	const songsDir = "..\\..\\music\\bathroom"
	const port = 8080
	ticker := time.NewTicker(5 * time.Second)
	quit := make(chan int)

	// test periodical functions
	go func() {
		log.Printf("goroutine started")
		for {
			select {
			case <-ticker.C:
				log.Println("function has been invoked")
			case <-quit:
				ticker.Stop()
				return
			}
		}
	}()

	http.Handle("/", addHeaders(http.FileServer(http.Dir(songsDir))))
	http.Handle("/quit", createShutDown(quit))
	fmt.Printf("Starting server on %v\n", port)
	log.Printf("Serving %s on HTTP port: %v\n", songsDir, port)

	log.Fatal(http.ListenAndServe(fmt.Sprintf(":%v", port), nil))
}

func addHeaders(h http.Handler) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Access-Control-Allow-Origin", "*")
		h.ServeHTTP(w, r)
	}
}

func createShutDown(quit chan int) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		log.Println("shuitting down")
		quit <- 0
		w.WriteHeader(http.StatusOK)
	}
}
