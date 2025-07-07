// src/components/PixelArtGenerator.jsx
import React, { useState, useEffect, useRef } from 'react';
import { Upload, Download, Settings, Palette, Zap, Image as ImageIcon, Type } from 'lucide-react';
import io from 'socket.io-client';

const PixelArtGenerator = () => {
    const [activeTab, setActiveTab] = useState('text');
    const [inputText, setInputText] = useState('');
    const [uploadedImage, setUploadedImage] = useState(null);
    const [selectedStyle, setSelectedStyle] = useState('8bit');
    const [resolution, setResolution] = useState('32x32');
    const [colorPalette, setColorPalette] = useState('classic');
    const [generationStatus, setGenerationStatus] = useState('idle');
    const [generatedImage, setGeneratedImage] = useState(null);
    const [progress, setProgress] = useState(0);
    const [jobId, setJobId] = useState(null);
    const [error, setError] = useState(null);
    const [history, setHistory] = useState([]);
    const [batchCount, setBatchCount] = useState(1);
    const [previewStages, setPreviewStages] = useState([]);
    
    const socketRef = useRef(null);
    const fileInputRef = useRef(null);

    // Socket connection for real-time updates
    useEffect(() => {
        if (jobId) {
            socketRef.current = io('http://localhost:8000');
            
            socketRef.current.on('connect', () => {
                socketRef.current.emit('join_room', jobId);
            });
            
            socketRef.current.on('generation_progress', (data) => {
                setProgress(data.progress);
                if (data.stage_image) {
                    setPreviewStages(prev => [...prev, data.stage_image]);
                }
            });
            
            socketRef.current.on('generation_complete', (data) => {
                setGenerationStatus('completed');
                setGeneratedImage(data.image_url);
                setProgress(100);
            });
            
            socketRef.current.on('generation_error', (data) => {
                setGenerationStatus('error');
                setError(data.error);
            });
            
            return () => {
                if (socketRef.current) {
                    socketRef.current.disconnect();
                }
            };
        }
    }, [jobId]);

    // Handle text-to-pixel art generation
    const handleTextGeneration = async () => {
        if (!inputText.trim()) {
            setError('Please enter a description');
            return;
        }
        
        setGenerationStatus('generating');
        setError(null);
        setProgress(0);
        setPreviewStages([]);
        
        try {
            const response = await fetch('/api/generate/text', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    text: inputText,
                    style: selectedStyle,
                    resolution: resolution,
                    color_palette: colorPalette,
                    batch_count: batchCount
                })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                setJobId(data.job_id);
            } else {
                setError(data.error || 'Generation failed');
                setGenerationStatus('error');
            }
        } catch (err) {
            setError('Network error occurred');
            setGenerationStatus('error');
        }
    };

    // Handle image-to-pixel art generation
    const handleImageGeneration = async () => {
        if (!uploadedImage) {
            setError('Please upload an image');
            return;
        }
        
        setGenerationStatus('generating');
        setError(null);
        setProgress(0);
        setPreviewStages([]);
        
        const formData = new FormData();
        formData.append('image', uploadedImage);
        formData.append('style', selectedStyle);
        formData.append('resolution', resolution);
        formData.append('color_palette', colorPalette);
        formData.append('batch_count', batchCount);
        
        try {
            const response = await fetch('/api/generate/image', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            if (response.ok) {
                setJobId(data.job_id);
            } else {
                setError(data.error || 'Generation failed');
                setGenerationStatus('error');
            }
        } catch (err) {
            setError('Network error occurred');
            setGenerationStatus('error');
        }
    };

    // Handle file upload
    const handleFileUpload = (event) => {
        const file = event.target.files[0];
        if (file) {
            if (file.type.startsWith('image/')) {
                setUploadedImage(file);
                setError(null);
            } else {
                setError('Please upload a valid image file');
            }
        }
    };

    // Handle export
    const handleExport = async (format = 'png') => {
        if (!generatedImage) return;
        
        try {
            const response = await fetch('/api/export', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    image_url: generatedImage,
                    format: format
                })
            });
            
            const blob = await response.blob();
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `pixel-art-${Date.now()}.${format}`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        } catch (err) {
            setError('Export failed');
        }
    };

    // Load generation history
    useEffect(() => {
        const loadHistory = async () => {
            try {
                const response = await fetch('/api/history');
                const data = await response.json();
                setHistory(data.generations || []);
            } catch (err) {
                console.error('Failed to load history:', err);
            }
        };
        
        loadHistory();
    }, []);

    const styles = [
        { id: '8bit', name: '8-Bit Classic', description: 'Retro NES-style pixel art' },
        { id: '16bit', name: '16-Bit', description: 'SNES-era detailed sprites' },
        { id: 'gameboy', name: 'Game Boy', description: 'Monochrome green palette' },
        { id: 'modern', name: 'Modern Pixel', description: 'High-res pixel art style' }
    ];

    const resolutions = ['16x16', '32x32', '64x64', '128x128'];
    const colorPalettes = [
        { id: 'classic', name: 'Classic', colors: 16 },
        { id: 'gameboy', name: 'Game Boy', colors: 4 },
        { id: 'nes', name: 'NES', colors: 56 },
        { id: 'custom', name: 'Custom', colors: 'Variable' }
    ];

    return (
        <div className="max-w-7xl mx-auto p-6 bg-gray-900 text-white min-h-screen">
            <div className="mb-8">
                <h1 className="text-4xl font-bold text-center mb-2 bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
                    AI Pixel Art Generator
                </h1>
                <p className="text-center text-gray-400">
                    Transform text descriptions and images into stunning pixel art
                </p>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Input Section */}
                <div className="lg:col-span-1 space-y-6">
                    {/* Tab Selection */}
                    <div className="flex bg-gray-800 rounded-lg p-1">
                        <button
                            className={`flex-1 flex items-center justify-center gap-2 py-2 px-4 rounded-md transition-colors ${
                                activeTab === 'text' ? 'bg-purple-600' : 'hover:bg-gray-700'
                            }`}
                            onClick={() => setActiveTab('text')}
                        >
                            <Type size={16} />
                            Text
                        </button>
                        <button
                            className={`flex-1 flex items-center justify-center gap-2 py-2 px-4 rounded-md transition-colors ${
                                activeTab === 'image' ? 'bg-purple-600' : 'hover:bg-gray-700'
                            }`}
                            onClick={() => setActiveTab('image')}
                        >
                            <ImageIcon size={16} />
                            Image
                        </button>
                    </div>

                    {/* Input Area */}
                    {activeTab === 'text' ? (
                        <div className="space-y-4">
                            <div>
                                <label className="block text-sm font-medium text-gray-300 mb-2">
                                    Describe your pixel art
                                </label>
                                <textarea
                                    value={inputText}
                                    onChange={(e) => setInputText(e.target.value)}
                                    placeholder="e.g., A brave knight with a sword and shield, standing in front of a castle..."
                                    className="w-full h-32 bg-gray-800 border border-gray-600 rounded-lg p-3 text-white placeholder-gray-400 focus:border-purple-500 focus:outline-none resize-none"
                                />
                            </div>
                        </div>
                    ) : (
                        <div className="space-y-4">
                            <div>
                                <label className="block text-sm font-medium text-gray-300 mb-2">
                                    Upload image
                                </label>
                                <div
                                    className="border-2 border-dashed border-gray-600 rounded-lg p-8 text-center cursor-pointer hover:border-purple-500 transition-colors"
                                    onClick={() => fileInputRef.current?.click()}
                                >
                                    <Upload className="mx-auto mb-2 text-gray-400" size={24} />
                                    <p className="text-gray-400">Click to upload or drag and drop</p>
                                    <p className="text-sm text-gray-500">PNG, JPG, GIF up to 10MB</p>
                                </div>
                                <input
                                    ref={fileInputRef}
                                    type="file"
                                    accept="image/*"
                                    onChange={handleFileUpload}
                                    className="hidden"
                                />
                                {uploadedImage && (
                                    <div className="mt-2 text-sm text-green-400">
                                        Selected: {uploadedImage.name}
                                    </div>
                                )}
                            </div>
                        </div>
                    )}

                    {/* Style Selection */}
                    <div>
                        <label className="block text-sm font-medium text-gray-300 mb-2">
                            Art Style
                        </label>
                        <div className="grid grid-cols-1 gap-2">
                            {styles.map((style) => (
                                <button
                                    key={style.id}
                                    className={`p-3 rounded-lg border text-left transition-colors ${
                                        selectedStyle === style.id
                                            ? 'border-purple-500 bg-purple-500/10'
                                            : 'border-gray-600 hover:border-gray-500'
                                    }`}
                                    onClick={() => setSelectedStyle(style.id)}
                                >
                                    <div className="font-medium">{style.name}</div>
                                    <div className="text-sm text-gray-400">{style.description}</div>
                                </button>
                            ))}
                        </div>
                    </div>

                    {/* Settings */}
                    <div className="space-y-4">
                        <div>
                            <label className="block text-sm font-medium text-gray-300 mb-2">
                                Resolution
                            </label>
                            <select
                                value={resolution}
                                onChange={(e) => setResolution(e.target.value)}
                                className="w-full bg-gray-800 border border-gray-600 rounded-lg p-2 text-white focus:border-purple-500 focus:outline-none"
                            >
                                {resolutions.map((res) => (
                                    <option key={res} value={res}>{res}</option>
                                ))}
                            </select>
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-gray-300 mb-2">
                                Color Palette
                            </label>
                            <select
                                value={colorPalette}
                                onChange={(e) => setColorPalette(e.target.value)}
                                className="w-full bg-gray-800 border border-gray-600 rounded-lg p-2 text-white focus:border-purple-500 focus:outline-none"
                            >
                                {colorPalettes.map((palette) => (
                                    <option key={palette.id} value={palette.id}>
                                        {palette.name} ({palette.colors} colors)
                                    </option>
                                ))}
                            </select>
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-gray-300 mb-2">
                                Batch Count
                            </label>
                            <input
                                type="number"
                                min="1"
                                max="10"
                                value={batchCount}
                                onChange={(e) => setBatchCount(parseInt(e.target.value))}
                                className="w-full bg-gray-800 border border-gray-600 rounded-lg p-2 text-white focus:border-purple-500 focus:outline-none"
                            />
                        </div>
                    </div>

                    {/* Generate Button */}
                    <button
                        onClick={activeTab === 'text' ? handleTextGeneration : handleImageGeneration}
                        disabled={generationStatus === 'generating'}
                        className="w-full bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 disabled:from-gray-600 disabled:to-gray-600 py-3 rounded-lg font-medium transition-all duration-200 flex items-center justify-center gap-2"
                    >
                        {generationStatus === 'generating' ? (
                            <>
                                <div className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent"></div>
                                Generating...
                            </>
                        ) : (
                            <>
                                <Zap size={16} />
                                Generate Pixel Art
                            </>
                        )}
                    </button>
                </div>

                {/* Preview Section */}
                <div className="lg:col-span-2 space-y-6">
                    {/* Progress Bar */}
                    {generationStatus === 'generating' && (
                        <div className="bg-gray-800 rounded-lg p-4">
                            <div className="flex justify-between items-center mb-2">
                                <span className="text-sm font-medium">Generation Progress</span>
                                <span className="text-sm text-gray-400">{progress}%</span>
                            </div>
                            <div className="w-full bg-gray-700 rounded-full h-2">
                                <div
                                    className="bg-gradient-to-r from-purple-600 to-pink-600 h-2 rounded-full transition-all duration-300"
                                    style={{ width: `${progress}%` }}
                                ></div>
                            </div>
                        </div>
                    )}

                    {/* Error Display */}
                    {error && (
                        <div className="bg-red-900/50 border border-red-500 rounded-lg p-4">
                            <div className="text-red-200">{error}</div>
                        </div>
                    )}

                    {/* Real-time Preview Stages */}
                    {previewStages.length > 0 && (
                        <div className="bg-gray-800 rounded-lg p-4">
                            <h3 className="text-lg font-medium mb-3">Generation Stages</h3>
                            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                                {previewStages.map((stage, index) => (
                                    <div key={index} className="bg-gray-700 rounded-lg p-2">
                                        <img
                                            src={stage}
                                            alt={`Stage ${index + 1}`}
                                            className="w-full h-auto rounded pixelated"
                                        />
                                        <div className="text-xs text-gray-400 mt-1 text-center">
                                            Stage {index + 1}
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}

                    {/* Generated Result */}
                    {generatedImage && (
                        <div className="bg-gray-800 rounded-lg p-6">
                            <div className="flex justify-between items-center mb-4">
                                <h3 className="text-lg font-medium">Generated Pixel Art</h3>
                                <div className="flex gap-2">
                                    <button
                                        onClick={() => handleExport('png')}
                                        className="bg-green-600 hover:bg-green-700 px-4 py-2 rounded-lg flex items-center gap-2 transition-colors"
                                    >
                                        <Download size={16} />
                                        PNG
                                    </button>
                                    <button
                                        onClick={() => handleExport('svg')}
                                        className="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-lg flex items-center gap-2 transition-colors"
                                    >
                                        <Download size={16} />
                                        SVG
                                    </button>
                                </div>
                            </div>
                            <div className="bg-gray-700 rounded-lg p-4 text-center">
                                <img
                                    src={generatedImage}
                                    alt="Generated pixel art"
                                    className="max-w-full h-auto mx-auto pixelated"
                                    style={{ imageRendering: 'pixelated' }}
                                />
                            </div>
                        </div>
                    )}

                    {/* Generation History */}
                    {history.length > 0 && (
                        <div className="bg-gray-800 rounded-lg p-6">
                            <h3 className="text-lg font-medium mb-4">Recent Generations</h3>
                            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                                {history.slice(0, 8).map((item, index) => (
                                    <div key={index} className="bg-gray-700 rounded-lg p-2 cursor-pointer hover:bg-gray-600 transition-colors">
                                        <img
                                            src={item.output_image_url}
                                            alt="Previous generation"
                                            className="w-full h-auto rounded pixelated"
                                        />
                                        <div className="text-xs text-gray-400 mt-1 truncate">
                                            {item.input_text || 'Image upload'}
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default PixelArtGenerator;