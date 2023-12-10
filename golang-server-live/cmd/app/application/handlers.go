package application

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"

	"github.com/sound-org/radio-ai/server/internal/channel"
	"github.com/sound-org/radio-ai/server/internal/cnf"
	"github.com/sound-org/radio-ai/server/pkg/utils"
)

// createHandler creates and configures an HTTP handler for serving various endpoints.
//
// Parameters:
//   - config: A pointer to the configuration object.
//   - channels: A slice of pointers to channel objects representing different channels.
//
// Returns:
//   - http.Handler: An HTTP handler configured to serve specific endpoints.
//
// Example usage:
//
//	config := // initialize your configuration
//	channels := // initialize your channels
//	handler := createHandler(config, channels)
//	http.ListenAndServe(":8080", handler)
func createHandler(config *cnf.Config, channels []*channel.Channel) http.Handler {
	mux := http.NewServeMux()

	mux.Handle("/info", addHeaders(infoHandler(config),
		map[string]string{
			"Content-Type":                 "application/json",
			"Access-Control-Allow-Origin":  "*",
			"Access-Control-Allow-Methods": "*",
			"Access-Control-Allow-Headers": "Content-Type",
		}))

	for i, c := range channels {
		log.Printf("[INIT]: manifest endpoint:\"%s\"", c.Config.Hls)
		mux.Handle(fmt.Sprintf("/%s", c.Config.Hls), addHeaders(channelHandler(channels[i]),
			map[string]string{
				"Access-Control-Allow-Origin": "*",
			}))
	}

	log.Printf("[INIT]: resource endpoint:\"%s\"", "channels")
	mux.Handle("/channels/", addHeaders(channelResource("."),
		map[string]string{
			"Access-Control-Allow-Origin": "*",
		}))

	return mux
}

// addHeaders is a middleware function that wraps an HTTP handler and adds custom headers
// to the response before passing the request to the underlying handler.
//
// Parameters:
//   - h: The HTTP handler to wrap.
//   - headers: A map of header key-value pairs to be added to the response.
//
// Returns:
//   - http.HandlerFunc: An HTTP handler function with added custom headers.
//
// Example usage:
//
//	originalHandler := // your original HTTP handler
//	headers := map[string]string{
//	    "Content-Type": "application/json",
//	    "Custom-Header": "value",
//	}
//	handlerWithHeaders := addHeaders(originalHandler, headers)
//	http.ListenAndServe(":8080", handlerWithHeaders)
func addHeaders(h http.Handler, headers map[string]string) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		for key, value := range headers {
			w.Header().Set(key, value)
		}
		h.ServeHTTP(w, r)
	}
}

// infoHandler creates an HTTP handler function that responds with channel information
// in JSON format based on the provided configuration.
//
// Parameters:
//   - cnfg: A pointer to the configuration object containing channel information.
//
// Returns:
//   - http.HandlerFunc: An HTTP handler function that writes JSON response with channel information.
//
// Example usage:
//
//	config := // initialize your configuration
//	handler := infoHandler(config)
//	http.ListenAndServe(":8080", handler)
func infoHandler(cnfg *cnf.Config) http.HandlerFunc {

	type info struct {
		Id   uint   `json:"id"`
		Name string `json:"name"`
		Desc string `json:"description"`
		Hls  string `json:"hls_path"`
	}

	return func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		infos := utils.Map[cnf.ChannelConfig, info](cnfg.Channels, func(cc cnf.ChannelConfig) info {
			return info{
				Id:   cc.Id,
				Name: cc.Name,
				Desc: cc.Desc,
				Hls:  cc.Hls,
			}
		})
		json.NewEncoder(w).Encode(infos)
	}
}

// channelHandler creates an HTTP handler function for serving a specific channel's content manifest.
//
// Parameters:
//   - channel: A pointer to the channel object containing the streaming information.
//
// Returns:
//   - http.HandlerFunc: An HTTP handler function that writes the channel's content manifest to the response.
//
// Example usage:
//
//	myChannel := // initialize your channel
//	handler := channelHandler(myChannel)
//	http.ListenAndServe(":8080", handler)
func channelHandler(channel *channel.Channel) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		hls := channel.Stream()
		hls.Write(w)
	}
}

// channelResource creates an HTTP handler that serves static files from the specified directory.
//
// Parameters:
//   - paths: The root directory containing the static files to be served.
//
// Returns:
//   - http.Handler: An HTTP handler that serves static files using http.FileServer.
//
// Example usage:
//
//	handler := channelResource("/path/to/static/files")
//	http.ListenAndServe(":8080", handler)
func channelResource(paths string) http.Handler {
	return http.FileServer(http.Dir(paths))
}
