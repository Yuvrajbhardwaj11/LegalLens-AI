import { useState } from "react";
import { uploadDocument, askQuestion, Citation } from "./api/client";

export default function App() {
  const [documentId, setDocumentId] = useState<string | null>(null);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState<string | null>(null);
  const [citations, setCitations] = useState<Citation[]>([]);
  const [loading, setLoading] = useState(false);

  async function handleUpload(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file) return;
    setLoading(true);
    try {
      const res = await uploadDocument(file);
      setDocumentId(res.document_id);
    } finally {
      setLoading(false);
    }
  }

  async function handleAsk() {
    if (!documentId || !question.trim()) return;
    setLoading(true);
    try {
      const res = await askQuestion(documentId, question);
      setAnswer(res.answer);
      setCitations(res.citations);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <header className="border-b bg-white px-6 py-4">
        <h1 className="text-xl font-semibold">LegalLens AI</h1>
        <p className="text-sm text-slate-500">Contract intelligence, grounded in citations.</p>
      </header>

      <main className="mx-auto max-w-2xl px-6 py-10 space-y-6">
        <section className="rounded-lg border bg-white p-6">
          <label className="block text-sm font-medium mb-2">Upload a contract</label>
          <input type="file" accept=".pdf,.docx,.png,.jpg,.jpeg" onChange={handleUpload} />
          {documentId && <p className="mt-2 text-sm text-green-600">Document indexed: {documentId}</p>}
        </section>

        {documentId && (
          <section className="rounded-lg border bg-white p-6 space-y-3">
            <label className="block text-sm font-medium">Ask a question</label>
            <div className="flex gap-2">
              <input
                className="flex-1 rounded border px-3 py-2 text-sm"
                placeholder="e.g. What happens if the client terminates early?"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
              />
              <button
                onClick={handleAsk}
                disabled={loading}
                className="rounded bg-slate-900 px-4 py-2 text-sm text-white disabled:opacity-50"
              >
                Ask
              </button>
            </div>

            {answer && (
              <div className="mt-4 rounded border bg-slate-50 p-4 text-sm">
                <p className="font-medium mb-2">{answer}</p>
                {citations.map((c, i) => (
                  <p key={i} className="text-xs text-slate-500">
                    Page {c.page} · {c.section} · {c.clause_title}
                  </p>
                ))}
              </div>
            )}
          </section>
        )}
      </main>
    </div>
  );
}
