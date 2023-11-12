# radio-ai

How To:

- to create a new radio broadcast, create a POST request at <http://localhost:8000/channels/prepare-broadcast>

GO:

 W `/go` znajduje się server obsługujący HLS. Aby go odpalić potrzeba go <=1.21.3
 Klienta możnma odpalić tu : <https://hlsjs-dev.video-dev.org/demo/>  w linku do src wpicas <http://localhost:8080/outputlist.m3u8>
 Server odpalać z pliku /cmd/app/main.go komendą go run .

HLS:

 Tworzenie plików .ts oraz playlisty .m3u8 przez ffmpeg :
  `ffmpeg -i x.mp3 -c:a libmp3lame -b:a 128k -map 0:0 -f segment -segment_time 10 -segment_list outputlist.m3u8 -segment_format mpegts output%03d.ts`

MIDI to MP3:
Ja korzystam z fluidsynth
`fluidsynth -a alsa -T raw -F - soundfont.sf2 MIDI_sample.mid |
  ffmpeg -f s32le -i - MIDI_sample.mp3`
