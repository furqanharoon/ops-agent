# ops-agent

`ops-agent` is an AI engineering project for incident investigation workflows.

The project started as a ReAct-style agent that could retrieve incident data through tools. It has since evolved into a workflow-oriented system that combines agentic tool use, LangGraph orchestration, human approval gates, checkpointing, interrupt and resume behavior, custom evaluations, and structured observability.

The system is structured around production-oriented design patterns without claiming to be a fully deployed operations platform. Its focus is agent state management, durable workflow design, human-in-the-loop routing, evaluation harnesses, and observable tool execution.

## Current Capabilities

### ReAct Agent

The agent follows a ReAct-style loop:

```text
Think
  |
Select tool
  |
Execute tool
  |
Observe result
  |
Continue reasoning
  |
Produce final output
```

The runtime maintains agent state across iterations, including the original user query, trace ID, message history, tool history, observations, token usage, LLM call count, and retrieved incident data.

The planner asks the model to choose the next tool or return a final answer. The implementation currently restricts execution to one tool per model response, which keeps the loop easy to inspect and makes state transitions explicit.

Implemented tools:

| Tool | Purpose |
| --- | --- |
| `get_incident` | Retrieves case details such as case ID, priority, reporter, issue type, short description, and customer satisfaction. |
| `get_incident_duration` | Retrieves opened and closed timestamps and computes incident duration. |
| `get_incident_timeline` | Retrieves the chronological incident event timeline. |

The agent stores retrieved incident data in memory so later workflow stages can operate on structured facts rather than repeatedly calling tools.

## Incident Investigation Workflow

The investigation flow is split into clear stages:

1. Incident retrieval through agent tools
2. Duration retrieval
3. Timeline retrieval
4. Investigation facts extraction
5. Incident analysis
6. Human approval for high-severity incidents
7. Report generation or manual review routing

The agent is responsible for gathering operational data. The workflow is responsible for turning that data into facts, analysis, approval decisions, and final output.

That separation is intentional. It keeps the agentic retrieval loop independent from the deterministic workflow stages that follow it.

## LangGraph Workflow

The project uses LangGraph to model the incident investigation as an explicit state machine.

Implemented LangGraph concepts:

| Concept | How it appears in this project |
| --- | --- |
| `StateGraph` | Defines the workflow around a typed `WorkflowState`. |
| Nodes | `facts`, `analysis`, `required_approval`, `report`, and `manual_review`. |
| Edges | Define normal flow from facts to analysis to output. |
| Conditional routing | Routes high-severity incidents to human approval. |
| Fan-out / fan-in concepts | Represented at the architecture level through staged data gathering and consolidation into investigation facts. |
| Checkpointing | Uses LangGraph `MemorySaver` for workflow state persistence during a run. |
| Interrupts | Pauses execution when human approval is required. |
| Resume | Continues the workflow after an approval or rejection decision is supplied. |
| Human-in-the-loop | High-severity incidents require an explicit approval decision before report generation. |

Current workflow:

```text
START
  |
Facts
  |
Analysis
  |
High Severity?
  |-------- No -------> Report -------> END
  |
 Yes
  |
Human Approval
  |
Approved?
  |-------- Yes ------> Report -------> END
  |
 No
  |
Manual Review -------> END
```

### Workflow Stages

`Facts`

Builds an `InvestigationFacts` object from the incident, duration, and timeline data gathered by the agent. This stage derives operational metrics such as resolution duration, total personnel, handoff count, support levels involved, and escalation count.

`Analysis`

Produces an `IncidentAnalysis` object from the extracted facts. The current severity rule is intentionally simple: incidents with more than two escalations are classified as high severity. This makes the routing behavior transparent and testable.

`High Severity?`

Routes normal incidents directly to report generation. High-severity incidents are routed to human approval.

`Human Approval`

Uses LangGraph `interrupt()` to pause the workflow and return an approval request payload. The workflow does not proceed until a resume command supplies the human decision.

`Approved?`

Routes approved incidents to report generation. Rejected incidents are routed to manual review with the rejection reason preserved in workflow state.

`Report`

Generates a text report containing facts, derived metrics, severity, and analysis summary.

`Manual Review`

Terminates the automated path when a human rejects the report. This keeps rejected high-severity incidents from being treated as fully automated completions.

## Human-In-The-Loop Workflow

High-severity incidents require human approval before report generation.

Conceptually, the flow works like this:

```text
Workflow reaches approval node
  |
interrupt() returns an approval request
  |
LangGraph checkpoints workflow state
  |
Caller keeps the same thread_id
  |
Human submits approval decision
  |
Workflow resumes from checkpoint
  |
Conditional routing decides next node
```

`interrupt()`

The approval node calls `interrupt()` with a payload containing a message and the current analysis. This pauses execution and gives the caller enough context to ask a human for a decision.

Checkpointing

The workflow is compiled with a LangGraph checkpointer. The current implementation uses `MemorySaver`, which preserves workflow state between interrupt and resume calls within the same process.

`thread_id`

LangGraph uses `thread_id` to associate a workflow invocation with its checkpointed state. Resume calls must use the same `thread_id` as the interrupted workflow.

Resume flow

The workflow is resumed by invoking the graph with a LangGraph `Command(resume=...)` payload. The resume payload supplies `approval_status` and, when rejected, a `rejection_reason`.

Example:

```python
from langgraph.types import Command
from langgraph.workflow import graph

resume_result = graph.invoke(
    Command(
        resume={
            "approval_status": "approved"
        }
    ),
    config={
        "configurable": {
            "thread_id": "workflow-1"
        }
    }
)
```

## Observability

The project includes custom observability features in the agent runtime. The goal is to make agent behavior inspectable without depending on an external tracing platform.

Implemented observability:

| Feature | Purpose |
| --- | --- |
| Trace IDs | Correlate work performed for a single agent execution. |
| Tool execution logging | Records which tool was called and with what arguments. |
| Tool execution timing | Captures elapsed time for each tool call. |
| Tool history | Stores tool name, arguments, and result in agent state. |
| Failure logging | Captures tool failures with error details and execution context. |
| Observation tracking | Stores observations returned from tools. |
| Token usage tracking | Accumulates input, output, and total token usage. |
| LLM call counting | Tracks how many model calls were required for a run. |

Observability flow:

```text
User Query
  |
Agent Runtime creates trace_id
  |
Planner LLM call
  |
Tool selected
  |
Tool execution timer starts
  |
Tool succeeds or fails
  |
Structured log event emitted
  |
Agent state updated with history, observations, and token usage
```

Example structured event:

```json
{
  "timestamp": 1760000000.0,
  "event_type": "tool_execution",
  "payload": {
    "trace_id": "d3a8f9e2-9f29-4f9d-9a41-8b77f9d8c110",
    "tool_name": "get_incident",
    "arguments": {
      "case_id": "INC24493"
    },
    "execution_time_in_ms": 0.018
  }
}
```

The logs are currently printed as JSON. A future version can route the same event structure to a database, tracing system, or workflow observability dashboard.

## Evaluation Framework

The project includes a custom evaluation framework for regression testing the incident investigation behavior.

Implemented evaluation features:

| Feature | Purpose |
| --- | --- |
| JSON test cases | Stores repeatable investigation scenarios and expected facts. |
| Automated execution | Runs the agent against each evaluation query. |
| Pass/fail scoring | Compares extracted facts against expected values. |
| Regression testing | Detects when changes break known investigation behavior. |

The evaluations are intentionally separate from the workflow system.

```text
Evaluation Runner
  |
Runs agent execution
  |
Builds investigation facts
  |
Compares facts to expected JSON
  |
Reports pass/fail results
```

The workflow is the system under test. The eval runner is the testing harness.

This separation matters because the evaluation system should not become part of the product path. It should exercise the product path from the outside, collect outputs, and score them against expected behavior.

## Technical Architecture

High-level architecture:

```text
User Query
     |
ReAct Agent
     |
Tool Calls
     |
Incident Data
     |
Facts Extraction
     |
LangGraph Workflow
     |
Analysis
     |
Human Approval
     |
Report
```

More detailed execution path:

```text
User Query
  |
app.runtime.AgentState
  |
app.planner.decide_tool()
  |
Anthropic tool-calling response
  |
app.tools.tools_registry
  |
PostgreSQL incident data
  |
Agent observations and memory
  |
app.services.facts_extractor
  |
app.services.analyzer
  |
langgraph.workflow.StateGraph
  |
Approval interrupt or report generation
```

Core modules:

| Module | Responsibility |
| --- | --- |
| `app/runtime.py` | Agent execution loop, agent state, tool execution, memory, and observability counters. |
| `app/planner.py` | LLM planner, tool schema definitions, and tool/final-response decision parsing. |
| `app/tools/incident_tools.py` | Incident data retrieval tools backed by PostgreSQL. |
| `app/services/facts_extractor.py` | Converts raw incident data into structured investigation facts. |
| `app/services/analyzer.py` | Classifies incident severity and builds analysis summary. |
| `app/services/report_generator.py` | Creates final investigation report text. |
| `langgraph/workflow.py` | LangGraph workflow definition, edges, routing, and checkpointer setup. |
| `langgraph/nodes.py` | Workflow node implementations and routing functions. |
| `evals/run_evals.py` | Evaluation runner for regression testing. |
| `evals/scoring.py` | Field-level expected-versus-actual scoring. |

## Why The Architecture Is Split This Way

The project separates retrieval, reasoning, workflow orchestration, and evaluation because each part has a different failure mode.

The ReAct agent is useful for deciding what information to retrieve next. It is flexible, but it is also probabilistic.

The tools provide a narrow contract around operational data access. They keep database access out of the prompt and make each external action observable.

The facts extractor converts raw tool output into typed data. This gives the workflow a stable interface and makes downstream analysis easier to test.

The LangGraph workflow handles state transitions, approval gates, and resume behavior. These are control-flow concerns, so they are better represented as a graph than hidden inside a long prompt.

The evaluation harness stays outside the workflow. This keeps tests independent from the implementation path and makes it easier to catch regressions in the behavior users actually experience.

## Engineering Concepts Demonstrated

This project highlights AI engineering patterns that are relevant beyond a narrow chatbot wrapper:

| Concept | Demonstrated by |
| --- | --- |
| ReAct | Iterative think, act, observe loop in the agent runtime. |
| Tool calling | Model-selected incident tools with explicit schemas. |
| Agent state management | `AgentState` tracks messages, observations, memory, tool history, trace ID, and token usage. |
| LangGraph | Workflow modeled as a `StateGraph` with nodes, edges, and conditional routing. |
| Human-in-the-loop systems | High-severity incidents pause for approval before report generation. |
| Durable workflows | Checkpoint and resume semantics are built into the workflow design. |
| Checkpointing | `MemorySaver` persists workflow state during interrupt/resume execution. |
| Interrupt/Resume | Approval node pauses with `interrupt()` and resumes with `Command(resume=...)`. |
| Workflow routing | Severity and approval status determine graph transitions. |
| Structured observability | JSON event logs, trace IDs, tool timing, failures, token usage, and LLM call counts. |
| Custom evaluations | JSON cases and scoring logic validate extracted investigation facts. |
| Failure handling | Tool failures are logged and stored in state as failed observations. |

## What This Project Is Not

This is not a simple chatbot wrapper.

It is not a single-prompt application.

It is not limited to a single external API call.

The focus is on workflow orchestration, agent architecture, human-in-the-loop systems, evaluation, observability, and production-oriented design patterns. The design choices map to problems that show up in real AI systems.

## Current Roadmap

Completed:

- ReAct agent
- Tool calling
- Agent state management
- Structured observability
- Custom evals
- LangGraph workflow
- Checkpointing with in-memory persistence
- Interrupts
- Resume flow
- Human approvals

Planned:

- PostgreSQL checkpoint persistence
- Workflow runs database
- FastAPI service layer hardening
- Next.js dashboard
- Workflow visualization
- Authentication
- Docker deployment
- Workflow observability dashboard

## Running Locally

Install dependencies:

```bash
pip install -r requirements.txt
```

The project expects:

- A local PostgreSQL database named `incident_management`
- Incident and event tables compatible with `app/tools/incident_tools.py`
- An Anthropic API key available in the environment for the planner model

Run the evaluation harness:

```bash
python evals/run_evals.py
```

Run the LangGraph workflow example:

```bash
python langgraph/test_workflow.py
```

## Repository Structure

```text
app/
  main.py                  FastAPI entrypoints in progress
  runtime.py               ReAct agent loop and state
  planner.py               LLM planner and tool schemas
  logger.py                JSON event logging
  db.py                    PostgreSQL connection helper
  services/                Facts extraction, analysis, approval, reporting
  schemas/                 Pydantic models for facts and analysis
  tools/                   Incident retrieval tools and registry
  utils/                   Runtime helper utilities

langgraph/
  workflow.py              StateGraph definition and checkpointer
  nodes.py                 Workflow nodes and route functions
  state.py                 Workflow state type
  test_workflow.py         Interrupt/resume workflow example

evals/
  investigations.json      Evaluation cases
  run_evals.py             Evaluation runner
  scoring.py               Expected versus actual comparison
```

## Design Status

The current implementation covers the core architecture and control flow. Some infrastructure choices are still intentionally scoped:

- Checkpointing currently uses in-memory persistence.
- Logs are emitted to stdout as structured JSON.
- The evaluation harness is custom and lightweight.
- Approval handling currently runs through workflow state rather than a full user interface.
- The FastAPI surface exists, but the service layer and dashboard are still future work.

These constraints keep the system inspectable while leaving a clear path toward persistent workflow state, richer observability, authenticated APIs, and an operator dashboard.
