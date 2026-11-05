-- Dijalankan otomatis oleh image Postgres pada inisialisasi pertama (lokal).
-- Database aplikasi dibuat oleh POSTGRES_DB; database Langflow dibuat terpisah.
SELECT 'CREATE DATABASE langflow'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'langflow')\gexec
