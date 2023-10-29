package hls

import (
	"log"
	"os"
	"testing"
)

func TestLoadRecord(t *testing.T) {

	// given
	file, err := os.CreateTemp(".", "test")
	if err != nil {
		log.Fatal(err)
	}
	defer os.Remove(file.Name())
	defer file.Close()

	str := "#EXTM3U\n" +
		"#EXT-X-VERSION:3\n" +
		"#EXT-X-MEDIA-SEQUENCE:0\n" +
		"#EXT-X-ALLOW-CACHE:YES\n" +
		"#EXT-X-TARGETDURATION:11\n" +
		"#EXTINF:10.004900,\n" +
		"ts/output000.ts\n" +
		"#EXTINF:10.004900,\n" +
		"ts/output001.ts\n" +
		"#EXTINF:10.004889,\n" +
		"ts/output002.ts\n" +
		"#EXTINF:10.004900,\n" +
		"ts/output003.ts\n" +
		"#EXTINF:0.887100,\n" +
		"ts/output024.ts\n" +
		"#EXT-X-ENDLIST\n"

	file.WriteString(str)

	reader, err := os.Open(file.Name())
	if err != nil {
		log.Fatal(err)
	}
	defer reader.Close()

	rec, err := Load(reader)
	if err != nil {
		log.Fatal(err)
	}

	if assertRecord(rec) {
		log.Fatal("Loading is failing")
	}
}

func assertRecord(rec *Record) bool {
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
