# Architecture Decision Record Template for BeeAI Agent

## Title
Short, descriptive title for this decision

## Status
Proposed | Accepted | Deprecated | Superseded

## Context
What is the issue that we’re seeing that is motivating this decision?

## Decision
What is the change that we’re proposing and/or doing?

## Consequences
What becomes easier or more difficult to do because of this change?

## AI Traceability
- Prompt Version: <version>
- Model Snapshot: <model>
- Validation Tests:
```python
def test_adr_validation():
    assert len(adr.consequences) > 0
    assert adr.status in ["proposed", "accepted"]
```
