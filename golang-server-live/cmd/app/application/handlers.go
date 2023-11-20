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

func addHeaders(h http.Handler, headers map[string]string) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		for key, value := range headers {
			w.Header().Set(key, value)
		}
		h.ServeHTTP(w, r)
	}
}

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

func channelHandler(channel *channel.Channel) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		hls := channel.Stream()
		hls.Write(w)
	}
}

func channelResource(paths string) http.Handler {
	return http.FileServer(http.Dir(paths))
}
