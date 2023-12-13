import React from "react";
import {useEffect, useRef} from "react";

/**
 * This function takes in the audio data, analyzes it, and generates a waveform that is visualized on a canvas element
 *
 * @param analyser analyser node from WebAudioAPI
 * @param canvas HTML canvas element
 * @param canvasCtx rendering context of the canvas
 * @param dataArray array of data that will be populated
 * @param bufferLength length of an audio buffer
 */
export function animateBars(analyser: { getByteFrequencyData: (arg0: any) => void }, canvas: HTMLCanvasElement, canvasCtx: CanvasRenderingContext2D, dataArray: number[], bufferLength: number) {
    // Analyze the audio data using the Web Audio API's `getByteFrequencyData` method.
    analyser.getByteFrequencyData(dataArray);

    // Set the canvas fill style to black.
    canvasCtx.fillStyle = '#000';

    // Calculate the height of the canvas.
    const HEIGHT = canvas.height / 2;

    // Calculate the width of each bar in the waveform based on the canvas width and the buffer length.
    var barWidth = Math.ceil(canvas.width / bufferLength) * 2.5;

    // Initialize variables for the bar height and x-position.
    let barHeight;
    let x = 0;

    // Loop through each element in the `dataArray`.
    for (let i = 0; i < bufferLength; i++) {
        barHeight = (dataArray[i] / 255) * HEIGHT;
        canvasCtx.fillStyle = 'rgb(' + 242 + ',' + 104 + ',' + 65 + ')';
        canvasCtx.fillRect(x, HEIGHT - barHeight, barWidth, barHeight);
        x += barWidth + 1;
    }
}

/**
 * This component renders an audio animation
 *
 * @param analyzerData set of objects necessary to animate {analyzer, bufferLength, dataArray}
 */
export const WaveForm = ({ analyzerData }: any) => {
    const canvasRef = useRef<HTMLCanvasElement>(null);
    const { dataArray, analyzer, bufferLength } = analyzerData;

    // Function to draw the waveform
    const draw = (dataArray: number[], analyzer: { getByteFrequencyData: (arg0: any) => void; }, bufferLength: number) => {
        const canvas = canvasRef.current;
        if (!canvas || !analyzer) return;
        const canvasCtx = canvas.getContext("2d");

        const animate = () => {
            requestAnimationFrame(animate);
            canvas.width = canvas.width;
            // @ts-ignore
            animateBars(analyzer, canvas, canvasCtx, dataArray, bufferLength);
        };

        animate();
    };

    // Effect to draw the waveform on mount and update
    useEffect(() => {
        draw(dataArray, analyzer, bufferLength);
    }, [dataArray, analyzer, bufferLength]);

    // Return the canvas element
    return (
        <canvas
            className="Canvas"
            ref={canvasRef}
        />
    );
};

export default WaveForm;