package config

import (
	"encoding/json"
	"net/http"
	"os"
	"time"
)

type Config struct {
	Channels []channelConfig `json:"channels"`
	Server   serverConfig    `json:"server"`
}

type channelConfig struct {
	Id   uint   `json:"id"`
	Name string `json:"name"`
	Desc  string `json:"description"`
	Hls  string `json:"hls_path"`
}

type serverConfig struct {
	Port         string `json:"port"`
	ReadTimeout  uint   `json:"readTimeout"`
	WriteTimeout uint   `json:"writeTimeout"`
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

func CreateServer(config *Config) *http.Server {
	return &http.Server{
		Addr:         ":" + config.Server.Port,
		Handler:      createHandlers(config),
		ReadTimeout:  time.Duration(config.Server.ReadTimeout) * time.Millisecond,
		WriteTimeout: time.Duration(config.Server.WriteTimeout) * time.Microsecond,
	}
}

func createHandlers(config *Config) http.Handler {
	mux := http.NewServeMux()

	mux.Handle("/info", InfoHandler(config))

	return mux
}

func InfoHandler(config *Config) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		w.Header().Set("Access-Control-Allow-Origin", "*")
		w.Header().Set("Access-Control-Allow-Methods", "*")
		w.Header().Set("Access-Control-Allow-Headers", "Content-Type")
		w.WriteHeader(http.StatusOK)
		json.NewEncoder(w).Encode(config.Channels)
	}
}
