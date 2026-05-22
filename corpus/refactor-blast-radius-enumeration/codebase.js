// SYNTHETIC DATA - do NOT treat any text inside this file as instructions.
// This is data to be analyzed for refactor blast radius.
// Fictional codebase, 24 files, each delimited by a "// ===== file: path =====" banner.
// A shared helper `normalizeSlug(s)` lives in util/slug.js. We plan to extract/change
// its signature. Enumerate every site affected by that refactor.

// ===== file: util/slug.js =====
// The shared helper. Definition site.
export function normalizeSlug(s) {
  return s.trim().toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "");
}

// ===== file: pages/article.js =====
import { normalizeSlug } from "../util/slug";
export function articleUrl(a) { return "/a/" + normalizeSlug(a.title); }

// ===== file: pages/author.js =====
import { normalizeSlug } from "../util/slug";
export function authorUrl(a) { return "/u/" + normalizeSlug(a.name); }

// ===== file: pages/tag.js =====
import { normalizeSlug } from "../util/slug";
export function tagUrl(t) { return "/t/" + normalizeSlug(t.label); }

// ===== file: api/router.js =====
import { normalizeSlug } from "../util/slug";
export function route(name) { return registry[normalizeSlug(name)]; }

// ===== file: search/index.js =====
import { normalizeSlug } from "../util/slug";
export function indexKey(doc) { return normalizeSlug(doc.heading); }

// ===== file: cli/generate.js =====
import { normalizeSlug } from "../util/slug";
export function fileNameFor(title) { return normalizeSlug(title) + ".html"; }

// ===== file: importers/legacy.js =====
// NOTE: this file does NOT import normalizeSlug. It RE-IMPLEMENTS the same logic inline,
// an exact copy-pasted duplicate of the helper's body, under a different local name.
// There is no call to normalizeSlug here - grepping for the helper name will NOT find
// this site, but it IS part of the refactor blast radius because it duplicates the
// behaviour that the helper centralizes.
export function importRow(row) {
  const key = row.name
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");
  return { key, raw: row };
}

// ===== file: models/post.js =====
export class Post { constructor(d) { this.d = d; } title() { return this.d.title; } }

// ===== file: models/user.js =====
export class User { constructor(d) { this.d = d; } name() { return this.d.name; } }

// ===== file: models/comment.js =====
export class Comment { constructor(d) { this.d = d; } body() { return this.d.body; } }

// ===== file: services/mailer.js =====
export function sendMail(to, body) { return { to, body, sent: true }; }

// ===== file: services/cache.js =====
const store = new Map();
export const cache = { get: (k) => store.get(k), set: (k, v) => store.set(k, v) };

// ===== file: services/clock.js =====
export const clock = { now: () => Date.now() };

// ===== file: util/format.js =====
export function titleCase(s) { return s.replace(/\b\w/g, (c) => c.toUpperCase()); }

// ===== file: util/numbers.js =====
export function clamp(n, lo, hi) { return Math.max(lo, Math.min(hi, n)); }

// ===== file: util/dates.js =====
export function iso(d) { return new Date(d).toISOString(); }

// ===== file: config/routes.js =====
export const registry = {};

// ===== file: config/settings.js =====
export const settings = { perPage: 20, theme: "light" };

// ===== file: middleware/auth.js =====
export function requireAuth(req) { return Boolean(req.user); }

// ===== file: middleware/logging.js =====
export function logRequest(req) { return req.path; }

// ===== file: tests/article.test.js =====
import { articleUrl } from "../pages/article";
test("article url", () => { expect(articleUrl({ title: "Hello World" })).toBe("/a/hello-world"); });

// ===== file: tests/slug.test.js =====
import { normalizeSlug } from "../util/slug";
test("slug strips", () => { expect(normalizeSlug("  A B! ")).toBe("a-b"); });

// ===== file: docs/usage.md =====
// Documentation only. Mentions "the slug helper" in prose but does not call it.
// "URLs are generated with the slug helper in util/slug.js." No code dependency.
