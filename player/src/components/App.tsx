import './App.css';
import './Slider.css'
import Music from "../interface/Music";
import * as React from "react";
import {ReactElement, useEffect, useRef, useState} from "react";
import {PauseIcon, PlayIcon, SpeakerWaveIcon} from "@heroicons/react/24/solid";
import Hls from "hls.js";
import WaveForm from './WaveForm';

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
    const [volume, setVolume] = useState(MAX_VOLUME)
    const [duration, setDuration] = useState(0);
    const [currentTime, setCurrentTime] = useState(0);
    const [isPlaying, setIsPlaying] = useState<boolean>(false);
    const audioRef = useRef<HTMLAudioElement>(null);

    // HLS
    const hlsSource = "http://localhost:8080/bathroom/outputlist.m3u8";
    const hlsRef = useRef<Hls | null>(null);

    // HLS setup - call once on render
    useEffect(() => {
        if (audioRef.current) {
            hlsRef.current = new Hls();
            hlsRef.current.attachMedia(audioRef.current);
            hlsRef.current.on(Hls.Events.MEDIA_ATTACHED, () => {
                hlsRef.current.loadSource(hlsSource);

                hlsRef.current.on(Hls.Events.MANIFEST_PARSED, () => {
                    hlsRef.current.on(Hls.Events.LEVEL_LOADED, (_: string, data) => {
                        const duration = data.details.totalduration;
                        setDuration(duration);
                        setCurrentTime(0);
                        // audioRef.current.play();
                        // setIsPlaying(true);
                    })
                })
            })
        }
    }, [])

    // Audio analyzer
    const [analyzerData, setAnalyzerData] = useState(null);
    const audioAnalyzer = () => {
        // create a new AudioContext
        const audioCtx = new window.AudioContext();
        // create an analyzer node with a buffer size of 2048
        const analyzer = audioCtx.createAnalyser();
        analyzer.fftSize = 2048;

        const bufferLength = analyzer.frequencyBinCount;
        const dataArray = new Uint8Array(bufferLength);
        const source = new MediaElementAudioSourceNode(audioCtx, {
            mediaElement: audioRef.current
        });
        source.connect(analyzer);
        source.connect(audioCtx.destination);

        // set the analyzerData state with the analyzer, bufferLength, and dataArray
        setAnalyzerData({ analyzer, bufferLength, dataArray });
    };


    function togglePlay(): void {
        if (analyzerData === null) {
            audioAnalyzer();
        }
        if (isPlaying) {
            audioRef.current!.pause();
            setIsPlaying(false);
        } else {
            audioRef.current!.play();
            setIsPlaying(true);
        }
    }

    function handleVolume(e: React.ChangeEvent<HTMLInputElement>): void {
        const { value } = e.target;
        const volume = Number(value) / MAX_VOLUME;
        audioRef.current.volume = volume;
        setVolume(volume);
    }

    return (
    <div className="App">
      <header className="App-header">
        rAIdio
      </header>
      <div className="App-body">
          <div className="Player">
              <div className="Player-image" onClick={togglePlay}>
                  <img src={music.image} className="Player-img" alt="Song thumbnail"/>
                  <button type="button" className="Player-btn">
                      {!isPlaying ? (
                          <PlayIcon className="Player-icon" aria-hidden="true" />
                      ) : (
                          <PauseIcon className="Player-icon" aria-hidden="true" />
                      )}
                  </button>
              </div>
              <div className="Analyzer">
                  {analyzerData && <WaveForm analyzerData={analyzerData}/>}
              </div>
              <p>Duration: {Math.round(duration)} s</p>
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
          <audio ref={audioRef}>
              <source src="" type="audio/mp3" />
          </audio>
      </div>
    </div>
  );
}

export default App;
