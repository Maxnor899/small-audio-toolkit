# system design Journey — Synthesis (Intent → Protocol → Results)

This document is a **synthetic recap** of the complete system design discussed so far.
It is meant to be reused as a reference in other discussions, chats, or design reviews.

It deliberately focuses on:
- user point of view
- conceptual flow
- mapping to system responsibilities

Not on implementation details.

---

## 1. Core idea

The system is designed around a strict separation:

- **The user expresses intentions** (what they want to look for).
- **The system enforces methodology** (how it is allowed to look).

The user never tunes algorithms.
The system never guesses intentions.

---

## 2. Mental model for the user

An analysis is **not a button**.
It is closer to a **recipe**.

- The user chooses *what kind of question* they want to ask an audio file.
- The system chooses *how to ask that question correctly*.

Cocktail analogy:
- intention = type of cocktail
- protocol = recipe
- analyses = ingredients
- parameters = dosages
- rules = cooking principles you cannot violate

---

## 3. First mandatory choice: intention families

At the very beginning, the user must choose **what they want to try to do**.

These choices are imposed by the structure of the system itself and correspond to **families of questions**:

- Temporal
- Spectral
- Time–Frequency
- Modulation
- Inter-channel
- Information
- Steganography
- Meta-analysis

Key rules:
- The user may choose **several intentions**.
- **Each intention creates its own protocol**.
- Intentions are never mixed inside a single protocol.

> One intention = one coherent recipe.

---

## 4. Two-level questioning, depending on user expertise

### Level 1 — Always the same

**Question:**
> “What do you want to try to look for?”

The answer is one or more intention families.

This level never exposes technical concepts.

---

### Level 2 — Depends on user profile

#### Profile A: Simple user (default)

- The user does **not** choose analyses.
- The system proposes predefined recipe variants:
  - exploratory
  - standard (recommended)
  - robust (less sensitive)

Each variant is:
- coherent
- safe
- pre-validated

The user only chooses *style*, not mechanics.

---

#### Profile B: Advanced user (opt-in)

- The user may refine the recipe **within strict bounds**.
- They can:
  - select controlled variants
  - provide expected constraints (speed, scale, range)

They still:
- do not select algorithms freely
- do not tune thresholds arbitrarily

The system remains the arbiter.

---

## 5. Protocol generation principles

For each intention:

1. The system instantiates a **base protocol** (recipe).
2. Required analyses (ingredients) are automatically selected.
3. Parameters are handled according to fixed rules:

- **Derived**: computed automatically from the audio
- **Normative**: fixed by known conventions
- **Instrumental**: bounded by resources or measurement limits
- **Undefined**: explicitly require user input

No parameter is ever guessed.

---

## 6. The moulinette (compiler)

The moulinette is a **protocol compiler**, not an analysis tool.

Its role is to combine:
- the user protocol (intent)
- the audio context (objective facts)
- the global rule catalog

And produce:
- a fully compiled protocol, or
- a partially compiled protocol with explicit missing assumptions

It:
- never runs analyses
- never inspects results
- never retries with different parameters

Its job is to **prevent methodological cheating**.

---

## 7. Multiple intentions handling

If the user selects multiple intention families:

- multiple independent protocols are generated
- each protocol is compiled separately
- each protocol is executed separately
- results are evaluated separately

Results may later be:
- displayed side by side
- compared
- summarized

But never merged silently.

---

## 8. Execution and validation

Once a protocol is compiled:

1. SAT executes it **exactly as written**.
2. Output is a `results.json` containing measurements only.
3. SAP² evaluates structural applicability:
   - applicable
   - under-constrained
   - not applicable

No semantic meaning is inferred.

---

## 9. Why this design matters

Because of this pipeline:

- parameters are never tuned to make something appear
- assumptions are explicit and traceable
- negative results are trustworthy
- refusals are meaningful

The system may say:
> “I cannot run this yet”

That is not a failure.
It is enforced honesty.

---

## 10. One-sentence summary

> The user chooses the question.
> The system enforces how that question may be asked.
> Whatever the outcome, it can be trusted.

---

This document is intended as a **shared reference** for future discussions.

