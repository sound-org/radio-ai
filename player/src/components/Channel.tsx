import React from "react";

interface ChannelProps {
    num: number,
    hlsPath: string,
    thumbnailPath: string,
    active: boolean,
    switchChannel: (a: string, idx: number, b: string) => void
}

const Channel: React.FC<ChannelProps> = (props) => {
    const handleClick = () => {
        if (!props.active) {
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