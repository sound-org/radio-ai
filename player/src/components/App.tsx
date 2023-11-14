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

    // Music controls
    const MAX_VOLUME = 20;
    const [volume, setVolume] = useState(MAX_VOLUME)
    const [duration, setDuration] = useState(0);
    const [currentTime, setCurrentTime] = useState(0);
    const [isPlaying, setIsPlaying] = useState<boolean>(false);
    const audioRef = useRef<HTMLAudioElement>(null);

    // Channel handling
    const [channelsInfo, setChannelsInfo] = useState<ChannelInfo[]>([]);
    const [activeChannelIdx, setActiveChannelIdx] = useState<number>(1);
    const [hlsUrl, setHlsUrl] = useState<string>("http://localhost:8080/jazz/outputlist.m3u8");
    const [thumbnailPath, setThumbnailPath] = useState<string>("/assets/thumb1.jpg");
    const [resumePlaying, setResumePlaying] = useState(false);

    const switchChannel = (newUrl: string, newIdx: number, newImgPath: string) => {
        setHlsUrl(newUrl);
        setActiveChannelIdx(newIdx);
        setThumbnailPath(newImgPath);
        setResumePlaying(true);
    }

    // HLS
    const hlsRef = useRef<Hls | null>(null);

    // HLS setup
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
                        if (resumePlaying) {
                            audioRef.current!.play();
                            setIsPlaying(true);
                            setResumePlaying(false);
                        }
                    })
                })
            })
        }
    }, [hlsUrl])

    // Radio config
    useEffect(() => {
        fetch("../radio_config.json", {
                headers : {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                }
            }).then((response) => {
                if (response.ok) {
                    return response.json();
                }
            }).then((json) => {
                const info: ChannelInfo[] = json as ChannelInfo[];
                setChannelsInfo(info);
            }
        );
    }, [])

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
                    return <Channel key={i} num={info.id} hlsPath={info.hlsPath} thumbnailPath={`/assets/thumb${info.id}.jpg`} active={activeChannelIdx === info.id} switchChannel={switchChannel} />;
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
