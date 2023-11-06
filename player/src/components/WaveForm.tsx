// This function takes in the audio data, analyzes it, and generates a waveform
// that is visualized on a canvas element.
import React from "react";
import {useEffect, useRef} from "react";

function animateBars(analyser: { getByteFrequencyData: (arg0: any) => void }, canvas: HTMLCanvasElement, canvasCtx: CanvasRenderingContext2D, dataArray: number[], bufferLength: number) {
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

    // let r = Math.floor(Math.random() * 255)
    // let g = Math.floor(Math.random() * 255)
    // let b = Math.floor(Math.random() * 255)

    // Loop through each element in the `dataArray`.
    for (let i = 0; i < bufferLength; i++) {
        // Calculate the height of the current bar based on the audio data and the canvas height.
        barHeight = (dataArray[i] / 255) * HEIGHT;

        // Set the canvas fill style to the random RGB values.
        canvasCtx.fillStyle = 'rgb(' + 242 + ',' + 104 + ',' + 65 + ')';

        // Draw the bar on the canvas at the current x-position and with the calculated height and width.
        canvasCtx.fillRect(x, HEIGHT - barHeight, barWidth, barHeight);

        // Update the x-position for the next bar.
        x += barWidth + 1;
    }
}

// Component to render the waveform
const WaveForm = ({ analyzerData }: any) => {
    // Ref for the canvas element
    const canvasRef = useRef<HTMLCanvasElement>(null);
    const { dataArray, analyzer, bufferLength } = analyzerData;

    // Function to draw the waveform
    const draw = (dataArray: number[], analyzer: { getByteFrequencyData: (arg0: any) => void; }, bufferLength: number) => {
        const canvas = canvasRef.current;
        if (!canvas || !analyzer) return;
        const canvasCtx = canvas.getContext("2d");

        const animate = () => {
            requestAnimationFrame(animate);
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