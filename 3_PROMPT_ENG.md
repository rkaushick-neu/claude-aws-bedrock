# 3. Prompt Engineering

Relevant Notebooks:
- [001_prompting.ipynb](./notebooks/3-prompt-engineering/001_prompting.ipynb)

Improving our prompt to get a more reliable & higher quality outputs.

## Prompt Engineering Iterative Process

```mermaid
flowchart TD
  A["Set a goal"] --> B["Write an initial prompt"]
  B --> C["Evaluate the prompt"]
  C --> D["Apply a prompt engineering technique"]
  D --> E["Re-evaluate to verify better performance"]
  E-. "Repeat" .-> D
```

## Our Goal

Write a prompt that generates a 1-day meal plan for an athlete based on their height, weight, goal and dietary restrictions.

![Prompt Engineering Goal](./images/Prompt_Eng_Goal.png)

