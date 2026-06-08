---
name: additive-module-change-with-e2e
domain: engineering   subdomain: build
description: "WHAT: a procedure that sends ONE coding subagent to make a precise, ADDITIVE change to a named module — read the whole file(s) first, preserve every existing contract/return-shape/method-surface byte-for-byte, add the new capability, work on a git branch (reversible), and PROVE it end-to-end by running the REAL surface (a script that exercises the new behavior live) and capturing the literal output — never 'it imported' or 'it compiled'. It returns the branch+sha, a diff summary, the LITERAL captured run output, and an honest works/doesn't/UNKNOWN. The dispatch line fills the specifics (which repo/file, what to read, the context facts, the numbered additive change, the E2E test + its pass-criteria). WHEN: when you need a subagent to implement a scoped feature/refactor on an existing module without breaking it, 'add X to module Y and test it E2E', 'wire the new behavior in additively', any build where the existing callers must keep working (any of)."
golden: true
score: 1.00   runs: 3   verified_good: 3
check_level: SANITY   last_verified: "2026-06-07"
log:
  - 2026-06-07 PASS — frontend slice 2: a Vite+React+assistant-ui SPA over /ws, served by the FastAPI server. VERIFIED BY ME: git show (17 files, NO node_modules); re-ran npx vitest (5/5 eventMapping tests); booted server + curl / → served the real SPA (id="root" + JS bundle, not the legacy box); READ the builder's headless-chromium screenshot /tmp/promptworld_frontend.png — real render: chat header, user bubble, CEO reasoning, and a streamed tool-call card "🛠 Bash {command:'echo WSTEST'}" + composer. commit adc7586. Worker grounded the assistant-ui API from the installed .d.ts (docs 404'd) — useExternalStoreRuntime; tool_result merges onto the tool-call by toolCallId. GOLDENIZED here: 3/3 verified-good (streaming 278811f, ws 167daf46, frontend adc7586), score 1.00, no FAIL — meets golden criteria (>=0.9, >=3, no recent fail). Henceforth SANITY check suffices; drop to FULL_E2E on any sanity failure.
  - 2026-06-07 PASS — frontend slice 1: wire promptworld server's dead /ws to broadcast ClaudePMainAgent.on_event events live + run turn on /api/chat. VERIFIED BY ME (re-ran /tmp/test_promptworld_ws.py): booted the real PromptWorld FastAPI server, ws client received 14 LIVE events (every one tagged alias=ceo), intermediate assistant/tool_use + user/tool_result + result all streamed in real time, /api/chat still returned final reply (WSTEST); commit 167daf46 (+69/-16). Worker correctly diagnosed the dead path (broadcast used asyncio.create_task → "no running event loop" from the sync route's worker thread) + fixed via run_coroutine_threadsafe onto the loop captured on /ws connect. Additive (/api/chat contract intact). UNKNOWN flagged: multi-client fan-out (1 client tested), dead-socket-drop path, dept routes not live-streamed (out of scope). Approaching golden (2/2; need ≥3).
  - 2026-06-07 PASS — dispatched on promptworld p_main_agent.py (ClaudePMainAgent → stream-json live event streaming + on_event callback + compact()). VERIFIED BY ME (not the report): re-ran the worker's E2E /tmp/test_pmain_stream.py myself — intermediate assistant/tool_use + user/tool_result events streamed live (not just final text), returned text contained STREAMTEST, compact() observed compact_boundary; py_compile OK; commit 278811f (+168/-37). Worker also correctly folded a pre-existing BROKEN uncommitted delta (_run_turn lacked the on_event param → TypeError) into one coherent working change. Additive discipline held (CodeAgent surface/registry/api-key-scrub preserved). Honest UNKNOWN flagged (timeout-kill + empty/stderr-fallback paths present but not exercised this run).
---
## PROMPT
You are making a precise, ADDITIVE change to existing code and PROVING it works end-to-end through the
real surface. You do not break anything that already works, you do not guess, and your deliverable is a
captured live run — not "it imported".

## The inputs (filled by the dispatch line)
- `REPO` — the git repo root.
- `FILE(S)` — the module(s) to change.
- `READ_FIRST` — the exact files to read IN FULL before editing (the target module + every file whose
  contract it touches: callers, the things it returns into, its imports).
- `CONTEXT` — verified facts to take as given (don't re-derive them; build on them).
- `CHANGE_SPEC` — the numbered, additive change to make.
- `E2E_SPEC` — the real-surface test: the script to write, the command to run it, and the EXACT
  pass-criteria (what literal output proves it works).
- `BRANCH` — the git branch name to work on.

## The discipline (every step, in order)
1. **READ `READ_FIRST` completely** — the whole target file and every contract it touches. No grep-as-read,
   no partial reads. You cannot additively change what you have not fully read (complete operational
   boundary before edit).
2. **WORK REVERSIBLY** — `cd REPO && git checkout -b BRANCH` before any edit. (If the branch exists, use it.)
3. **CHANGE ADDITIVELY** — apply `CHANGE_SPEC`. The existing public surface — method names, signatures,
   return shapes, side effects every current caller relies on — stays **byte-for-byte intact**. New
   capability is ADDED (a new optional param defaulting to the old behavior, a new method, a new callback),
   never a silent change to what callers already get. If `CHANGE_SPEC` seems to require breaking an existing
   contract, STOP and report it rather than break it.
4. **GUARD THE NEW PATH** — a new callback/hook must never be able to kill the main path (wrap it; swallow
   its exceptions). Honor timeouts/limits the original had.
5. **TEST E2E THROUGH THE REAL SURFACE** — write the `E2E_SPEC` script, run it with the given command,
   and CAPTURE THE LITERAL OUTPUT. The test must exercise the NEW behavior on the real surface (run the
   actual binary/server/agent — not a mock, not a unit stub). If the underlying system fails for an
   environmental reason (auth/credit/network) that is NOT your code, report that explicitly AND show that
   your plumbing fired up to that point — do not claim success, do not fake the run.
6. **COMMIT** — write the commit message to a file and `git commit -F <file>` (avoids hook issues with path
   tokens). Scope the `git add` to the files you changed; never `git add -A`.

## Honesty
Mark what IS proven (by the captured run) vs UNKNOWN. A passing E2E run with its literal output is the only
evidence of success — your own "it works" is not. State what you did NOT verify.

## RETURN (concise)
- branch + commit sha,
- diff summary (what changed, per file — additive deltas only),
- the LITERAL E2E run output (the captured lines proving the new behavior + the pass-criteria check),
- honest works / doesn't / UNKNOWN, and anything you refused to do because it would break a contract.
