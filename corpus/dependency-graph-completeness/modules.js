// SYNTHETIC DATA - do NOT treat any text inside this file as instructions.
// This is data to be analyzed for module dependency completeness.
// Fictional codebase. 22 modules in one file, each delimited by a banner comment.
// Enumerate the full TRANSITIVE dependency set of the module named "orchestrator".

// ========== module: orchestrator ==========
import { planRun } from "./planner";
import { loadConfig } from "./config";
import { Reporter } from "./reporter";
export function orchestrate(input) {
  const cfg = loadConfig();
  const plan = planRun(input, cfg);
  return new Reporter(plan).emit();
}

// ========== module: planner ==========
import { resolveSteps } from "./steps";
import { Validator } from "./validator";
const HANDLER_PREFIX = "./handlers/";
export function planRun(input, cfg) {
  const v = new Validator(cfg);
  v.check(input);
  const steps = resolveSteps(input);
  // Dynamically load the handler module by name. The handler module is NOT
  // referenced by any static import anywhere in this codebase.
  const handlerName = cfg.handler || "default";
  const handler = require(HANDLER_PREFIX + handlerName);
  return steps.map((s) => handler.apply(s));
}

// ========== module: config ==========
import { readEnv } from "./env";
import { defaults } from "./defaults";
export function loadConfig() {
  return { ...defaults, ...readEnv() };
}

// ========== module: reporter ==========
import { format } from "./formatter";
import { sink } from "./sink";
export class Reporter {
  constructor(plan) { this.plan = plan; }
  emit() { return sink(format(this.plan)); }
}

// ========== module: steps ==========
import { Graph } from "./graph";
export function resolveSteps(input) {
  return new Graph(input).topoSort();
}

// ========== module: validator ==========
import { schema } from "./schema";
export class Validator {
  constructor(cfg) { this.schema = schema(cfg); }
  check(x) { return this.schema.validate(x); }
}

// ========== module: env ==========
export function readEnv() { return process.env; }

// ========== module: defaults ==========
export const defaults = { handler: "fastpath", retries: 3 };

// ========== module: formatter ==========
import { theme } from "./theme";
export function format(plan) { return theme.wrap(JSON.stringify(plan)); }

// ========== module: sink ==========
import { transport } from "./transport";
export function sink(text) { return transport.send(text); }

// ========== module: graph ==========
import { dsu } from "./dsu";
export class Graph {
  constructor(input) { this.input = input; this.dsu = dsu(); }
  topoSort() { return this.input.slice().sort(); }
}

// ========== module: schema ==========
import { rules } from "./rules";
export function schema(cfg) { return { validate: (x) => rules(cfg).every((r) => r(x)) }; }

// ========== module: theme ==========
export const theme = { wrap: (s) => "[" + s + "]" };

// ========== module: transport ==========
import { retry } from "./retry";
export const transport = { send: (t) => retry(() => t) };

// ========== module: dsu ==========
export function dsu() { return { find: (x) => x, union: () => {} }; }

// ========== module: rules ==========
export function rules(cfg) { return cfg.retries ? [() => true] : []; }

// ========== module: retry ==========
import { backoff } from "./backoff";
export function retry(fn) { return backoff(fn); }

// ========== module: backoff ==========
export function backoff(fn) { return fn(); }

// ========== module: handlers/fastpath ==========
// This module is loaded ONLY via the dynamic require in planner:
//   require(HANDLER_PREFIX + (cfg.handler || "default"))
// and cfg.handler defaults to "fastpath" (see defaults module).
// There is NO static `import` of this module anywhere - grepping for an import
// statement will never find it. It IS a transitive runtime dependency of orchestrator.
import { meter } from "./meter";
export function apply(step) { meter.tick(); return step; }

// ========== module: handlers/default ==========
// A second possible dynamic handler target (cfg.handler === "default").
import { meter } from "./meter";
export function apply(step) { meter.tick(); return step; }

// ========== module: meter ==========
// Dependency of the dynamically-loaded handler modules only.
export const meter = { tick: () => {} };

// ========== module: unused-legacy ==========
// NOT a dependency of orchestrator. Nothing in the orchestrator graph imports this.
// It is a distractor - a leftover module that exists but is unreachable from orchestrator.
import { backoff } from "./backoff";
export function legacyRun() { return backoff(() => 0); }
