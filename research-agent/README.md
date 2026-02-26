# research-agent

Autonomous research agent demo built on [APEX](https://github.com/axiom-llc/apex).

The agent self-directs across a SEARCH/THINK/DONE loop — fetching from public APIs, reasoning over accumulated knowledge, and producing a final Markdown report. No human input after the initial goal.

## How it works

```
goal → [SEARCH public APIs] → [THINK: synthesise, identify gaps] → [DONE] → report.md
             ↑___________________________|
```

Each step the agent decides its own next action. It declares DONE when the goal is satisfied.

## Source

Agent code lives in [`apex/examples/`](https://github.com/axiom-llc/apex/tree/main/examples):

- `research-agent.sh` — single autonomous agent
- `research-swarm.sh` — parallel swarm with synthesis layer

## Sample Output

See [`sample-run/report.md`](./sample-run/report.md) for an example research report produced by the agent.

## Requirements

- [APEX](https://github.com/axiom-llc/apex) installed
- `GEMINI_API_KEY` set in environment

## Usage

```bash
export GEMINI_API_KEY=your-key
./apex/examples/research-agent.sh "how does RAFT consensus work" 15

# autonomous topic selection
./apex/examples/research-agent.sh
```
