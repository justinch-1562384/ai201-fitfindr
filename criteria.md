# Acceptance criteria — FitFindr

Five criteria that say what "working" means for this agent, written in unit 3
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"The agent handles errors"* is an opinion.
*"When search returns nothing, the agent stops before calling the second tool,
in 5 of 5 tries"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter one. A reason that says something about your tools, your loop, or the
data earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

**Two are written for you. You write three.**

---

## 1. A matching query completes all three tools

Given a query that matches at least one listing, the agent completes all three
tool calls and returns a fit card — in at least 4 of 5 tries.

**Why this target:**
As a fit card is reliant on output from suggest_outfit, there may be an issue calling the tool when suggest_results returns an empty list due to an error. With chaining calls, we do not expect 100% success rate 

---

## 2. An impossible query stops before the second tool

Given a query that matches no listings, the agent stops before calling
`suggest_outfit` and returns a message naming what to change — 5 of 5 tries.

**Why this target:**

This is an error condition, as the return statement for this tool in README.md should provide an string about general fashion advice rather than an empty string or an error. 
---

## 3. Something about state

Given a query that matches at least one listing, session["selected_item"]["id"] equals the id of the new_item passed to suggest_outfit and the id of the new_item passed to create_fit_card, in 5 of 5 runs where search returned results.

**Why this target:**

All three tools utilize the same listing dictionary. Should one not match the others in all three tool calls, we can assume the state is compromised at one point. 

---

## 4. Something about the fit card

<!-- YOU WRITE THIS ONE.

     The fit card calls a model, so the same input can produce different words
     each time. That's not a bug — it's the nature of the tool. So what would
     make it acceptable?

     Think about what you'd actually be unhappy to see. A caption that never
     mentions the price? Two different items producing the same opening
     sentence? A card longer than a caption anyone would post? Any of those can
     be turned into a number. -->

For five calls to create_fit_card, ensure that the text contains the listing's price is formatted as $N or $N.NN is found in the listing object 5 out of 5 times. Please also ensure that the platform and item_name is referenced as well. 

**Why this target:**
There will always be a listing dict object inputted based on our specs. README.MD also has the requirement to have the price, platform, and item_name always referenced in the fit card. 


---

## 5. Your choice

With an empty wardrobe, suggest_outfit returns a non-empty string with no error, and the agent still produces a fit card, in 5 of 5 tries.


**Why this target:**

The tool should give general styling advice instead of raising an error or returning "". The check on wardrobe['items'] happens in code before the model is called, so this path is predictable. The starter code also says unit 4 has you trigger the empty wardrobe, so you'll be testing it anyway.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 4 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 4. Something about the fit card

         The fit card is different every time.

         **Why this target:** ...

         > **Revised in unit 4:** For 5 different items, the 5 fit cards share
         > no opening sentence.
         >
         > **Why revised:** "different" wasn't checkable — two cards that
         > differed by one word still counted. The new version is something I
         > can actually score.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said the empty search stops it 5 of 5 times, but I got 3 of 5,
            so 3 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
