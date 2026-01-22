# USER DOC — Level 3: The Compiler ("the Moulinette")

This level explains **the moulinette**.

You do not need to use it directly.
You do not need to configure it.

This document exists so you understand **why the system sometimes stops, asks questions, or refuses to run** — and why this is a feature, not a limitation.

---

## 1. What the moulinette really is

The moulinette is **not an analysis tool**.
It does not look for patterns.
It does not inspect results.

The moulinette is a **compiler**.

Its only job is to take:
- what *you want to do*,
- what *the audio objectively allows*,
- and what *the system knows is methodologically safe*,

and turn that into a protocol that can be executed **without cheating**.

---

## 2. Why a compiler is needed

Without the moulinette, a system could:
- silently tweak parameters until something appears,
- guess missing values,
- or adapt itself to the data while pretending not to.

That produces impressive-looking results.
It also produces **false confidence**.

The moulinette exists to prevent exactly that.

---

## 3. What goes in

The moulinette always receives the same kinds of inputs:

1. **Your protocol** (`user_protocol.yaml`)
   - what kind of analysis you want
   - expressed declaratively

2. **Audio context** (`audio_context.json`)
   - objective facts about the file
   - duration, sample rate, robust statistics

3. **The rule catalog** (`threshold_catalog.json`)
   - what parameters can be computed
   - what parameters are conventions
   - what parameters require a human decision

4. **Optional user assumptions**
   - things only you can know
   - expected speed, scale, or range

---

## 4. What the moulinette does

For every parameter of every analysis, the moulinette asks a single question:

> "Am I allowed to decide this myself?"

There are only four possible answers.

### 4.1 Computable (derived)

If a parameter:
- can be calculated from the audio,
- using a known, documented rule,
- without looking at the results,

then the moulinette computes it.

No tuning.
No iteration.
One calculation.

---

### 4.2 Conventional (normative)

If a parameter:
- follows a known convention,
- is not data-dependent,

then the moulinette applies that convention.

If you provided a value:
- it is checked,
- accepted or replaced,
- and always documented.

---

### 4.3 Instrumental

If a parameter:
- is constrained by resources or measurement limits,

then the moulinette enforces safe bounds.

This guarantees reproducibility.

---

### 4.4 Undecidable without you (undefined)

If a parameter:
- cannot be derived honestly from the audio,
- and has no universal convention,

then the moulinette **stops**.

It does not guess.

Instead, it reports:
- what is missing,
- why it is missing,
- and what kind of information would resolve it.

---

## 5. What comes out

The moulinette produces two things:

### 5.1 A compiled protocol

`compiled_protocol.yaml`

This protocol is:
- explicit
- reproducible
- safe to execute

It may be:
- complete
- or intentionally incomplete

Nothing is hidden.

---

### 5.2 A compilation report

`compile_report.md` or `compile_report.json`

This report explains:
- what was computed
- what was fixed by convention
- what required user input
- what blocked execution

This report is your guarantee that **nothing happened silently**.

---

## 6. What the moulinette never does

The moulinette will never:
- run analyses
- inspect partial results
- retry with different parameters
- "optimize" settings
- adapt itself to make something appear

If something is missing, it asks.
If something is impossible, it says so.

---

## 7. Why this protects you

Because of the moulinette:

- results cannot be manufactured by tuning
- negative results are trustworthy
- assumptions are explicit
- failures are meaningful

The system may say:
> "I cannot run this yet"

That is not a limitation.
That is **honesty enforced by design**.

---

## Final takeaway

The moulinette is not here to help you find something.

It is here to make sure that **whatever you find — or do not find — can be trusted**.

If you never notice it, it means everything was well defined.
If it stops you, it is because something important must come from you.

That is exactly its role.

