import { describe, expect, it } from "vitest";
import { apiUrl } from "@/lib/config";

describe("apiUrl", () => {
  it("joins base and path with exactly one slash", () => {
    expect(apiUrl("/api/v1/me")).toMatch(/^https?:\/\/[^/]+\/api\/v1\/me$/);
    expect(apiUrl("api/v1/me")).toMatch(/\/api\/v1\/me$/);
  });
});
