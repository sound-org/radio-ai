package hls

import (
	"bufio"
	"fmt"
	"net/http"
	"os"
	"regexp"
	"strconv"
	"strings"
	"text/template"
)

type TsFile struct {
	Header string
	Name   string
}

type Metadata struct {
	Version  uint16
	Sequence uint32
	Cache    string
	Duration float32
}

type Playlist struct {
	Metadata Metadata
	Ts       []TsFile
	HasEnd   bool
	ToDelete bool
}

func Load(rd *os.File) (*Playlist, error) {
	scanner := bufio.NewScanner(rd)

	metadata := parseMetadata(scanner)
	if err := scanner.Err(); err != nil {
		return nil, err
	}

	ts, hasEnd := parseBody(scanner)
	if err := scanner.Err(); err != nil {
		return nil, err
	}

	return &Playlist{
		Metadata: *metadata,
		Ts:       *ts,
		ToDelete: false,
		HasEnd:   hasEnd,
	}, nil
}

func parseMetadata(scanner *bufio.Scanner) *Metadata {
	scanner.Scan()
	header := extract(scanner.Text(), "#EXTM3U")
	scanner.Scan()
	version := extract(scanner.Text(), "#EXT-X-VERSION:*")
	scanner.Scan()
	sequence := extract(scanner.Text(), "#EXT-X-MEDIA-SEQUENCE:*")
	scanner.Scan()
	cache := extract(scanner.Text(), "#EXT-X-ALLOW-CACHE:*")
	scanner.Scan()
	duration := extract(scanner.Text(), "#EXT-X-TARGETDURATION:*")

	if header != "" {
		panic(fmt.Errorf("wrong header in a file"))
	}

	versionNumber, err := strconv.ParseUint(version, 10, 16)
	if err != nil {
		panic(err)
	}

	sequenceNumber, err := strconv.ParseUint(sequence, 10, 32)
	if err != nil {
		panic(err)
	}

	durationNumber, err := strconv.ParseFloat(duration, 32)
	if err != nil {
		panic(err)
	}

	return &Metadata{
		Version:  uint16(versionNumber),
		Sequence: uint32(sequenceNumber),
		Duration: float32(durationNumber),
		Cache:    cache,
	}
}

func parseBody(scanner *bufio.Scanner) (*[]TsFile, bool) {
	var ts []TsFile
	for scanner.Scan() {
		if scanner.Text() == "#EXT-X-ENDLIST" {
			return &ts, true
		}
		header := scanner.Text()
		scanner.Scan()
		name := scanner.Text()
		ts = append(ts, TsFile{
			Header: header,
			Name:   name,
		})
	}

	return &ts, false
}

func extract(line, pattern string) string {
	matched, err := regexp.MatchString(pattern, line)
	if err != nil {
		panic(err)
	}
	if !matched {
		panic(fmt.Errorf("field with pattern %s not found", pattern))
	}
	fieldName := strings.Replace(pattern, "*", "", -1)
	return strings.Replace(line, fieldName, "", -1)

}

func (record *Playlist) SaveToFile(wr *os.File, path string) error {
	str := "#EXTM3U\n" +
		"#EXT-X-VERSION:{{ .Metadata.Version }}\n" +
		"#EXT-X-MEDIA-SEQUENCE:{{ .Metadata.Sequence }}\n" +
		"#EXT-X-ALLOW-CACHE:{{ .Metadata.Cache }}\n" +
		"#EXT-X-TARGETDURATION:{{ .Metadata.Duration }}\n" +
		"{{ range .Ts }}{{ .Header }}\n{{ .Name }}\n{{ end }}" +
		"{{ if .HasEnd }}#EXT-X-ENDLIST{{ else }}{{ end }}\n"

	t, err := template.New("manifest").Parse(str)
	if err != nil {
		return err
	}

	err = t.Execute(wr, record)
	if err != nil {
		return err
	}

	return nil
}

func (playlist *Playlist) Save(wr http.ResponseWriter) error {
	str := "#EXTM3U\n" +
		"#EXT-X-VERSION:{{ .Metadata.Version }}\n" +
		"#EXT-X-MEDIA-SEQUENCE:{{ .Metadata.Sequence }}\n" +
		"#EXT-X-ALLOW-CACHE:{{ .Metadata.Cache }}\n" +
		"#EXT-X-TARGETDURATION:{{ .Metadata.Duration }}\n" +
		"{{ range .Ts }}{{ .Header }}\n{{ .Name }}\n{{ end }}" +
		"{{ if .HasEnd }}#EXT-X-ENDLIST{{ else }}{{ end }}\n"

	t, err := template.New("manifest").Parse(str)
	if err != nil {
		return err
	}

	err = t.Execute(wr, playlist)
	if err != nil {
		return err
	}

	return nil
}
