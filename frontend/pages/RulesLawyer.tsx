import React, { useState, FormEvent } from "react";

interface RuleResponse {
  // Adjust these fields to match the actual response structure
  answer: string;
}

const RulesLawyer: React.FC = () => {
  const [query, setQuery] = useState<string>("");
  const [result, setResult] = useState<string>("");
  const [history, setHistory] = useState<string[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;
    setLoading(true);
    setError(null);

    try {
      const response = await fetch("http://localhost:8000/rules", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ user_prompt: query }),
      });

      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.detail || "Failed to fetch rule answer");
      }

      const data: RuleResponse = await response.json();
      setResult(data.answer);
      setHistory((prevHistory) => [query, ...prevHistory]);
    } catch (err: any) {
      setError(err.message || "Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex">
      {/* Sidebar: Query History */}
      <aside className="w-1/4 p-4 border-r border-gray-300">
        <h2 className="text-xl font-bold mb-4">History</h2>
        <ul>
          {history.map((item, index) => (
            <li key={index} className="mb-2 text-gray-700">
              {item}
            </li>
          ))}
        </ul>
      </aside>

      {/* Main Content: Query and Results */}
      <main className="flex-1 p-6">
        <h1 className="text-3xl font-bold mb-6">RulesLawyer</h1>
        <form onSubmit={handleSubmit} className="mb-6">
          <div className="flex">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Ask a D&D rules question..."
              className="flex-1 p-3 border border-gray-300 rounded-l-md focus:outline-none focus:ring-2 focus:ring-blue-400"
            />
            <button
              type="submit"
              className="p-3 bg-blue-500 text-white font-bold rounded-r-md hover:bg-blue-600 transition-colors"
            >
              {loading ? "Loading..." : "Ask"}
            </button>
          </div>
        </form>
        {error && (
          <div className="text-red-500 mb-4">
            <p>{error}</p>
          </div>
        )}
        {result && (
          <div className="bg-white p-4 rounded shadow">
            <h2 className="text-xl font-bold mb-2">Answer</h2>
            <p>{result}</p>
          </div>
        )}
      </main>
    </div>
  );
};

export default RulesLawyer;
