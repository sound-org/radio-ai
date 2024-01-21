import React from "react";

/**
 * An interface containing the input data necessary to render a {@link Channel}
 */
export interface ChannelProps {
    /** Index of the channel */
    num: number,
    /** Path to HLS playlist */
    hlsPath: string,
    /** Path to a thumbnail image */
    thumbnailPath: string,
    /** Flag indicated whether the channel is clicked */
    active: boolean,
    /** Function to be called after clicking a channel */
    switchChannel: (a: string, idx: number, b: string) => void;
}

/**
 * A channel component
 *
 * @param props ChannelProps object
 * @returns React functional component
 */
export const Channel: React.FC<ChannelProps> = (props: ChannelProps) => {
    const handleClick = () => {
        if (!props.active) {
            console.error("Switching to channel " + props.num + "with path " + props.hlsPath);
            props.switchChannel(props.hlsPath, props.num, props.thumbnailPath);
        }
    }

    return (
      <div className={props.active ? "Channel-active" : "Channel"} onClick={handleClick} data-testid={"channel"}>
          {props.num}
      </div>
    );
}

export default Channel;
