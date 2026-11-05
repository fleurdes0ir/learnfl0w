# ponytail: Lazy Coding Pattern

Shortest diff wins. Best code = code never written.

## Ladder (stop at first rung that holds)

1. Does this need to exist? (YAGNI)
2. Stdlib does it? Use it.
3. Native platform (CSS/DB constraint/pgvector)? Use it.
4. Already-installed dependency? Use it.
5. One line? One line.
6. Only then: minimum working code.

## Rules

- No unrequested abstractions (no interface with 1 impl, no factory for 1 product, no config for constant)
- No boilerplate "for later"
- Deletion > addition
- Boring > clever
- Fewest files
- Two stdlib options same size → take edge-case-correct one

## Mark simplifications

```python
# ponytail: assumes single tenant, add multi-tenant when >100 orgs
```

Pattern: `ponytail: [ceiling], add when [threshold]`

## Never skip

- Input validation at trust boundaries
- Error handling preventing data loss  
- Security, accessibility
- Anything explicitly requested

## Tests

Non-trivial logic → ONE runnable check (assert-based self-check or small test file, no frameworks). Trivial one-liners need no test.

## Active always

No drift to over-building.
