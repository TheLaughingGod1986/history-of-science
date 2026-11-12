import { afterEach, describe, expect, it } from "vitest";
import { mkdtempSync, mkdirSync, copyFileSync, writeFileSync, existsSync, readFileSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import { spawnSync } from "node:child_process";

const roots: string[] = [];
afterEach(() => roots.splice(0).forEach((root) => rmSync(root, { recursive: true, force: true })));
function fixture() {
  const root = mkdtempSync(path.join(tmpdir(), "prisma-cli-test-"));
  roots.push(root);
  mkdirSync(path.join(root, "scripts"));
  copyFileSync(path.resolve("scripts/with-direct-url.mjs"), path.join(root, "scripts/with-direct-url.mjs"));
  return root;
}
function run(root: string, variables: Record<string, string>, args: string[]) {
  return spawnSync(process.execPath, [path.join(root, "scripts/with-direct-url.mjs"), ...args], {
    env: { PATH: process.env.PATH, NODE_ENV: "test", ...variables }, encoding: "utf8",
  });
}
const probe = "console.log(JSON.stringify({database:process.env.DATABASE_URL,direct:process.env.DIRECT_URL}))";
function result(stdout: string) { return JSON.parse(stdout.trim().split("\n").at(-1)!); }

describe("Prisma CLI URL handoff", () => {
  it("preserves separate runtime and migration URLs without writing an env file", () => {
    const root = fixture();
    const output = run(root, { DATABASE_URL: "runtime-test", DIRECT_URL: "migration-test" }, [process.execPath, "-e", probe]);
    expect(output.status).toBe(0);
    expect(result(output.stdout)).toEqual({ database: "runtime-test", direct: "migration-test" });
    expect(existsSync(path.join(root, ".env"))).toBe(false);
  });
  it("falls back to the runtime alias and leaves an existing env file untouched", () => {
    const root = fixture();
    const content = "POSTGRES_URL=local-test\n";
    writeFileSync(path.join(root, ".env"), content);
    const output = run(root, {}, [process.execPath, "-e", probe]);
    expect(output.status).toBe(0);
    expect(result(output.stdout)).toEqual({ database: "local-test", direct: "local-test" });
    expect(readFileSync(path.join(root, ".env"), "utf8")).toBe(content);
  });
  it("skips migrate deploy only when no runtime URL is configured", () => {
    const root = fixture();
    expect(run(root, {}, ["prisma", "migrate", "deploy"]).status).toBe(0);
    expect(run(root, { DATABASE_URL: "test-only" }, ["prisma", "migrate", "deploy"]).status).not.toBe(0);
  });
  it("propagates child command failures", () => {
    expect(run(fixture(), {}, [process.execPath, "-e", "process.exit(7)"]).status).toBe(7);
  });
});
