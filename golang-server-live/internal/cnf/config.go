package cnf

import (
	"encoding/json"
	"os"
)

type Config struct {
	Channels []ChannelConfig `json:"channels"`
	Server   ServerConfig    `json:"server"`
}

type ChannelConfig struct {
	Id     uint      `json:"id"`
	Name   string    `json:"name"`
	Desc   string    `json:"description"`
	Src    string    `json:"streaming_output_dir"`
	Hls    string    `json:"hls_path"`
	Stream HlsConfig `json:"hls"`
}

type ServerConfig struct {
	Port         string `json:"port"`
	ReadTimeout  uint   `json:"readTimeout"`
	WriteTimeout uint   `json:"writeTimeout"`
}

type HlsConfig struct {
	Buffer   uint `json:"buffer"`
	PushSize uint `json:"pushSize"`
	Version  uint `json:"version"`
	Sequence uint `json:"sequence"`
	Duration uint `json:"duration"`
	Cache    bool `json:"cache"`
}

// Load reads a JSON configuration file from the specified path and returns a Config instance.
//
// Parameters:
//   - path: The path to the JSON configuration file.
//
// Returns:
//   - *Config: A pointer to the Config instance representing the loaded configuration.
//   - error: An error, if any, encountered during the loading process.
//
// Example usage:
//
//	configPath := "/path/to/config.json"
//	loadedConfig, err := Load(configPath)
//	if err != nil {
//	    // handle the error
//	}
func Load(path string) (*Config, error) {
	var config Config
	f, err := os.Open(path)
	if err != nil {
		return nil, err
	}
	defer f.Close()

	jsonParser := json.NewDecoder(f)
	if err = jsonParser.Decode(&config); err != nil {
		return nil, err
	}

	return &config, nil
}
