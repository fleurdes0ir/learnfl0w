import { id } from "@/lib/i18n/id";

export default function HomePage() {
  return (
    <main style={{ padding: "2rem", maxWidth: 720, margin: "0 auto" }}>
      <h1>{id.appName}</h1>
      <p>{id.tagline}</p>
    </main>
  );
}
