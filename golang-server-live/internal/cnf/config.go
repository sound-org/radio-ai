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
