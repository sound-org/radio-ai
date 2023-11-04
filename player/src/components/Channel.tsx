import React, {useEffect, useState} from "react";

const Channel: React.FC<{num: number, hlsPath: string, active: boolean}> = (props) => {
    const [isActive, setIsActive] = useState<boolean>(false);

    useEffect(() => {
        setIsActive(props.active);
    }, [props.active])

    const handleClick = () => {
        if (!isActive) {
            setIsActive(true);
        }
    }

    return (
      <div className={isActive ? "Channel-active" : "Channel"} onClick={handleClick}>
          {props.num}
      </div>
    );
}

export default Channel;