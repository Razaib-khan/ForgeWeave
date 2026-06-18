# Research Plan

**Topic:** {{topic}}
**Depth:** {{depth}}
**Focus:** {{focus}}

## Subtopics

{% for subtopic in subtopics %}
### {{subtopic.name}}

**Questions:**
{% for q in subtopic.questions %}
- {{q}}
{% endfor %}

**Seed URLs:**
{% for url in subtopic.seed_urls %}
- {{url}}
{% endfor %}

{% endfor %}
## Execution Strategy

**Strategy:** {{execution_strategy}}
**Total subtopics:** {{subtopics | length}}
