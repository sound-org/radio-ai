package reader

import (
	"errors"
	"log"
	"os"
	"path/filepath"
	"sync"
	"testing"
	"time"

	"github.com/sound-org/radio-ai/server/internal/hls"
	"github.com/sound-org/radio-ai/server/internal/utils"
)

func TestReadDirectory(t *testing.T) {
	// given
	path := filepath.Join("..")

	dirs, err := getFiles(path, "*.go")
	if err != nil {
		log.Fatal(err)
	}

	log.Println(dirs)

	if len(dirs) == 0 {
		log.Fatalf("content of directory: %s is empty or nill", path)
	}
}

func TestIsToDelete(t *testing.T) {
	// given
	now := time.Now()
	fileModification := time.Now().Add(-2*24*time.Hour + 2*time.Minute)
	maxLifespan := 2

	if isToDelete(now, fileModification, maxLifespan) {
		log.Fatal("time is wrongly calculated")
	}
}

func TestAddRecord(t *testing.T) {
	file, err := utils.CreateSimpleM3U8(".")
	if err != nil {
		log.Fatal(err)
	}
	defer os.Remove(file.Name())

	manager := Manager{
		ReadRecords:   make(map[string]*hls.Record),
		WriteRecord:   hls.Record{},
		StreamingFile: nil,
		Mutex:         &sync.RWMutex{},
	}

	if manager.addRecord(file.Name()) != 1 {
		log.Fatal("file was not added")
	}
}

func TestMarkToDelete(t *testing.T) {
	file, err := utils.CreateSimpleM3U8(".")
	if err != nil {
		log.Fatal(err)
	}
	defer os.Remove(file.Name())

	err = utils.ChModTime(file, 2, 20)
	if err != nil {
		log.Fatal(err)
	}

	manager := Manager{
		ReadRecords:   make(map[string]*hls.Record),
		WriteRecord:   hls.Record{},
		StreamingFile: nil,
		Mutex:         &sync.RWMutex{},
	}

	if manager.addRecord(file.Name()) != 1 {
		log.Fatal("file was not added")
	}

	manager.markToDelete()
	if !manager.ReadRecords[file.Name()].ToDelete {
		log.Fatal("file was not marked to be deleted")
	}
}

func TestDelete(t *testing.T) {
	path := filepath.Join(".", "temp")
	os.Mkdir("temp", 0755)
	log.Println(path)
	file, err := utils.CreateSimpleM3U8(path)
	if err != nil {
		log.Fatal(err)
	}
	err = utils.ChModTime(file, 2, 20)
	if err != nil {
		log.Fatal(err)
	}

	manager := Manager{
		ReadRecords:   make(map[string]*hls.Record),
		WriteRecord:   hls.Record{},
		StreamingFile: nil,
		Mutex:         &sync.RWMutex{},
	}

	manager.addRecord(file.Name())
	manager.markToDelete()
	manager.delete()

	if _, err := os.Stat(file.Name()); !errors.Is(err, os.ErrNotExist) || len(manager.ReadRecords) != 0 {
		log.Fatal("file was not deleted")
	}

}

func TestCreateMAnager(t *testing.T) {
	path := filepath.Join(".", "temp")
	os.Mkdir("temp", 0755)
	defer os.RemoveAll(path)

	file, err := utils.CreateSimpleM3U8(path)
	if err != nil {
		log.Fatal(err)
	}

	mutex := sync.RWMutex{}
	manager, err := CreateManager(".", "streaming1.m3u8", &mutex)
	if err != nil {
		log.Fatal(err)
	}

	if _, exists := manager.ReadRecords[file.Name()]; !exists {
		log.Fatalf("file %s does not exists in the records", file.Name())
	}

	manager.StreamingFile.Close()
	err = os.Remove(manager.StreamingFile.Name())
	if err != nil {
		log.Fatal(err)
	}
}
