import './App.css';
import './Slider.css'
import Music from "../interface/Music";
import * as React from "react";
import {ReactElement, useEffect, useRef, useState} from "react";
import {PauseIcon, PlayIcon, SpeakerWaveIcon} from "@heroicons/react/24/solid";
import Hls from "hls.js";
import WaveForm from './WaveForm'
import Channel from './Channel';

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

    // Channel handling
    const [activeChannelIdx, setActiveChannelIdx] = useState<number>(1);
    const [hlsUrl, setHlsUrl] = useState<string>("http://localhost:8080/jazz/outputlist.m3u8");
    const [thumbnailPath, setThumbnailPath] = useState<string>("/assets/thumb1.jpg");

    const switchChannel = (newUrl: string, newIdx: number, newImgPath: string) => {
        setHlsUrl(newUrl);
        setActiveChannelIdx(newIdx);
        setThumbnailPath(newImgPath)
    }

    // HLS
    const hlsRef = useRef<Hls | null>(null);

    // HLS setup - call once on render
    useEffect(() => {
        if (audioRef.current) {
            hlsRef.current = new Hls();
            hlsRef.current.attachMedia(audioRef.current);
            hlsRef.current.on(Hls.Events.MEDIA_ATTACHED, () => {
                hlsRef.current?.loadSource(hlsUrl);

                hlsRef.current?.on(Hls.Events.MANIFEST_PARSED, () => {
                    hlsRef.current?.on(Hls.Events.LEVEL_LOADED, (_: string, data) => {
                        const duration = data.details.totalduration;
                        setDuration(duration);
                        setCurrentTime(0);
                        audioRef.current!.play();
                        setIsPlaying(true);
                        if (analyzerData === null) {
                            audioAnalyzer();
                        }
                    })
                })
            })
        }
    }, [hlsUrl])

    // Audio analyzer
    const [analyzerData, setAnalyzerData] = useState<any>(null);
    const audioAnalyzer = () => {
        // create a new AudioContext
        const audioCtx = new window.AudioContext();
        // create an analyzer node with a buffer size of 2048
        const analyzer = audioCtx.createAnalyser();
        analyzer.fftSize = 2048;

        const bufferLength = analyzer.frequencyBinCount;
        const dataArray = new Uint8Array(bufferLength);
        const source = new MediaElementAudioSourceNode(audioCtx, {
            mediaElement: audioRef.current!
        });
        source.connect(analyzer);
        source.connect(audioCtx.destination);

        // set the analyzerData state with the analyzer, bufferLength, and dataArray
        setAnalyzerData({ analyzer, bufferLength, dataArray });
    };

    function togglePlay(): void {
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
        audioRef.current!.volume = volume;
        setVolume(volume);
    }

    const musicBgStyle = {
        backgroundImage: `url('${thumbnailPath}')`,
        backgroundPosition: "center",
        backgroundSize: "cover",
        minWidth: "100px",
        minHeight: "100px",
        width: "50vh",
        height: "50vh",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        cursor: "pointer"
    };

    return (
        <div className="App">
            <div className="Channels">
                <Channel num={1} hlsPath="http://localhost:8080/jazz/outputlist.m3u8" thumbnailPath="/assets/thumb1.jpg" active={activeChannelIdx === 1} switchChannel={switchChannel}/>
                <Channel num={2} hlsPath="http://localhost:8080/bathroom/outputlist.m3u8" thumbnailPath="/assets/thumb2.jpg" active={activeChannelIdx === 2} switchChannel={switchChannel}/>
                <Channel num={3} hlsPath="http://localhost:8080/channel1" thumbnailPath="/assets/thumb3.jpg" active={activeChannelIdx === 3} switchChannel={switchChannel}/>
                <Channel num={4} hlsPath="" thumbnailPath="/assets/thumb4.jpg" active={activeChannelIdx === 4} switchChannel={switchChannel}/>
                <Channel num={5} hlsPath="" thumbnailPath="/assets/thumb5.jpg" active={activeChannelIdx === 5} switchChannel={switchChannel}/>
            </div>
            <div className="Radio">
                <header className="Radio-header">
                    rAIdio
                </header>
                <div className="Player">
                    <div className="Image" style={musicBgStyle} onClick={togglePlay}>
                        <button type="button" className="Player-btn">
                            {!isPlaying ? (
                                <PlayIcon className="Player-icon" aria-hidden="true"/>
                            ) : (
                                <PauseIcon className="Player-icon" aria-hidden="true"/>
                            )}
                        </button>
                    </div>
                    <div className="Analyzer">
                        {analyzerData && <WaveForm analyzerData={analyzerData}/>}
                    </div>
                    <div className="Volume">
                        <input
                            type="range"
                            min={0}
                            max={MAX_VOLUME}
                            onChange={(e) => handleVolume(e)}
                        />
                        <SpeakerWaveIcon className="Volume-icon"/>
                    </div>
                    <audio ref={audioRef}>
                        <source src="" type="audio/mp3"/>
                    </audio>
                </div>
            </div>
        </div>
    );
}

export default App;
