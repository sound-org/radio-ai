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

// Playlist represents a metadata of media segment object from HLS protocol.
type TsFile struct {
	Header string
	Name   string
}

// Playlist represents a metadata of playlist object from HLS protocol.
type Metadata struct {
	Version  uint16
	Sequence uint32
	Cache    string
	Duration float32
}

// Playlist represents a playlist object from HLS protocol.
type Playlist struct {
	Metadata Metadata
	Ts       []TsFile
	HasEnd   bool
	ToDelete bool
}

// Load reads and parses the content of an M3U8 file from the provided file descriptor (os.File).
// It extracts metadata and Ts (media segments) information from the M3U8 file content.
//
// Parameters:
//   - rd: An os.File representing the opened M3U8 file for reading.
//
// Returns:
//   - *Playlist: A pointer to the Playlist instance representing the loaded M3U8 content.
//   - error: An error, if any, encountered during the loading and parsing process.
//
// Example usage:
//
//	fileDescriptor := // open an os.File for the M3U8 file
//	playlist, err := Load(fileDescriptor)
//	if err != nil {
//	    // handle the error
//	}
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

// parseMetadata reads and parses metadata information from a scanner representing an M3U8 file.
// It extracts version, media sequence, cache status, and target duration from the M3U8 file header.
//
// Parameters:
//   - scanner: A bufio.Scanner providing access to the content of the M3U8 file.
//
// Returns:
//   - *Metadata: A pointer to the Metadata instance representing the parsed metadata.
//
// Example usage:
//
//	fileScanner := // create a bufio.Scanner for the M3U8 file
//	metadata := parseMetadata(fileScanner)
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

// parseBody reads and parses the body of an M3U8 file, extracting media segment information (Ts).
// It continues parsing until the end of the file or an "#EXT-X-ENDLIST" marker is encountered.
//
// Parameters:
//   - scanner: A bufio.Scanner providing access to the content of the M3U8 file.
//
// Returns:
//   - *[]TsFile: A pointer to a slice of TsFile instances representing the parsed media segments.
//   - bool: A boolean indicating whether an "#EXT-X-ENDLIST" marker was encountered.
//
// Example usage:
//
//	fileScanner := // create a bufio.Scanner for the M3U8 file
//	tsSegments, hasEnd := parseBody(fileScanner)
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

// extract extracts the value of a field from a line based on a specified pattern.
//
// Parameters:
//   - line:    The input line containing the field value.
//   - pattern: The pattern used to identify the field within the line.
//
// Returns:
//   - string: The extracted value of the field.
//
// Example usage:
//
//	inputLine := // the line containing the field value
//	fieldPattern := // the pattern to identify the field
//	fieldValue := extract(inputLine, fieldPattern)
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

// Write generates and writes the content of an M3U8 manifest to the provided http.ResponseWriter.
// It uses a template to format the playlist's metadata and media segments (Ts) information.
//
// Parameters:
//   - wr:      The http.ResponseWriter to write the M3U8 manifest content to.
//
// Returns:
//   - error:   An error, if any, encountered during the writing process.
//
// Example usage:
//
//	myPlaylist := // initialize your Playlist
//	httpResponseWriter := // obtain the http.ResponseWriter
//	err := myPlaylist.Write(httpResponseWriter)
//	if err != nil {
//	    // handle the error
//	}
func (playlist *Playlist) Write(wr http.ResponseWriter) error {
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
