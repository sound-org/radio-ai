package test_utils

import (
	"os"
)

// CreateFile creates a temporary file with the specified content and file name pattern in the given directory.
// The created file is returned as an os.File pointer.
//
// Parameters:
//   - content:   The content to be written to the created file.
//   - path:      The directory in which the temporary file will be created.
//   - nameRegex:  The regular expression pattern for generating the temporary file name.
//
// Returns:
//   - *os.File:  A pointer to the created os.File instance.
//   - error:      An error, if any, encountered during the file creation process.
//
// Example usage:
//
//	fileContent := // specify the content for the file
//	directoryPath := // specify the directory path for creating the file
//	namePattern := // specify the regular expression pattern for the file name
//	createdFile, err := CreateFile(fileContent, directoryPath, namePattern)
//	if err != nil {
//	    // handle the error
//	}
func CreateFile(content, path, nameRegex string) (*os.File, error) {
	file, err := os.CreateTemp(path, nameRegex)
	if err != nil {
		return nil, err
	}
	defer file.Close()
	file.WriteString(content)
	return file, err
}

// GetM3U8 generates and returns a sample M3U8 playlist string with predefined metadata and media segments.
//
// Returns:
//   - string: The generated M3U8 playlist string.
//
// Example usage:
//
//	m3u8Playlist := GetM3U8()
func GetM3U8() string {
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

	return str
}

// GetConfiguration returns a sample JSON string representing a configuration with multiple channels and server settings.
//
// Returns:
//   - string: The sample JSON configuration string.
//
// Example usage:
//
//	configurationJSON := GetConfiguration()
func GetConfiguration() string {
	return "{\"channels\":[{\"id\":1,\"name\":\"channel-1\",\"description\":\"channel-1description\",\"hls_path\":\"channels/1/streaming/manifest\",\"broadcast_output_dir\":\"channels/1/broadcast\",\"streaming_output_dir\":\"channels/1/streaming\",\"speaker\":{\"name\":\"Bob\",\"TTS\":\"PYTTSX3\",\"voice\":\"english\",\"personality\":\"YourareandradioDJ,youlovegoodhardrockmusic,theharderthebettermusic,youaredefinitelycrazy\",\"output_dir\":\"channels/1/speaker\"},\"music\":{\"music_generators\":[{\"type\":\"ai\",\"theme\":\"Classicjazzmusicwithamoderntwist\",\"output_dir\":\"channels/1/music/ai\"},{\"type\":\"algorithmic\",\"output_dir\":\"channels/1/music/algorithmic\"}]},\"hls\":{\"buffer\":10,\"pushSize\":2,\"version\":3,\"sequence\":0,\"duration\":11,\"cache\":false}},{\"id\":2,\"name\":\"channel-2\",\"description\":\"channel-2description\",\"hls_path\":\"channels/2/streaming/manifest\",\"broadcast_output_dir\":\"channels/2/broadcast\",\"streaming_output_dir\":\"channels/2/streaming\",\"speaker\":{\"name\":\"Bob\",\"TTS\":\"PYTTSX3\",\"voice\":\"english\",\"personality\":\"YourareandradioDJ,youlovegoodhardrockmusic,theharderthebettermusic,youaredefinitelycrazy\",\"output_dir\":\"channels/2/speaker\"},\"music\":{\"music_generators\":[{\"type\":\"ai\",\"theme\":\"Classicjazzmusicwithamoderntwist\",\"output_dir\":\"channels/2/music/ai\"},{\"type\":\"ai\",\"theme\":\"Goodoldrockmusic\",\"output_dir\":\"channels/2/music/ai\"},{\"type\":\"ai\",\"theme\":\"PsychedelicandalternativerockmusiclikeaPinkFloyd\",\"output_dir\":\"channels/2/music/ai\"}]},\"hls\":{\"buffer\":10,\"pushSize\":2,\"version\":3,\"sequence\":0,\"duration\":11,\"cache\":false}}],\"server\":{\"port\":\"8080\",\"readTimeout\":10000,\"writeTimeout\":10000}}"
}
