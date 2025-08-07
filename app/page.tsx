"use client";

import { useState, useEffect } from "react";
import { Moon, Sun, Mic, MicOff } from 'lucide-react';
import { useTheme } from "next-themes";
import StoryCard from "@/components/story-card";
import ImageKeyframes from "@/components/image-keyframes";

export default function Home() {
  const [showStory, setShowStory] = useState(false);
  const { theme, setTheme } = useTheme();
  const [keywords, setKeywords] = useState("");
  const [isListening, setIsListening] = useState(false);
  const [recognition, setRecognition] = useState<SpeechRecognition | null>(null);

  useEffect(() => {
    if (typeof window !== 'undefined' && 'webkitSpeechRecognition' in window) {
      const SpeechRecognition = window.webkitSpeechRecognition || window.SpeechRecognition;
      const recognitionInstance = new SpeechRecognition();
      
      recognitionInstance.continuous = false;
      recognitionInstance.interimResults = false;
      recognitionInstance.lang = 'en-US';
      
      recognitionInstance.onstart = () => {
        setIsListening(true);
      };
      
      recognitionInstance.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        setKeywords(prev => prev + (prev ? ' ' : '') + transcript);
      };
      
      recognitionInstance.onend = () => {
        setIsListening(false);
      };
      
      recognitionInstance.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
        setIsListening(false);
      };
      
      setRecognition(recognitionInstance);
    }
  }, []);

  const handleGenerateStory = () => {
    setShowStory(true);
  };

  const handleVoiceInput = () => {
    if (!recognition) {
      alert('Speech recognition is not supported in your browser');
      return;
    }
    
    if (isListening) {
      recognition.stop();
    } else {
      recognition.start();
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center px-4 py-8 md:py-16">
      {/* Dark Mode Toggle */}
      <div className="absolute top-4 right-4">
        <button
          onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
          className="p-2 rounded-full bg-gray-100 dark:bg-gray-800 transition-colors"
          aria-label="Toggle theme"
        >
          {theme === "dark" ? (
            <Sun className="h-5 w-5 text-yellow-500" />
          ) : (
            <Moon className="h-5 w-5 text-gray-700" />
          )}
        </button>
      </div>

      {/* Hero Section */}
      <div className="w-full max-w-3xl mx-auto text-center space-y-8 mb-12">
        <h1 className="text-4xl md:text-5xl font-bold tracking-tight text-gray-900 dark:text-white">
          StoryGen
        </h1>
        <p className="text-xl text-gray-600 dark:text-gray-300">
          Enter keywords to generate a captivating story
        </p>
        
        <div className="flex flex-col md:flex-row gap-3 w-full max-w-2xl mx-auto">
          <div className="flex-1 relative">
            <input
              type="text"
              value={keywords}
              onChange={(e) => setKeywords(e.target.value)}
              placeholder="Enter keywords (e.g., hacker, AI, future)"
              className="w-full px-6 py-4 pr-14 text-lg rounded-2xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 shadow-sm focus:outline-none focus:ring-2 focus:ring-purple-500 dark:text-white"
            />
            <button
              onClick={handleVoiceInput}
              className={`absolute right-3 top-1/2 transform -translate-y-1/2 p-2 rounded-full transition-colors ${
                isListening 
                  ? 'bg-red-100 text-red-600 dark:bg-red-900 dark:text-red-400' 
                  : 'bg-gray-100 text-gray-600 dark:bg-gray-700 dark:text-gray-400 hover:bg-gray-200 dark:hover:bg-gray-600'
              }`}
              aria-label={isListening ? 'Stop recording' : 'Start voice input'}
            >
              {isListening ? (
                <MicOff className="h-5 w-5" />
              ) : (
                <Mic className="h-5 w-5" />
              )}
            </button>
          </div>
          <button
            onClick={handleGenerateStory}
            className="px-8 py-4 text-lg font-medium text-white bg-purple-600 rounded-2xl hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2 transition-colors shadow-md"
          >
            Generate Story
          </button>
        </div>
      </div>

      {/* Story Display */}
      {showStory && (
        <div className="w-full max-w-3xl mx-auto space-y-12 animate-fade-in">
          <StoryCard />
          <ImageKeyframes />
        </div>
      )}
    </div>
  );
}
