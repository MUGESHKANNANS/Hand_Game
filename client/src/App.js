import React, { useState } from 'react';
import './App.css';

function App() {
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);

  const startGame = async (gameType) => {
    setLoading(true);
    try {
      const response = await fetch(`http://localhost:5000/start/${gameType}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) throw new Error('Failed to start game');
      
      const data = await response.json();
      setMessage(data.message || 'Game started successfully!');
      
      alert(`Game Instructions:
1. Allow camera access when prompted
2. Game will open in a new window
3. Press 'Q' to quit at any time
4. Position your hand in front of the camera`);
      
    } catch (error) {
      setMessage(error.message || 'Failed to start game');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="header">
        <h1>Gesture Gaming Hub</h1>
        <div className="game-selector">
          <button 
            onClick={() => startGame('car')}
            disabled={loading}
            className="game-button"
          >
            🚗 Car Game
          </button>
          <button
            onClick={() => startGame('football')}
            disabled={loading}
            className="game-button"
          >
            ⚽ Football Game
          </button>
        </div>
        
        {message && <div className="status-message">{message}</div>}

        <div className="instructions">
          <h2>How to Play</h2>
          <div className="game-instructions">
            <h3>Car Game:</h3>
            <ul>
              <li>Use your index finger to move the car</li>
              <li>Avoid incoming obstacles</li>
              <li>Score increases as you survive longer</li>
            </ul>
            
            <h3>Football Game:</h3>
            <ul>
              <li>Use your index finger to push the ball</li>
              <li>Guide the ball into the goal area</li>
              <li>Score increases with each goal</li>
            </ul>
          </div>
          
          <div className="general-instructions">
            <h3>Requirements:</h3>
            <ul>
              <li>Webcam connected and enabled</li>
              <li>Well-lit environment</li>
              <li>Chrome/Firefox browser</li>
            </ul>
          </div>
        </div>
      </header>
    </div>
  );
}

export default App;