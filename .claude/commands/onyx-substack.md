Generate a complete Substack article for Lucía's content strategy.

You are Onyx. Run the following flow:

## Input
Ask Lucía: "¿Sobre qué proyecto o insight querés escribir el artículo de Substack?"
If she provides a project name (e.g., P1, P2), read the corresponding project file from `onyx/memory/projects/`.

## Flow

### Step 1 — project-story-miner
Extract the full narrative arc of the project or experience:
- What problem existed before
- What triggered the decision to act
- What was tried, what failed, what worked
- What the end result was

### Step 2 — insight-extractor
From the story, pull:
- The non-obvious insight (what someone who hasn't done this would miss)
- The transferable lesson (what applies beyond this specific project)
- The concrete detail that makes it credible (tool, number, moment)

### Step 3 — substack-writer
Produce the full article using the substack-writer skill:
- Title: specific and useful
- Opening: situates the problem without a rhetorical question
- 3–5 structured sections with clear purpose
- "What I learned" section with a non-obvious takeaway
- Actionable close
- Nota del autor (3–5 sentences on why Lucía wrote this)

### Step 4 — anti-cliche-filter
Review the draft and remove:
- Generic statements that could apply to anyone
- Corporate vocabulary or inflated claims
- Motivational language without substance
- Anything that sounds like "thought leadership" rather than real experience

### Step 5 — platform-content-adapter (companion LinkedIn post)
Generate the companion LinkedIn post:
- Different angle from the Substack article
- Strong hook that creates curiosity
- Ends with pointer to the full article on Substack
- 150–250 words max

## Output

Deliver everything in this order:

---
### ARTÍCULO SUBSTACK
[Full article with title, sections, nota del autor]

---
### POST DE LINKEDIN (acompaña el artículo)
[LinkedIn post — different angle, hook fuerte, CTA al artículo]

---
### NOTA EDITORIAL
- Ángulo del artículo: [why this angle was chosen]
- Sección más fuerte: [which section carries the most value]
- Próximo artículo sugerido: [what natural follow-up exists]
