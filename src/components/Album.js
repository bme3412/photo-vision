'use client';

export default function Album({ album }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {album.map((item, index) => (
        <div key={index} className="bg-white rounded-lg shadow-md overflow-hidden">
          <img src={item.imageUrl} alt={`Album image ${index + 1}`} className="w-full h-48 object-cover" />
          <div className="p-4">
            <h3 className="font-bold text-lg mb-2">Generated Caption:</h3>
            <p className="text-gray-600 mb-4">{item.caption}</p>
            <h4 className="font-semibold mb-1">Image Analysis:</h4>
            <p className="text-gray-600 mb-2">{item.analysis}</p>
            <h4 className="font-semibold mb-1">EXIF Data:</h4>
            <ul className="text-sm text-gray-500">
              {Object.entries(item.exif_data).map(([key, value]) => (
                <li key={key}>{`${key}: ${value}`}</li>
              ))}
            </ul>
          </div>
        </div>
      ))}
    </div>
  );
}