import { connection } from "next/server";

import { ChatForm } from "./components/chat-form";

async function isBackendHealthy(): Promise<boolean> {
  const backendUrl = process.env.BACKEND_URL ?? "http://127.0.0.1:8000";

  try {
    const response = await fetch(new URL("/health", backendUrl), {
      cache: "no-store",
      signal: AbortSignal.timeout(2000),
    });
    const body: unknown = await response.json();

    return (
      response.ok &&
      typeof body === "object" &&
      body !== null &&
      "status" in body &&
      body.status === "ok"
    );
  } catch {
    return false;
  }
}

export default async function Home() {
  await connection();
  const backendHealthy = await isBackendHealthy();

  return (
    <main className="mx-auto flex min-h-screen max-w-3xl flex-col justify-center gap-8 px-6 py-16">
      <div className="space-y-4">
        <p className="text-sm font-semibold uppercase tracking-widest text-blue-700">
          Moroccan Legal AI
        </p>
        <h1 className="text-4xl font-bold tracking-tight sm:text-5xl">
          Assistant juridique marocain
        </h1>
        <p className="max-w-2xl text-lg text-zinc-600 dark:text-zinc-300">
          Première étape : connecter l&apos;interface Next.js à notre API
          FastAPI. La recherche juridique et le chat seront ajoutés ensuite.
        </p>
      </div>

      <section className="rounded-2xl border border-zinc-200 bg-white p-6 dark:border-zinc-800 dark:bg-zinc-950">
        <h2 className="text-lg font-semibold">Connexion au backend</h2>
        <p
          className={
            backendHealthy
              ? "mt-3 font-medium text-green-700 dark:text-green-400"
              : "mt-3 font-medium text-amber-700 dark:text-amber-400"
          }
        >
          {backendHealthy
            ? "API FastAPI connectée et disponible"
            : "API indisponible : démarre le serveur FastAPI"}
        </p>
        <p className="mt-2 text-sm text-zinc-500 dark:text-zinc-400">
          Vérification de la route GET /health.
        </p>
      </section>

      <ChatForm />
    </main>
  );
}
