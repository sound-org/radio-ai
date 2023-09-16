import './App.css';
import * as React from "react";
import { ReactElement } from "react";

const App: React.FC = (): ReactElement => {

  return (
    <div className="App">
      <header className="App-header">
        App header
      </header>
      <div className="App-body">
          <p>App body</p>
          <audio controls>
              <source src="http://techslides.com/demos/samples/sample.mp3" type="audio/mp3"/>
              {/*sample-music.mp3*/}
          </audio>
      </div>
    </div>
  );
}

export default App;
