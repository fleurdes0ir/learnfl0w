# infra/

Konfigurasi deployment dan infrastruktur. Panduan lengkap: [docs/architecture/deployment.md](../docs/architecture/deployment.md).

| Folder | Isi |
|---|---|
| `cloud-run/` | Manifest atau skrip deploy tambahan (mis. `service.yaml`, Cloud Run Job) |
| `tailscale/` | Konfigurasi sidecar Tailscale untuk menjangkau 9router (divalidasi pada Gate G1) |

Aturan: tidak ada rahasia di folder ini. Nilai rahasia berasal dari Secret Manager.
