import React, { useState } from 'react';
import axios from 'axios';

const PixelArtGenerator = () => {
  const [inputText, setInputText] = useState('');
  const [style, setStyle] = useState('8bit');
  const [resolution, setResolution] = useState('32x32');
  const [status, setStatus] = useState('');

  const generateArt = async () => {
    setStatus('Generating...');
    const res = await axios.post('http://localhost:5000/api/generate/text', {
      text: inputText,
      style,
      resolution
    });
    setStatus(`Submitted. Job ID: ${res.data.jobId}`);
  };

  return (
    <div className="p-4 bg-white rounded shadow mt-4">
      <input
        className="w-full p-2 border"
        placeholder="Enter description"
        value={inputText}
        onChange={(e) => setInputText(e.target.value)}
      />
      <button className="mt-2 bg-blue-500 text-white px-4 py-2" onClick={generateArt}>
        Generate Pixel Art
      </button>
      <p className="mt-2 text-sm text-gray-600">{status}</p>
    </div>
  );
};

export default PixelArtGenerator;
