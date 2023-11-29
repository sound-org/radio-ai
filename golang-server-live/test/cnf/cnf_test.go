package cnf_test

import (
	"log"
	"os"
	"testing"

	"github.com/sound-org/radio-ai/server/internal/cnf"
	test_utils "github.com/sound-org/radio-ai/server/internal/utils"
)

func TestLoad(t *testing.T) {

	// given
	file, err := test_utils.CreateFile(test_utils.GetConfiguration(), ".", "test_config*.json")
	if err != nil {
		log.Fatal(err)
	}
	defer os.Remove(file.Name())

	config, err := cnf.Load(file.Name())
	if err != nil {
		log.Fatal(err)
	}

	if len(config.Channels) != 2 {
		t.FailNow()
	}

}
