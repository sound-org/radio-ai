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

// Create initializes and returns an instance of the App by loading configuration,
// creating channels, and setting up an HTTP server.
//
// Parameters:
//   - path: The path to the configuration file.
//
// Returns:
//   - *App: A pointer to the initialized App instance.
//   - error: An error, if any, encountered during initialization.
//
// Example usage:
//
//	app, err := Create("/path/to/config")
//	if err != nil {
//	    // handle the error
//	}
//	// Use the 'app' instance for further operations.
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

// createServer creates and configures an HTTP server based on the provided configuration and channels.
//
// Parameters:
//   - config: A pointer to the configuration object.
//   - channels: A slice of pointers to channel objects representing different channels.
//
// Returns:
//   - *http.Server: A pointer to the configured HTTP server.
//   - error: An error, if any, encountered during server creation.
//
// Example usage:
//
//	config := // initialize your configuration
//	channels := // initialize your channels
//	server, err := createServer(config, channels)
//	if err != nil {
//	    // handle the error
//	}
//	// Start the server: server.ListenAndServe()
func createServer(config *cnf.Config, channels []*channel.Channel) (*http.Server, error) {

	mux := createHandler(config, channels)

	return &http.Server{
		Addr:         ":" + config.Server.Port,
		Handler:      mux,
		ReadTimeout:  time.Duration(config.Server.ReadTimeout) * time.Millisecond,
		WriteTimeout: time.Duration(config.Server.WriteTimeout) * time.Microsecond,
	}, nil
}

// Start initiates the application by launching the configured channels and starting the HTTP server.
// It also logs the application's configuration and status.
//
// Returns:
//   - error: An error, if any, encountered during the application start process.
//
// Example usage:
//
//	app := // initialize your App
//	err := app.Start()
//	if err != nil {
//	    // handle the error
//	}
//	// The application is now running.
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
