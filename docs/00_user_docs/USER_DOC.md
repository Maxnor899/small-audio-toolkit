# USER DOC

## Welcome

This documentation is for you if you want to analyze an audio file **without being a specialist** in signal processing, without knowing SAT or SAP², and without wanting to tweak dozens of technical parameters.

Here, we explain **how to think with the tool**, not how it is implemented.

---

## 1. An analysis is not a magic button

When you come with an audio file, the first question is not:
> “Which algorithms should I run?”

The real question is:
> **“What am I trying to do?”**

In our system, an analysis works like a **recipe**.

Before talking about ingredients, you need to know **for what occasion you are cooking**.

---

## 2. The recipe analogy (to understand the process)

Imagine you want to prepare a cocktail.

- Is it just to taste something, without a clear idea?
- Is it to verify a known recipe?
- Is it to confirm a specific flavor you already suspect?

Depending on the occasion, you don’t choose the same recipe.

### 2.1 What kind of cocktail?

When you say “I think there is something in this file”, we will ask you:

- Is it something **rhythmic**? (pulses, silences, durations)
- Something **sonic**? (tones, frequencies, shifts)
- Something **statistical**? (repetitions, anomalies)

This is like saying:
> “I’d like a sweet, fresh cocktail, beach vibe.”

At this point, we start to see what it looks like.

---

## 3. A recipe implies unavoidable ingredients

If you want a Mojito, there are ingredients you cannot escape:

- lime
- mint
- sugar
- a bit of alcohol

You can adjust proportions.
But you can’t decide that lime becomes chocolate.

In audio analysis, it’s the same:
- some **analyses are mandatory** depending on what you are looking for,
- others simply don’t make sense in that context.

---

## 4. With ingredients, you don’t do just anything

Even with the right ingredients, bad proportions ruin the result.

- Too much sugar → sickly
- Too little → bland

In our tool, these proportions correspond to **parameters**.

The important difference is:

- some parameters are **computed automatically**
- some are **known conventions**
- some cannot be decided without **your input**

We refuse to guess those for you.

---

## 5. What the tool does for you (and what it does not)

The good news is: we know the recipes.

Concretely:

- we automatically compute everything that can be computed honestly
- we apply known conventions
- and when a piece of information depends on your real intention…

👉 **we ask you clearly**.

This is not a bug.
It is deliberate.

---

## 6. What actually happens, step by step

Here is the simple flow:

```
[ You have an audio file ]
            |
            v
[ You say what you want to look for ]
 (rhythm? pulses? tones?)
            |
            v
[ We propose a recipe ]
 (a coherent type of analysis)
            |
            v
[ We prepare everything that can be done automatically ]
 (computed parameters, applied conventions)
            |
            v
[ If an important info is missing ]
 ---> We ask you a clear question
            |
            v
[ Protocol ready (or almost) ]
            |
            v
[ Analysis is launched ]
            |
            v
[ Clear result ]
 (something / nothing / not exploitable)
```

---

## 7. What if the result is “there is nothing”?

That is a valid result.

The difference is that you can be sure of one thing:

> *It is not because parameters were tweaked arbitrarily.*

If nothing appears, it means:
- the recipe was coherent,
- the ingredients were the right ones,
- and the file probably contains nothing of that kind.

---

## 8. What you don’t need to know

You don’t need to know:
- signal processing
- the algorithms used
- internal thresholds
- SAP²

All of that exists to **protect you from wrong conclusions**.

---

## Summary

You don’t need to know how to cook the recipe.

You just need to know **what cocktail you want to drink**.

The rest, we either do it properly — or we ask you when it’s not possible.
