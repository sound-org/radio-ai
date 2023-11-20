package application

import (
	"encoding/json"
	"log"
	"net/http"
	"time"

	"github.com/sound-org/radio-ai/server/internal/channel"
	"github.com/sound-org/radio-ai/server/internal/cnf"
	"github.com/sound-org/radio-ai/server/pkg/utils"
)

type App struct {
	server   *http.Server
	channels []*channel.Channel
	config   *cnf.Config
}

func Create(path string) (*App, error) {

	cnfg, err := cnf.Load(path)
	if err != nil {
		return nil, err
	}

	channels := utils.Map[cnf.ChannelConfig, *channel.Channel](cnfg.Channels, func(cc cnf.ChannelConfig) *channel.Channel {
		return channel.FromConfig(cc)
	})

	server, err := createServer(cnfg, channels)
	if err != nil {
		return nil, err
	}

	return &App{
		config:   cnfg,
		channels: channels,
		server:   server,
	}, nil
}

func createServer(config *cnf.Config, channels []*channel.Channel) (*http.Server, error) {

	mux := createHandler(config, channels)

	return &http.Server{
		Addr:         ":" + config.Server.Port,
		Handler:      mux,
		ReadTimeout:  time.Duration(config.Server.ReadTimeout) * time.Millisecond,
		WriteTimeout: time.Duration(config.Server.WriteTimeout) * time.Microsecond,
	}, nil
}

func (app *App) Start() error {

	quit := make(chan bool)

	body, err := json.MarshalIndent(app.config, "", "  ")
	if err != nil {
		return err
	}

	for i := range app.channels {
		go channel.Run(app.channels[i], &quit)
	}

	log.Printf("Application started with config\n%s", string(body))

	return app.server.ListenAndServe()
}
