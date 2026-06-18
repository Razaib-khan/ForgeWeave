# Common Architecture Patterns

## Modular Monolith
- Single deployment unit
- Clear module boundaries with interfaces
- Good for: Most applications, team of 2-10

## Microservices
- Independent deployment per service
- Communication via API/events
- Good for: Large teams, independent scaling needs

## Event-Driven
- Components communicate via events
- Loose coupling, async processing
- Good for: Workflows, real-time updates, integrations

## Layered Architecture
- Presentation → Business Logic → Data Access
- Each layer only depends on the one below
- Good for: CRUD applications, enterprise software

## Hexagonal (Ports & Adapters)
- Core business logic has no external dependencies
- Adapters plug into ports for DB, UI, API
- Good for: Testability-critical systems, DDD

## Decision Checklist
- [ ] What are the non-functional requirements? (scalability, latency, reliability)
- [ ] How many teams will work on this?
- [ ] What's the expected change frequency?
- [ ] What's the deployment model? (self-hosted, serverless, edge)
