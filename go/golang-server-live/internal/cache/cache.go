package channel

import (
	"fmt"
	"io/fs"
	"os"
	"path/filepath"
	"strings"
	"sync"

	"github.com/sound-org/radio-ai/server/internal/hls"
	utils "github.com/sound-org/radio-ai/server/pkg"
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
	MusicDir      string
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
		MusicDir:    path,
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

	man.WriteRecord.Ts = append(man.WriteRecord.Ts, utils.Map(val.Ts[0:min(len(val.Ts), heapSize)], createMapping(name, man.MusicDir))...)
	man.WriteRecord.Metadata.Sequence = 0
	return nil

}

func (man *Manager) UpdateWriteRecord(name string, count, offset int) (bool, error) {
	val, ok := man.ReadRecords[name]
	if !ok {
		return false, fmt.Errorf("palylist %s was not found", name)
	}
	if len(val.Ts) <= offset {
		return false, fmt.Errorf("offset outside of range")
	}

	man.WriteRecord.Ts = man.WriteRecord.Ts[count:]
	man.WriteRecord.Ts = append(man.WriteRecord.Ts, utils.Map(val.Ts[offset:min(len(val.Ts), offset+count)], createMapping(name, man.MusicDir))...)
	man.WriteRecord.Metadata.Sequence = man.WriteRecord.Metadata.Sequence + uint32(count)

	return count+offset >= len(val.Ts), nil
}

func getPathWithoutMusicDirPath(playlistPath, tsPath, musicPath string) string {
	return filepath.ToSlash(strings.TrimPrefix(filepath.Join(filepath.Dir(playlistPath), tsPath), musicPath+string(os.PathSeparator)))
}

func createMapping(name, musicDir string) func(ts hls.TsFile) hls.TsFile {
	return func(ts hls.TsFile) hls.TsFile {
		return hls.TsFile{
			Header: ts.Header,
			Name:   getPathWithoutMusicDirPath(name, ts.Name, musicDir),
		}
	}
}

func (man *Manager) Save() {
	man.Mutex.Lock()
	man.StreamingFile.Seek(0, 0)
	man.WriteRecord.SaveToFile(man.StreamingFile, man.StreamingFile.Name())
	man.Mutex.Unlock()
}
