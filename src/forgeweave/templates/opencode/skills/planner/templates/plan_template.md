# Execution Plan Template

**Goal:** {{goal}}
**Complexity:** {{complexity}}

## Steps

{% for step in steps %}
{{loop.index}}. **{{step.action}}**
   - Tools: {{step.tools | join(", ")}}
   - Depends on: {{step.depends_on | join(", ") or "none"}}
{% endfor %}

## Dependencies

{% for dep in dependencies %}
- {{dep}}
{% endfor %}

## Risks

{% for risk in risks %}
- {{risk}}
{% endfor %}
