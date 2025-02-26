import React, { useState, FormEvent } from 'react';

// Optional: Add a custom fadeIn animation to your tailwind.config.js
// module.exports = {
//   theme: {
//     extend: {
//       keyframes: {
//         fadeIn: {
//           '0%': { opacity: 0 },
//           '100%': { opacity: 1 },
//         },
//       },
//       animation: {
//         fadeIn: 'fadeIn 0.5s ease-out',
//       },
//     },
//   },
//   plugins: [],
// };

const Header: React.FC = () => (
  <header className="bg-gray-800 text-white p-4 flex items-center justify-between">
    <h1 className="text-2xl font-bold flex items-center">
      <span className="inline-block w-6 h-6 mr-2">
        <svg
          viewBox="0 0 24 24"
          fill="currentColor"
          className="w-6 h-6 text-yellow-400"
          aria-hidden="true"
        >
          <path d="M2 22l1-6.414 2.94 2.94zM22 2l-9.071 9.071 2.946 2.946 9.07-9.07z" />
        </svg>
      </span>
      RulesLawyer
    </h1>
  </header>
);

interface SidebarProps {
  history: string[];
}

const Sidebar: React.FC<SidebarProps> = ({ history }) => (
  <aside className="hidden md:flex md:flex-col w-64 bg-gray-200 border-r border-gray-300 p-4 overflow-y-auto">
    <h2 className="text-lg font-semibold mb-2">History</h2>
    {history.length === 0 ? (
      <p className="text-sm italic text-gray-600">No recent queries</p>
    ) : (
      <ul className="space-y-1">
        {history.map((item, index) => (
          <li key={index} className="text-sm py-1 px-2 bg-white rounded shadow">
            {item}
          </li>
        ))}
      </ul>
    )}
  </aside>
);

interface SearchBarProps {
  userPrompt: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  onSubmit: (e: FormEvent) => void;
  loading: boolean;
}

const SearchBar: React.FC<SearchBarProps> = ({
  userPrompt,
  onChange,
  onSubmit,
  loading,
}) => (
  <form
    onSubmit={onSubmit}
    className="flex items-center space-x-2 border-b border-gray-400 pb-2"
  >
    <input
      type="text"
      value={userPrompt}
      onChange={onChange}
      placeholder="Ask a rules question (e.g. 'How does flanking work?')"
      className="flex-1 px-4 py-2 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400"
      aria-label="Rules question"
    />
    <button
      type="submit"
      disabled={!userPrompt.trim() || loading}
      className={`bg-blue-600 text-white px-4 py-2 rounded-md transition-colors focus:outline-none focus:ring-2 focus:ring-blue-400 ${
        !userPrompt.trim() || loading
          ? 'opacity-50 cursor-not-allowed'
          : 'hover:bg-blue-700'
      }`}
    >
      Ask
    </button>
  </form>
);

interface AnswerDisplayProps {
  answer: string;
}

const AnswerDisplay: React.FC<AnswerDisplayProps> = ({ answer }) => (
  <div className="bg-white p-4 rounded-md shadow animate-fadeIn">
    <h3 className="text-xl font-semibold mb-2">Answer</h3>
    <p className="text-gray-800 whitespace-pre-wrap">{answer}</p>
  </div>
);

const Footer: React.FC = () => (
  <footer className="bg-gray-800 text-white text-center p-2">
    <small>&copy; {new Date().getFullYear()} GPT DUNGEON MASTER. All rights reserved.</small>
  </footer>
);

const RulesLawyerPage: React.FC = () => {
  const [userPrompt, setUserPrompt] = useState('');
  const [answer, setAnswer] = useState('');
  const [history, setHistory] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!userPrompt.trim()) return;

    setLoading(true);
    setError('');
    setAnswer('');

    try {
      const response = await fetch('http://localhost:8001/rules', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_prompt: userPrompt }),
      });
// 
      if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Error fetching data');
      }
// 
      const data = await response.json();
 
      setAnswer(data.answer ?? 'No answer found.');
      setHistory((prev) => [...prev, userPrompt]);
    } catch (err: unknown) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError('An unknown error occurred.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gradient-to-b from-gray-50 to-gray-300 text-gray-900">
      <Header />
      <div className="flex flex-1 overflow-hidden">
        <Sidebar history={history} />
        <main className="flex-1 flex flex-col p-4 space-y-4">
          <SearchBar
            userPrompt={userPrompt}
            onChange={(e) => setUserPrompt(e.target.value)}
            onSubmit={handleSubmit}
            loading={loading}
          />
          {loading && (
            <div className="flex items-center space-x-2 text-gray-700">
              <svg
                className="animate-spin h-5 w-5 text-blue-600"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                aria-hidden="true"
              >
                <circle
                  className="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  strokeWidth="4"
                />
                <path
                  className="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8v8H4z"
                />
              </svg>
              <span className="text-sm">Consulting the ancient tomes...</span>
            </div>
          )}
          {error && (
            <div className="text-red-600" role="alert">
              <strong>Error:</strong> {error}
            </div>
          )}
          {answer && !loading && !error && <AnswerDisplay answer={answer} />}
        </main>
      </div>
      <Footer />
    </div>
  );
};

export default RulesLawyerPage;
