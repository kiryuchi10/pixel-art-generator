import PixelArtGenerator from './components/PixelArtGenerator';
import './tailwind.output.css';

function App() {
  return (
    <div className="min-h-screen p-8 bg-gray-100">
      <h1 className="text-3xl font-bold">AI Pixel Art Generator</h1>
      <PixelArtGenerator />
    </div>
  );
}
export default App;
