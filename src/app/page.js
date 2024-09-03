'use client';

import { useState } from 'react';
import ImageUploader from '@/components/ImageUploader';
import Album from '@/components/Album';

export default function Home() {
  const [album, setAlbum] = useState([]);
  const [showAlbum, setShowAlbum] = useState(false);

  const addToAlbum = (imageData) => {
    setAlbum([...album, imageData]);
  };

  return (
    <main className="min-h-screen bg-gray-100">
      <nav className="bg-white shadow-md">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex-shrink-0 flex items-center">
              <h1 className="text-2xl font-bold text-gray-800">Photo Vision</h1>
            </div>
            <div className="flex items-center">
              <ImageUploader addToAlbum={addToAlbum} />
              <button 
                onClick={() => setShowAlbum(!showAlbum)}
                className="ml-4 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition duration-300"
              >
                Album
              </button>
            </div>
          </div>
        </div>
      </nav>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {showAlbum ? <Album album={album} /> : <p className="text-center text-gray-600">Upload an image to get started!</p>}
      </div>
    </main>
  );
}