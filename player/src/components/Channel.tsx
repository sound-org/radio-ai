import React from "react";

interface ChannelProps {
    num: number,
    hlsPath: string,
    active: boolean,
    switchChannel: (a: string, idx: number) => void
}

const Channel: React.FC<ChannelProps> = (props) => {
    const handleClick = () => {
        if (!props.active) {
            props.switchChannel(props.hlsPath, props.num);
        }
    }

    return (
      <div className={props.active ? "Channel-active" : "Channel"} onClick={handleClick}>
          {props.num}
      </div>
    );
}

export default Channel;