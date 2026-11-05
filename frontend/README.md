# Frontend

Web app IT Career Compass (Next.js App Router, TypeScript, React Flow).

Aturan pengembangan: [AGENTS.md](AGENTS.md) dan [docs/engineering/coding-standards.md](../docs/engineering/coding-standards.md).

## Struktur

```text
src/
├── app/            # routes (App Router), termasuk /api/health
├── features/       # kode per fitur: components, hooks, api, types
├── components/     # UI bersama
└── lib/            # config, klien API, i18n (id.ts), utilitas
tests/              # test tambahan (test unit berdampingan dengan kode: *.test.ts)
```

## Menjalankan

```bash
cd frontend
npm install              # pertama kali; commit package-lock.json
npm run dev              # http://localhost:3000
```

Atur alamat API lewat `NEXT_PUBLIC_API_BASE_URL` (lihat `../.env.example`).

## Perintah

| Perintah | Fungsi |
|---|---|
| `npm run dev` | Server pengembangan |
| `npm run build` | Build produksi (output standalone untuk Docker) |
| `npm run lint` | ESLint tanpa warning |
| `npm run typecheck` | Cek tipe TypeScript |
| `npm test` | Test dengan Vitest |
| `npm run format` | Prettier |
| `npm run gen:api` | Membuat tipe dari `docs/api/openapi.yaml` |
