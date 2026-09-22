export async function POST(request: Request) {
  let payload: unknown;

  try {
    payload = await request.json();
  } catch {
    return Response.json({ detail: "Corps JSON invalide" }, { status: 400 });
  }

  const backendUrl = process.env.BACKEND_URL ?? "http://127.0.0.1:8000";

  try {
    const response = await fetch(new URL("/api/v1/chat", backendUrl), {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
      cache: "no-store",
      signal: AbortSignal.timeout(5000),
    });
    const body: unknown = await response.json();

    return Response.json(body, { status: response.status });
  } catch {
    return Response.json(
      { detail: "Le backend FastAPI est indisponible" },
      { status: 503 },
    );
  }
}
