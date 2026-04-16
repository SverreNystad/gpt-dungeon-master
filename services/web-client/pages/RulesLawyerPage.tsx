import React, { useState, useEffect, FormEvent } from 'react';

/**
 * A single-page UI for the RulesLawyer tool.
 * - Allows users to input a rules query
 * - Fetches results from the FastAPI endpoint `/rules`
 * - Displays the answer and keeps a local history of recent queries
 */
const RulesLawyerPage: React.FC = () => {
  // --------------------------
  // State
  // --------------------------
  const [userPrompt, setUserPrompt] = useState('');
  const [answer, setAnswer] = useState('');
  const [history, setHistory] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // --------------------------
  // Handlers
  // --------------------------
  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!userPrompt.trim()) return;

    setLoading(true);
    setError('');
    setAnswer('');

    try {
      const response = await fetch('http://localhost:8000/rules', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_prompt: userPrompt }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Error fetching data');
      }

      // Backend is expected to return a JSON structure, e.g. { answer: string, ... }
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

  // --------------------------
  // UI Markup
  // --------------------------
  return (
    <div className="flex flex-col h-screen bg-gradient-to-b from-gray-100 to-gray-300 text-gray-900">
      {/* HEADER */}
      <header className="bg-gray-800 text-white p-4 flex items-center justify-between">
        <h1 className="text-2xl font-bold flex items-center">
          <span className="inline-block w-6 h-6 mr-2">
            {/* Simple fantasy-inspired icon (e.g., a quill) */}
            <svg
              viewBox="0 0 24 24"
              fill="currentColor"
              className="w-6 h-6 text-yellow-400"
            >
              <path d="M2 22l1-6.414 2.94 2.94zM22 2l-9.071 9.071 2.946 2.946 9.07-9.07z" />
            </svg>
          </span>
          RulesLawyer
        </h1>
        {/* Could add nav items or settings here if needed */}
      </header>

      {/* MAIN CONTENT AREA */}
      <div className="flex flex-1 overflow-hidden">
        {/* SIDEBAR (History) */}
        <aside className="hidden md:flex md:flex-col w-64 bg-gray-200 border-r border-gray-300 p-4 overflow-y-auto">
          <h2 className="text-lg font-semibold mb-2">History</h2>
          {history.length === 0 ? (
            <p className="text-sm italic text-gray-600">No recent queries</p>
          ) : (
            <ul className="space-y-1">
              {history.map((item, index) => (
                <li
                  key={index}
                  className="text-sm py-1 px-2 bg-white rounded shadow cursor-default"
                >
                  {item}
                </li>
              ))}
            </ul>
          )}
        </aside>

        {/* MAIN PANEL */}
        <div className="flex-1 flex flex-col p-4 space-y-4">
          {/* SEARCH BAR */}
          <form
            onSubmit={handleSubmit}
            className="flex items-center space-x-2 border-b border-gray-400 pb-2"
          >
            <input
              type="text"
              value={userPrompt}
              onChange={(e) => setUserPrompt(e.target.value)}
              placeholder="Ask a rules question (e.g. 'How does flanking work?')"
              className="flex-1 px-4 py-2 rounded-md focus:outline-none"
            />
            <button
              type="submit"
              className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors"
            >
              Ask
            </button>
          </form>

          {/* STATUS DISPLAY */}
          {loading && (
            <div className="flex items-center space-x-2 text-gray-700">
              <svg
                className="animate-spin h-5 w-5 text-blue-600"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
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
            <div className="text-red-600">
              <strong>Error:</strong> {error}
            </div>
          )}

          {/* ANSWER DISPLAY */}
          {answer && !loading && !error && (
            <div className="bg-white p-4 rounded-md shadow">
              <h3 className="text-xl font-semibold mb-2">Answer</h3>
              <p className="text-gray-800 whitespace-pre-wrap">{answer}</p>
            </div>
          )}
        </div>
      </div>

      {/* FOOTER */}
      <footer className="bg-gray-800 text-white text-center p-2">
        <small>
          &copy; {new Date().getFullYear()} RulesLawyer. All rights reserved.
        </small>
      </footer>
    </div>
  );
};

export default RulesLawyerPage;
