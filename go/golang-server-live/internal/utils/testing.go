package utils

import (
	"os"
	"time"
)

func CreateSimpleM3U8(path string) (*os.File, error) {
	file, err := os.CreateTemp(path, "test")
	if err != nil {
		return nil, err
	}
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

	return file, nil
}

func ChModTiime(file *os.File, days, mins int) error {
	now := time.Now()
	toDeleteDate := time.Now().Add(time.Duration(days)*-24*time.Hour - time.Duration(mins)*time.Minute)
	err := os.Chtimes(file.Name(), now, toDeleteDate)
	if err != nil {
		return err
	}

	return nil
}
