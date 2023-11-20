package main

import (
	"log"
	"os"

	"github.com/sound-org/radio-ai/server/cmd/app/application"
)

func main() {

	arg := os.Args[1]

	app, err := application.Create(arg)
	if err != nil {
		panic(err)
	}

	log.Fatal(app.Start())

}
