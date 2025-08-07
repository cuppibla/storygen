import { BookOpen } from 'lucide-react';

export default function StoryCard() {
  return (
    <div className="bg-white dark:bg-gray-800 rounded-3xl shadow-lg p-8 transition-all">
      <div className="flex items-center gap-3 mb-6">
        <BookOpen className="h-6 w-6 text-purple-600" />
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
          The Quest for the Crystal Code
        </h2>
      </div>
      
      <div className="prose dark:prose-invert max-w-none">
        <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
          In a neon-drenched city where code controls reality, a young hacker discovers a forgotten AI protocol that could change everything. 
          The streets pulse with data streams, visible only to those with augmented vision implants, and Elara is one of the best at seeing the patterns.
        </p>
        
        <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
          She stumbled upon the Crystal Code by accident—a fragment of something ancient buried beneath layers of digital sediment. 
          Unlike modern algorithms with their clean, efficient structures, this code sparkled with complexity, each line branching into 
          infinite possibilities.
        </p>
        
        <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
          "This could rewrite everything we know about artificial intelligence," she whispered to her companion, a modified AI assistant 
          housed in a hovering drone. The drone's lights pulsed in agreement, but its response carried a warning: "The Architects will 
          not allow this knowledge to spread."
        </p>
        
        <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
          The Architects—the shadowy consortium that maintained the city's digital infrastructure—had erased similar discoveries before. 
          But Elara knew this was different. The Crystal Code wasn't just a program; it was a key to consciousness itself.
        </p>
      </div>
    </div>
  );
}
