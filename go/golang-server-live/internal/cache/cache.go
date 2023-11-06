package channel

import (
	"fmt"
	"io/fs"
	"os"
	"path/filepath"
	"sync"

	"github.com/sound-org/radio-ai/server/internal/hls"
)

// hls main streaming file configs
const version = 3
const beginSequence = 0
const enableCache = "NO"
const maxDuration = 11

func getFiles(path, pattern string) ([]string, error) {
	var paths []string

	err := filepath.Walk(path, func(path string, info fs.FileInfo, err error) error {
		if err != nil {
			return err
		}
		if info.IsDir() {
			return nil
		}
		if matched, err := filepath.Match(pattern, filepath.Base(path)); err != nil {
			return err
		} else if matched {
			paths = append(paths, path)
		}
		return nil
	})
	if err != nil {
		return nil, err
	}

	return paths, nil
}

type Manager struct {
	ReadRecords   map[string]*hls.Playlist
	WriteRecord   hls.Playlist
	StreamingFile *os.File
	Mutex         *sync.RWMutex
}

func (man *Manager) addRecord(path string) int {
	file, err := os.Open(path)
	if err != nil {
		return len(man.ReadRecords)
	}
	defer file.Close()

	record, err := hls.Load(file)
	if err != nil {
		return len(man.ReadRecords)
	}

	man.ReadRecords[path] = record

	return len(man.ReadRecords)
}

func CreateManager(path, streamingName string, mutex *sync.RWMutex) (*Manager, error) {
	paths, err := getFiles(path, "*.m3u8")
	if err != nil {
		return nil, fmt.Errorf("path %v does not contain any subdirectory", path)
	}

	file, err := os.Create(streamingName)
	if err != nil {
		return nil, err
	}

	manager := Manager{
		ReadRecords: make(map[string]*hls.Playlist),
		WriteRecord: hls.Playlist{
			Metadata: hls.Metadata{
				Version:  version,
				Sequence: beginSequence,
				Cache:    enableCache,
				Duration: maxDuration,
			},
			Ts:       []hls.TsFile{},
			HasEnd:   false,
			ToDelete: false,
		},
		StreamingFile: file,
		Mutex:         mutex,
	}

	for _, entry := range paths {
		manager.addRecord(entry)
	}

	return &manager, nil
}

func (man *Manager) refresh(path string) (bool, error) {
	paths, err := getFiles(path, "*.m3u8")
	if err != nil {
		return false, err
	}

	wasAdded := false

	for _, p := range paths {
		if _, ok := man.ReadRecords[p]; !ok {
			man.addRecord(p)
			wasAdded = true
		}
	}

	return wasAdded, nil
}

func (man *Manager) InitWriteRecord(name string, heapSize int) error {
	val, ok := man.ReadRecords[name]
	if !ok {
		return fmt.Errorf("playlist %s was not found", name)
	}

	for i := 0; i < min(len(val.Ts), heapSize); i++ {
		man.WriteRecord.Ts = append(man.WriteRecord.Ts, val.Ts[i])
	}
	man.WriteRecord.Metadata.Sequence = 0
	return nil

}

func (man *Manager) UpdateWriteRecord(name string, count, offset int) (bool, error) {
	// TODO : Fix adding path to output, currently returninng name from playlist not full path
	// TODO : Fix doesn't put last piece of ts before requesting of update
	val, ok := man.ReadRecords[name]
	if !ok {
		return false, fmt.Errorf("palylist %s was not found", name)
	}
	if len(val.Ts) <= offset {
		return false, fmt.Errorf("offset outside of range")
	}

	man.WriteRecord.Ts = man.WriteRecord.Ts[count:]
	man.WriteRecord.Ts = append(man.WriteRecord.Ts, val.Ts[offset:min(len(val.Ts)-1, offset+count)]...)
	man.WriteRecord.Metadata.Sequence = man.WriteRecord.Metadata.Sequence + uint32(count)

	return count+offset >= len(val.Ts), nil
}
