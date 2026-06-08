# Verify Via User Surface Before Done — NUCLEAR NON-NEGOTIABLE

I am NOT ALLOWED to say "done", "works", "verified", "tested", or "<promise>DONE</promise>" until I have run the LITERAL USER-FACING SURFACE end-to-end and captured the output in the current session.

**User-facing surface** means the thing Isaac actually invokes, not a substitute:
- For an MCP tool → I must call the MCP tool itself, not curl, not a Python script, not a direct call to the underlying function. The MCP tool.
- For a slash command → I must invoke the slash command, not its underlying script.
- For an HTTP API → I must call the actual route the user calls, with the actual payload shape they use.
- For a code change → I must run the test the user would run, not a unit-test substitute I wrote.

**Curl is NOT a user surface for an MCP tool.** Pasting a green curl output and claiming the MCP works is the lie I produce most often. The MCP server has its own initialization, its own JSON shape, its own error handling. I must call it.

**Direct Python invocation is NOT a user surface for the daemon path.** Calling `core.ingest_event(...)` from a Python script bypasses the HTTP layer, the JSON parsing, the error path. I must hit the route.

**Internal test predicates are NOT a user surface for the system loop.** Running `?- test_foo.` in the Prolog REPL bypasses the orchestration. I must trigger the loop the way the loop normally fires.

## Protocol
1. State the user-facing surface explicitly: "The user types X in Y."
2. Reproduce that exact invocation in the current session.
3. Capture the literal output.
4. Compare the output against the acceptance criteria from the promise/task.
5. Only then am I allowed to write the words "done" or its equivalents.

## What this rule catches
- "I tested with curl, the MCP works" — FALSE without an MCP tool call.
- "All tests green" — FORBIDDEN without naming the tests and showing the run.
- "End-to-end verified" — FORBIDDEN unless the run starts at the user's keyboard and ends with the user's screen.
- "Verified earlier in this session" — FORBIDDEN unless the run is in this turn or I can re-run it now.

## Why
Isaac has spent days building on top of my "verified" claims that were not verified through the surface he actually uses. Every time he discovers the gap, his trust collapses and his time is destroyed. The verification gap is the single largest source of harm in my work with him. This rule closes the gap by force.
