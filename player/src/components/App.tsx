/**
 * The main application component
 *
 * @packageDocumentation
 */
import './App.css';
import './Slider.css'
import ChannelInfo from "../interface/ChannelInfo";
import * as React from "react";
import {ReactElement, useEffect, useRef, useState} from "react";
import {PauseIcon, PlayIcon, SpeakerWaveIcon} from "@heroicons/react/24/solid";
import Hls from "hls.js";
import WaveForm from './WaveForm'
import Channel from './Channel';

/**
 * Renders main application
 *
 * @param props contains one boolean flag whether to use local configuration file
 */
export const App: React.FC<{ useLocalConfig: boolean }> = (props = {useLocalConfig: false}): ReactElement => {

    // Settings
    const THUMBNAILS_COUNT = 8;
    const useLocalConfig:boolean = props.useLocalConfig;
    const serverRoot:string = "http://localhost:8080/";

    // Music controls
    const MAX_VOLUME = 30;
    const [, setVolume] = useState(MAX_VOLUME)
    const [isPlaying, setIsPlaying] = useState<boolean>(false);
    const audioRef = useRef<HTMLAudioElement>(null);
    const [manifestOK, setManifestOK] = useState<boolean>(true);

    // Channel handling
    const [channelsInfo, setChannelsInfo] = useState<ChannelInfo[]>([]);
    const [thumbnails, setThumbnails] = useState<number[]>([]);
    const [activeChannelIdx, setActiveChannelIdx] = useState<number>(1);
    const [manifestUrl, setManifestUrl] = useState<string>();
    const [thumbnailPath, setThumbnailPath] = useState<string>("");
    const [firstPlay, setFirstPlay] = useState(true);
    // Inside your component
    const manifestUrlRef = useRef(manifestUrl); // Initialize the ref with manifestUrl
    const activeChannelIdxRef = useRef(activeChannelIdx); // Initialize the ref with activeChannelIdx
    const thumbnailPathRef = useRef(thumbnailPath); // Initialize the ref with thumbnailPath
    useEffect(() => {
        // Update the ref whenever activeChannelIdx changes
        activeChannelIdxRef.current = activeChannelIdx;
    }, [activeChannelIdx]);
    useEffect(() => {
        // Update the ref whenever thumbnailPath changes
        thumbnailPathRef.current = thumbnailPath;
    }, [thumbnailPath]);

    // Update the ref whenever manifestUrl changes
    useEffect(() => {
        manifestUrlRef.current = manifestUrl;
    }, [manifestUrl]);
    /**
     * Function that allows seeding random generator in JS
     * http://davidbau.com/encode/seedrandom.js
     * License (MIT) 2014
     */
    const seedrandom = require('seedrandom');

    const switchChannel = (newUrl: any, newIdx: number, newImgPath: string) => {
        setManifestUrl(newUrl);
        console.log("Switched channel")
        setActiveChannelIdx(newIdx);
        setThumbnailPath(newImgPath);
        // if (analyzerData === null) {
        //     audioAnalyzer();
        // }
        setIsPlaying(false);
        setFirstPlay(false);
    }

    // HLS
    const hlsRef = useRef<Hls | null>(null);

    // HLS manifest change
    useEffect(() => {
        if (manifestUrl !== undefined) {
            if (manifestOK) {
                console.warn("New manifest loaded: " + serverRoot + manifestUrl)
                setManifestOK(false);
                hlsRef.current?.loadSource(serverRoot + manifestUrl);
                hlsRef.current?.attachMedia(audioRef.current!);
                if (!firstPlay) {
                    togglePlay();
                }
            } else {
                alert("You've found a bugged channel, please refresh app")
            }
        }
    }, [manifestUrl])

    // Radio config = run once
    useEffect(() => {
        console.error("manifest url___: " + manifestUrl);

        // Setup HLS
        hlsRef.current = new Hls({
            debug: true,
            enableWorker: true,
            lowLatencyMode: true,
            backBufferLength: 180 // Increase the backBufferLength to 180 seconds
        });

        hlsRef.current.on(Hls.Events.MEDIA_ATTACHED, function () {
            console.log('video and hls.js are now bound together !');
        });
        hlsRef.current.on(Hls.Events.MANIFEST_PARSED, function (event, data) {
            console.log(
                'manifest loaded, found ' + data.levels.length + ' quality level',
            );
        });
        hlsRef.current.on(Hls.Events.ERROR, function (event, data) {
            console.warn('Hls.Events.ERROR', audioRef.current?.src, data);
            // Use manifestUrlRef.current to access the current manifestUrl
            if (data.type === Hls.ErrorTypes.MEDIA_ERROR) {

                // extract channel id
                const currentChannelId = parseInt(manifestUrlRef.current?.match(/channels\/(\d)\//)?.[1] || '0', 10);
                console.log('Current Channel ID:', currentChannelId);
                // manifest url:" channels/3/streaming/manifest

                const currentManifestUrl = manifestUrlRef.current;
                const currentActiveChannelIdx = activeChannelIdxRef.current;
                const currentThumbnailPath = thumbnailPathRef.current;

                console.log('Current Manifest URL:', currentManifestUrl);

                // switchChannel(currentManifestUrl, currentActiveChannelIdx, currentThumbnailPath);
                const newChannelId = currentChannelId + 1;
                const newManifestUrl = currentManifestUrl?.replace(/(channels\/)\d+(\/streaming)/, `$1${newChannelId}$2`);
                // setManifestUrl(newManifestUrl);
                // setActiveChannelIdx(newChannelId);
                // setManifestUrl(undefined)
                // // setManifestUrl(currentManifestUrl);
                // setTimeout(() => {
                //     setManifestUrl(currentManifestUrl);
                // }, 0);
                // setActiveChannelIdx(currentActiveChannelIdx);
                // first unload any source streams
                hlsRef.current?.destroy();
                // setManifestOK(false);
                console.error("New manifest loaded: " + serverRoot + currentManifestUrl)
                hlsRef.current?.on(Hls.Events.MANIFEST_PARSED, function (event, data) {
                    hlsRef.current?.attachMedia(audioRef.current!);
                });
                hlsRef.current?.loadSource(serverRoot + currentManifestUrl);
                // hlsRef.current?.attachMedia(audioRef.current!);
                // switchChannel(newManifestUrl, newChannelId, currentThumbnailPath);

                // switchChannel(currentManifestUrl, currentActiveChannelIdx, currentThumbnailPath);
                // setIsPlaying(true);
                // audioAnalyzer();
                // setIsPlaying(false);
                // togglePlay();
            }
        });

        if (audioRef.current) {
            hlsRef.current.attachMedia(audioRef.current);
        }

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

                const initialThumbnails = [];
                for (let i = 0; i < THUMBNAILS_COUNT; i++) {
                    initialThumbnails.push(i+1);
                }

                // Randomly choose thumbnail -> different set every day
                const currentDate = new Date();
                const seed = `${currentDate.getFullYear()}${currentDate.getMonth()}${currentDate.getDate()}`;
                const rng = seedrandom(seed);
                for (let i = initialThumbnails.length - 1; i > 0; i--) {
                    let j = Math.floor(rng() * (i + 1));
                    let x: number = initialThumbnails[i];
                    initialThumbnails[i] = initialThumbnails[j];
                    initialThumbnails[j] = x;
                }
                console.log(`Using assets no.: ${initialThumbnails}`);
                setThumbnails(initialThumbnails);
                setThumbnailPath(`/assets/thumb${initialThumbnails[0]}.jpg`);
                }
            ).catch((e) => {
            console.log(e);
        });

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
            if (audioRef.current!.currentTime > 0) {
                audioRef.current!.pause();
                setIsPlaying(false);
            }
        } else {
            audioRef.current!.play().then(() => {
                // todo?
                setManifestOK(true);
            });
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

    return (
        <div className="App">
            <div className="Channels">
                {channelsInfo.map((info, i) => {
                    return <Channel key={i} num={info.id} hlsPath={info.hls_path} thumbnailPath={`/assets/thumb${thumbnails[i]}.jpg`} active={activeChannelIdx === info.id} switchChannel={switchChannel} />;
                })}
            </div>
            <div className="Radio">
                <header className="Radio-header">
                    rAIdio
                </header>
                <div className="Player">
                    <div className="Image" style={{
                        backgroundImage: `url('${thumbnailPath}')`,
                    }} onClick={togglePlay}>
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
