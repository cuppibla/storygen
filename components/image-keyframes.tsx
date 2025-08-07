export default function ImageKeyframes() {
  const keyframes = [
    { id: 1, title: "Neon City" },
    { id: 2, title: "The Discovery" },
    { id: 3, title: "Crystal Code" },
    { id: 4, title: "The Architects" },
  ];

  return (
    <div className="space-y-4">
      <h3 className="text-xl font-semibold text-gray-800 dark:text-gray-200">
        Story Keyframes
      </h3>
      
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {keyframes.map((frame) => (
          <div 
            key={frame.id}
            className="aspect-video bg-gray-200 dark:bg-gray-700 rounded-xl flex items-center justify-center shadow-md overflow-hidden"
          >
            <div className="text-center p-4">
              <p className="font-medium text-gray-600 dark:text-gray-300">
                {frame.title}
              </p>
              <p className="text-sm text-gray-500 dark:text-gray-400">
                Image {frame.id}
              </p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
