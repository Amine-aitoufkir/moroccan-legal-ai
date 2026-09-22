"use client";

import { FormEvent, useState } from "react";

type ChatResponse = {
  answer: string;
  sources: string[];
};

export function ChatForm() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setAnswer("");
    setError("");
    setIsLoading(true);

    try {
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });
      const body: unknown = await response.json();

      if (!response.ok) {
        throw new Error("La demande n'a pas pu être traitée.");
      }

      const chatResponse = body as ChatResponse;
      setAnswer(chatResponse.answer);
    } catch (requestError) {
      setError(
        requestError instanceof Error
          ? requestError.message
          : "Une erreur inattendue est survenue.",
      );
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <section className="rounded-2xl border border-zinc-200 bg-white p-6 dark:border-zinc-800 dark:bg-zinc-950">
      <h2 className="text-lg font-semibold">Tester le contrat de chat</h2>
      <p className="mt-2 text-sm text-zinc-500 dark:text-zinc-400">
        La réponse est temporaire : le RAG juridique sera connecté plus tard.
      </p>

      <form className="mt-5 space-y-4" onSubmit={handleSubmit}>
        <label className="block" htmlFor="question">
          <span className="text-sm font-medium">Question</span>
          <textarea
            className="mt-2 min-h-28 w-full rounded-xl border border-zinc-300 bg-transparent p-3 outline-none focus:border-blue-600 dark:border-zinc-700"
            id="question"
            maxLength={2000}
            minLength={3}
            onChange={(event) => setQuestion(event.target.value)}
            placeholder="Exemple : Quels sont mes droits dans un contrat de travail ?"
            required
            value={question}
          />
        </label>
        <button
          className="rounded-xl bg-blue-700 px-5 py-3 font-semibold text-white disabled:cursor-not-allowed disabled:opacity-60"
          disabled={isLoading}
          type="submit"
        >
          {isLoading ? "Envoi..." : "Envoyer la question"}
        </button>
      </form>

      {answer ? (
        <div className="mt-5 rounded-xl bg-zinc-100 p-4 text-zinc-800 dark:bg-zinc-900 dark:text-zinc-100">
          {answer}
        </div>
      ) : null}
      {error ? <p className="mt-5 text-red-700">{error}</p> : null}
    </section>
  );
}
