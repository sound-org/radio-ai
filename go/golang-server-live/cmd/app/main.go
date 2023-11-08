package main

import (
	"fmt"
	"log"
	"net/http"
	"os"
	"path/filepath"
	"sync"
	"time"

	channel "github.com/sound-org/radio-ai/server/internal/cache"
)

func main() {

	// TODO : params of how long to waint between changes and how many records to change per tick
	dir := filepath.Join("..", "..", "music")
	streamingFilePath := filepath.Join(dir, "stream.m3u8")
	mutex := sync.RWMutex{}

	manager, err := channel.CreateManager(dir, streamingFilePath, &mutex)
	if err != nil {
		log.Println(err)
		return
	}

	const port = 8080
	ticker := time.NewTicker(5 * time.Second)
	quit := make(chan int)

	go runStreaming(manager, ticker, &quit)

	http.Handle("/", addHeaders(http.FileServer(http.Dir(dir))))
	http.Handle("/channel1", addHeaders(readStreamming(manager)))
	http.Handle("/quit", createShutDown(quit))
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

func createShutDown(quit chan int) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		log.Println("shuitting down")
		quit <- 0
		w.WriteHeader(http.StatusOK)
	}
}

func runStreaming(manager *channel.Manager, ticker *time.Ticker, quit *chan int) {
	err := manager.InitWriteRecord(filepath.Join("..", "..", "music", "bathroom", "outputlist.m3u8"), 5)
	if err != nil {
		log.Println(err)
		ticker.Stop()
		return
	}

	printCurrentWritePlaylist(manager)

	log.Println("Started saving...")
	manager.Save()
	log.Println("... done!")

	index := 0
	mIndex := 0
	musics := []string{filepath.Join("..", "..", "music", "bathroom", "outputlist.m3u8"), filepath.Join("..", "..", "music", "jazz", "outputlist.m3u8")}
	for {
		select {
		case <-ticker.C:
			update, err := manager.UpdateWriteRecord(musics[mIndex], 1, index)
			if err != nil {
				log.Print(err)
				ticker.Stop()
				return
			}
			index = (index + 1) % len(manager.ReadRecords[musics[mIndex]].Ts)
			if update {
				mIndex = (mIndex + 1) % 2
			}
			log.Printf("Updated (index: %v, music: %s)\n", index, musics[mIndex])
			//printCurrentWritePlaylist(manager)
			log.Println("Started saving...")
			manager.Save()
			log.Println("... done!")
		case <-*quit:
			ticker.Stop()
			manager.StreamingFile.Close()
			os.Remove(manager.StreamingFile.Name())
			return
		}
	}
}

func printCurrentWritePlaylist(man *channel.Manager) {
	err := man.WriteRecord.SaveToFile(os.Stdout, ".")
	if err != nil {
		log.Println(err)
	}
}

func readStreamming(manager *channel.Manager) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		log.Println("READ")
		manager.Mutex.RLock()
		manager.WriteRecord.Save(w)
		manager.Mutex.RUnlock()
		log.Println("DONE")
	}
}
