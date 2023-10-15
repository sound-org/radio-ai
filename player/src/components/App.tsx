import './App.css';
import './Slider.css'
import Music from "../interface/Music";
import * as React from "react";
import {ReactElement, useEffect, useRef, useState} from "react";
import {PauseIcon, PlayIcon, SpeakerWaveIcon} from "@heroicons/react/24/solid";
import useWebSocket from 'react-use-websocket';

const App: React.FC = (): ReactElement => {

    const SongsList: Music[]  = [
        {
            source: "assets/sample-music.mp3",
            image: "assets/thumbnail.jpg",
            title: "Sample local song"
        },
        {
            source: "https://www.learningcontainer.com/wp-content/uploads/2020/02/Kalimba.mp3",
            image: "https://images.unsplash.com/photo-1500462918059-b1a0cb512f1d?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1887&q=80",
            title: "Sample online song"
        }
    ];
    const music: Music = SongsList[1];

    // Music controls
    const MAX_VOLUME = 20;
    const [play, setPlay] = useState(true);
    const [volume, setVolume] = useState(MAX_VOLUME)
    const musicRef = useRef<HTMLAudioElement>(null);

    // Socket handling
    const [, setData] = useState<Blob>();
    const [counter, setCounter] = useState(0);
    const [audioURL, setAudioURL] = useState<String>(null);
    const [backupAudioURL, setBackupAudioURL] = useState<String>(null);
    const SERVER_URL = 'ws://localhost:8000';
    const { sendMessage, lastMessage, readyState } = useWebSocket(SERVER_URL);

    useEffect(() => {
        if (lastMessage !== null) {
            setCounter(c => c + 1);

            setData(lastMessage.data);
            const blob = new Blob([lastMessage.data.slice(0, lastMessage.data.length)], {type: "audio/mpeg-3"});

            if (play) {
                try {
                    if (musicRef.current.src === "") {
                        setAudioURL(URL.createObjectURL(blob));
                        musicRef.current.src = audioURL.toString();
                        musicRef.current.play().then(() => setPlay(true));
                    }

                    if (musicRef.current.duration - musicRef.current.currentTime < 5) {
                        console.log(musicRef.current.duration - musicRef.current.currentTime)
                        setAudioURL(backupAudioURL);
                        musicRef.current.src = audioURL.toString();
                        musicRef.current.play().then(() => setPlay(true));
                    } else {
                        setBackupAudioURL(URL.createObjectURL(blob));
                    }
                } catch (e) {
                    console.error(e.toString())
                }
            }
        }
    }, [lastMessage]);

    function togglePlay(): void {
        if (play) {
            musicRef.current?.pause();
            setPlay(false);
        } else {
            void musicRef.current?.play();
            setPlay(true);
        }
    }

    function handleVolume(e: React.ChangeEvent<HTMLInputElement>): void {
        const { value } = e.target;
        const volume = Number(value) / MAX_VOLUME;
        musicRef.current.volume = volume;
        setVolume(volume);
    }

    return (
    <div className="App">
      <header className="App-header">
        rAIdio
      </header>
      <div className="App-body">
          <div className="Player">
              <div className="Player-image">
                      <img src={music.image} className="Player-img" alt="Song thumbnail"/>
                  <button onClick={togglePlay} type="button" className="Player-btn">
                      {!play ? (
                          <PlayIcon className="Player-icon" aria-hidden="true" />
                      ) : (
                          <PauseIcon className="Player-icon" aria-hidden="true" />
                      )}
                  </button>
              </div>
              <p>Number of blobs received: {counter}</p>
              <div className="Volume">
                  <input
                      type="range"
                      min={0}
                      max={MAX_VOLUME}
                      onChange={(e) => handleVolume(e)}
                  />
                  <SpeakerWaveIcon className="Volume-icon"  />
              </div>
          </div>
          <audio ref={musicRef}>
              <source src="" type="audio/mp3"/>
          </audio>
      </div>
    </div>
  );
}

export default App;
