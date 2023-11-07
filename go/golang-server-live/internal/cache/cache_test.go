package channel

import (
	"log"
	"os"
	"path/filepath"
	"sync"
	"testing"

	"github.com/sound-org/radio-ai/server/internal/hls"
	internal_utils "github.com/sound-org/radio-ai/server/internal/utils"
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

func TestAddRecord(t *testing.T) {
	file, err := internal_utils.CreateSimpleM3U8(".")
	if err != nil {
		log.Fatal(err)
	}
	defer os.Remove(file.Name())

	manager := Manager{
		ReadRecords:   make(map[string]*hls.Playlist),
		WriteRecord:   hls.Playlist{},
		StreamingFile: nil,
		Mutex:         &sync.RWMutex{},
	}

	if manager.addRecord(file.Name()) != 1 {
		log.Fatal("file was not added")
	}
}

func TestCreateManager(t *testing.T) {
	path := filepath.Join(".", "temp")
	os.Mkdir("temp", 0755)
	defer os.RemoveAll(path)

	file, err := internal_utils.CreateSimpleM3U8(path)
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

func TestRefresh(t *testing.T) {

	mutex := sync.RWMutex{}
	manager, err := CreateManager(".", "streaming1.m3u8", &mutex)
	if err != nil {
		log.Fatal(err)
	}

	path := filepath.Join(".", "temp")
	os.Mkdir("temp", 0755)
	defer os.RemoveAll(path)

	file, err := internal_utils.CreateSimpleM3U8(path)
	if err != nil {
		log.Fatal(err)
	}
	file.Close()

	wasAdded, err := manager.refresh(path)
	if err != nil {
		log.Fatal(err)
	}

	if !wasAdded {
		log.Fatalf("cache not refreshed for file %v", file.Name())
	}

	manager.StreamingFile.Close()
	err = os.Remove(manager.StreamingFile.Name())
	if err != nil {
		log.Fatal(err)
	}
}

func TestInitWriteRecord(t *testing.T) {
	path := filepath.Join(".", "temp")
	os.Mkdir("temp", 0755)
	defer os.RemoveAll(path)

	file, err := internal_utils.CreateSimpleM3U8(path)
	if err != nil {
		log.Fatal(err)
	}

	mutex := sync.RWMutex{}
	manager, err := CreateManager(".", "streaming1.m3u8", &mutex)
	if err != nil {
		log.Fatal(err)
	}

	err = manager.InitWriteRecord(file.Name(), 4)
	if err != nil {
		log.Fatal(err)
	}

	if len(manager.WriteRecord.Ts) == 0 {
		log.Fatal("record was not added")
	}

	manager.StreamingFile.Close()
	err = os.Remove(manager.StreamingFile.Name())
	if err != nil {
		log.Fatal(err)
	}
}

func TestUpdateWriteRecords(t *testing.T) {
	path := filepath.Join(".", "temp")
	os.Mkdir("temp", 0755)
	defer os.RemoveAll(path)

	file, err := internal_utils.CreateSimpleM3U8(path)
	if err != nil {
		log.Fatal(err)
	}

	mutex := sync.RWMutex{}
	manager, err := CreateManager(".", "streaming1.m3u8", &mutex)
	if err != nil {
		log.Fatal(err)
	}

	err = manager.InitWriteRecord(file.Name(), 5)
	if err != nil {
		log.Fatal(err)
	}

	update, err := manager.UpdateWriteRecord(file.Name(), 2, 1)
	if err != nil {
		log.Fatal(err)
	}

	if update {
		log.Fatal("case should not require update")
	}

	lastElement := manager.WriteRecord.Ts[len(manager.WriteRecord.Ts)-1]
	if lastElement.Name != "temp/ts/output002.ts" {
		log.Fatalf("last record expected to be temp/ts/output002.ts but was %s", lastElement.Name)
	}

	manager.StreamingFile.Close()
	err = os.Remove(manager.StreamingFile.Name())
	if err != nil {
		log.Fatal(err)
	}
}
