import './App.css';
import './Slider.css'
import ChannelInfo from "../interface/ChannelInfo";
import * as React from "react";
import {ReactElement, useEffect, useRef, useState} from "react";
import {PauseIcon, PlayIcon, SpeakerWaveIcon} from "@heroicons/react/24/solid";
import Hls from "hls.js";
import WaveForm from './WaveForm'
import Channel from './Channel';

const App: React.FC = (): ReactElement => {

    // Settings
    const useLocalConfig:boolean = false;
    const serverRoot:string = "http://localhost:8080/";

    // Music controls
    const MAX_VOLUME = 20;
    const [, setVolume] = useState(MAX_VOLUME)
    const [isPlaying, setIsPlaying] = useState<boolean>(false);
    const audioRef = useRef<HTMLAudioElement>(null);

    // Channel handling
    const [channelsInfo, setChannelsInfo] = useState<ChannelInfo[]>([]);
    const [activeChannelIdx, setActiveChannelIdx] = useState<number>(1);
    const [manifestUrl, setManifestUrl] = useState<string>();
    const [thumbnailPath, setThumbnailPath] = useState<string>("/assets/thumb1.jpg");
    const [firstPlay, setFirstPlay] = useState(true);

    const switchChannel = (newUrl: string, newIdx: number, newImgPath: string) => {
        setManifestUrl(newUrl);
        console.log("Switched channel")
        setActiveChannelIdx(newIdx);
        setThumbnailPath(newImgPath);
        if (analyzerData === null) {
            audioAnalyzer();
        }
        setIsPlaying(false);
        setFirstPlay(false);
    }

    // HLS
    const hlsRef = useRef<Hls | null>(null);

    // HLS manifest change
    useEffect(() => {
        if (manifestUrl !== undefined) {
            console.log("New manifest loaded: " + serverRoot + manifestUrl)
            hlsRef.current?.loadSource(serverRoot + manifestUrl);
            if(!firstPlay) {
                togglePlay();
            }
        }
    }, [manifestUrl])

    // Radio config = run once
    useEffect(() => {
        // Fetch info
        fetch(useLocalConfig ? "../radio_config.json" : serverRoot + "info", {
                headers : {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                }
            }).then((response) => {
                if (response.ok) {
                    return response.json();
                }
            }).then((json) => {
                const info: ChannelInfo[] = json as ChannelInfo[];
                setChannelsInfo(info);
                setManifestUrl(info[0].hls_path);
                }
            ).catch(() => {
              console.error("SERVER ERROR");
        });

        // Setup HLS
        hlsRef.current = new Hls();
        if (audioRef.current) {
            hlsRef.current.attachMedia(audioRef.current);
        }
    }, []);

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
            // console.log(audioRef.current!.currentTime)
            if (audioRef.current!.currentTime > 0) {
                audioRef.current!.pause();
                setIsPlaying(false);
            }
        } else {
            audioRef.current!.play();
            setIsPlaying(true);
            if (analyzerData === null) {
                audioAnalyzer();
            }
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
    };

    return (
        <div className="App">
            <div className="Channels">
                {channelsInfo.map((info, i) => {
                    return <Channel key={i} num={info.id} hlsPath={info.hls_path} thumbnailPath={`/assets/thumb${info.id}.jpg`} active={activeChannelIdx === info.id} switchChannel={switchChannel} />;
                })}
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
                    <div className="Title">
                        {channelsInfo[activeChannelIdx-1]?.name}
                    </div>
                    <div className="Description">
                        {channelsInfo[activeChannelIdx-1]?.description}
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
