package main

import (
	"fmt"
	"log"
	"net/http"
	"path/filepath"
	"time"
)

func main() {

	dirBathroom := filepath.Join("..", "..", "music")
	dirJazz := filepath.Join("..", "..", "music", "jazz")
	const port = 8080
	ticker := time.NewTicker(5 * time.Second)
	quit := make(chan int)

	// test periodical functions
	go func() {
		log.Printf("goroutine started")
		i := 0
		for {
			select {
			case <-ticker.C:
				i = i + 1
				log.Printf("function has been invoked x%d\n", i)
			case <-quit:
				ticker.Stop()
				return
			}
		}
	}()

	http.Handle("/", addHeaders(http.FileServer(http.Dir(dirBathroom))))
	http.Handle("/quit", createShutDown(quit))
	fmt.Printf("Starting server on %v\n", port)
	log.Printf("Serving %s, %s on HTTP port: %v\n", dirBathroom, dirJazz, port)

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
