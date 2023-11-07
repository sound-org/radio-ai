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

	// TODO : there are still race conditions taht need to be fix
	// TODO : params of how long to waint between changes and how many records to change per tick
	dir := filepath.Join("..", "..", "music")
	streamingFilePath := filepath.Join(dir, "stream.m3u8")

	const port = 8080
	mutex := sync.RWMutex{}
	ticker := time.NewTicker(5 * time.Second)
	quit := make(chan int)

	go runStreaming(&mutex, ticker, &quit)

	http.Handle("/", addHeaders(http.FileServer(http.Dir(dir))))
	http.Handle("/channel1", addHeaders(readStreamming(streamingFilePath, &mutex)))
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

func runStreaming(mutex *sync.RWMutex, ticker *time.Ticker, quit *chan int) {
	dir := filepath.Join("..", "..", "music")
	streamingFilePath := filepath.Join(dir, "stream.m3u8")
	manager, err := channel.CreateManager(dir, streamingFilePath, mutex)
	if err != nil {
		log.Println(err)
		ticker.Stop()
		return
	}

	err = manager.InitWriteRecord(filepath.Join("..", "..", "music", "bathroom", "outputlist.m3u8"), 5)
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

func readStreamming(pathToStrimming string, mutex *sync.RWMutex, man *channel.Manager) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		log.Println("READ")
		mutex.RLock()
		http.ServeFile(w, r, pathToStrimming)
		mutex.RUnlock()
		log.Println("DONE")
	}
}
