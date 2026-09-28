---
name: evidence-based-debugging
description: "Use when: debugging a bug, reproducing a failing workflow, fixing runtime issues, validating a patch, or explaining why a code path fails. Covers root-cause analysis, fail-first tests, minimal fixes, and verification with evidence."
---

# Evidence-Based Debugging

This skill packages a disciplined workflow for investigating, fixing, and validating code changes in a project. It is designed for real-world debugging where the goal is not just a plausible fix, but a verified fix backed by reproduction, root-cause analysis, and focused validation.

## When to use

Use this skill when you need to:
- reproduce a bug or unexpected behavior
- isolate a failing code path or incorrect assumption
- patch a runtime, logic, or integration issue
- confirm the fix with the smallest relevant test or command
- explain the root cause in a way that can be reviewed and trusted

## Core workflow

### 1. Reproduce the problem
- Capture the failing behavior exactly as it occurs.
- Record the command, input, stack trace, logs, or output that demonstrates the problem.
- If the issue is not yet reproducible, build the smallest possible reproduction.

### 2. Isolate the root cause
- Trace the data flow to the failing component.
- Check the exact assumptions and boundaries between layers, such as config, API responses, runtime state, or file inputs.
- Prefer the narrowest evidence available: stack trace, logs, debugger state, or failing assertion.
- If the cause is not clear, instrument the key boundary rather than guessing.

### 3. Form a single, testable hypothesis
- State the likely cause in one sentence.
- Avoid stacking speculative fixes.
- If the hypothesis is uncertain, gather one more fact before changing code.

### 4. Write or update a failing check
- Add or adapt a test that captures the bug before the fix.
- Prefer a narrow regression test or minimal reproduction over broad refactors.
- The test should fail for the same reason the real bug fails.

### 5. Implement the smallest root-cause fix
- Keep the patch scope minimal and directly related to the identified cause.
- Do not broaden the change unless the failure requires it.
- Prefer the cleanest fix that addresses the actual defect without introducing unrelated changes.

### 6. Verify with focused evidence
- Run the smallest relevant command or test suite that checks the changed behavior.
- Confirm the fix resolves the failing case without causing obvious regressions in adjacent logic.
- If validation fails, return to the root cause and iterate rather than layering guesses.

### 7. Report the outcome with evidence
- Summarize the root cause, the fix, and the validation command or result.
- Include the key evidence: failing reproduction, exact command run, and final success signal.
- If the issue remains unresolved, explain what was verified and what remains uncertain.

## Decision points

- If the bug cannot be reproduced: build a minimal reproduction first.
- If the cause is not yet localized: inspect the boundary where the wrong value or state is introduced.
- If multiple theories exist: test the simplest one with direct evidence before changing more code.
- If a fix becomes broad or speculative: reduce scope and revisit the root cause.
- If validation does not pass: do not claim success; continue debugging until the relevant proof is in hand.

## Completion checks

A task is ready to consider complete only when all of the following are true:
- the bug or failure was reproduced or modeled precisely
- the root cause was identified with evidence
- a failing check or minimal repro exists for the issue
- the patch is minimal and aligned to the root cause
- the relevant validation command passes
- the final summary includes both the fix and the verification evidence

## Example prompts

- "Debug the failing downloader flow and confirm the root cause before patching."
- "Reproduce the bug, add a failing test, then implement the minimal fix and verify it."
- "Trace the incorrect state through the data path and explain why the behavior is wrong."
- "Find the root cause of this runtime error and confirm the fix with the smallest relevant command."

## Related customizations

- a project-level instruction for testing and verification standards
- a prompt for writing regression tests before fixing code
- a workspace-specific review checklist for bugfix PRs
