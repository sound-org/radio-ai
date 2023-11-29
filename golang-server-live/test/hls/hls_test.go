package hls

import (
	"log"
	"os"
	"testing"

	"github.com/sound-org/radio-ai/server/internal/hls"
	test_utils "github.com/sound-org/radio-ai/server/test/utils"
)

func TestLoadRecord(t *testing.T) {

	// given
	file, err := test_utils.CreateFile(test_utils.GetM3U8(), ".")
	if err != nil {
		log.Fatal(err)
	}
	defer os.Remove(file.Name())

	reader, err := os.Open(file.Name())
	if err != nil {
		log.Fatal(err)
	}
	defer reader.Close()

	rec, err := hls.Load(reader)
	if err != nil {
		log.Fatal(err)
	}

	if assertRecord(rec) {
		log.Fatal("Loading is failing")
	}
}

func assertRecord(rec *hls.Playlist) bool {
	ok := true

	ok = ok && rec.Metadata.Version == 3
	ok = ok && rec.Metadata.Sequence == 0
	ok = ok && rec.Metadata.Cache == "YES"
	ok = ok && rec.Metadata.Duration == 11
	ok = ok && len(rec.Ts) == 5
	ok = ok && rec.Ts[3].Header == "#EXTINF:10.004889,"
	ok = ok && rec.Ts[4].Name == "ts/output024.ts"
	ok = ok && rec.HasEnd
	ok = ok && !rec.ToDelete

	return ok
}
