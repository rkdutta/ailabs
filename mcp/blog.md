# Model Context Protocol (MCP): The Standard That Makes AI Actually Useful

Modern AI assistants are impressive in isolation — but their real value comes from connecting to the systems where your work actually lives: your codebase, your database, your Slack, your docs. The problem is that every such connection has historically been a one-off engineering project. MCP fixes that.

---

## The Problem: Context Is Scattered

When an AI generates a response, it can only work with what it can "see" — its **context**. Context can be as simple as a chat history, or as complex as a distributed system spread across:

- Jira (feature descriptions)
- Databases (schema and data)
- Slack (team communication)
- Google Drive (guidelines and docs)

All of that scattered context has to be assembled and fed into the model before it can do anything useful. **Context assembly is a great toil.** Historically, every team built their own bespoke glue code to pull this off.

---

## The Integration Tax: N × M

If you have N AI chatbots and M tools, you're on the hook for N × M custom integrations. Each one requires:

- Custom API clients
- Authentication and authorization logic
- Error handling
- Ongoing maintenance and security reviews

This doesn't scale. And it's where the **Model Context Protocol** comes in.

---

## What Is MCP?

> "Giving LLMs the power of calling functions."

MCP is an open standard that defines a common protocol for AI clients (hosts) to connect to external tools and data sources. Instead of every AI tool inventing its own integration format, MCP provides a shared language.

The math changes dramatically:

```
  A: MCP Servers                          B: MCP Clients
  (Suppliers / Services)                  (AI Chatbots)

  ┌──────────────────┐                   ┌──────────────────┐
  │   Salesforce     │──┐             ┌──│   ChatGPT        │
  └──────────────────┘  │             │  └──────────────────┘
  ┌──────────────────┐  │    MCP      │  ┌──────────────────┐
  │   GitHub         │──┼─ Protocol ──┼──│   Claude         │
  └──────────────────┘  │             │  └──────────────────┘
  ┌──────────────────┐  │             │  ┌──────────────────┐
  │   Slack          │──┘             └──│   Gemini         │
  └──────────────────┘                   └──────────────────┘

       A MCP Servers  ×  B MCP Clients  =  A×B Integrations
                                           (zero custom code per pair)
```

Add a new MCP Server for a service, and every MCP-compatible client can use it immediately — no additional integration work on either side.

---

## The Architecture: Host, LLM, and MCP Server

MCP introduces three distinct roles:

| Component | Role | Examples |
|-----------|------|---------|
| **Host** | The AI application the user interacts with | Claude Code, GitHub Copilot, LangChain |
| **LLM** | The model that reasons and generates responses | Gemini, GPT-4, Claude |
| **MCP Server** | A backend service wrapped in the MCP protocol | Google Drive, GitHub, Slack |

The Host contains both an LLM and an **MCP Client** — the component responsible for discovering and calling MCP Servers on the LLM's behalf.

```
  ┌────────────────────────────────────────────────────────────────────┐
  │                         HOST                                       │
  │             (Claude Code / GitHub Copilot / LangChain)             │
  │                                                                    │
  │   ┌────────────────────────────┐    ┌──────────────────────────┐   │
  │   │           LLM              │◄──►│       MCP Client         │   │
  │   │  (Gemini / GPT / Claude)   │    │    (tool dispatcher)     │   │
  │   └────────────────────────────┘    └──────────────┬───────────┘   │
  └─────────────────────────────────────────────────── ┼ ──────────────┘
                                                       │ MCP Protocol
                    ┌──────────────────────────────────┼───────────────────────┐
                    |                                  |                       |
                    ▼                                  ▼                       ▼
          ┌──────────────────┐             ┌──────────────────┐     ┌──────────────────┐
          │   MCP Server     │             │   MCP Server     │     │   MCP Server     │
          │  (Google Drive)  │             │    (GitHub)      │     │    (Slack)       │
          └──────────────────┘             └──────────────────┘     └──────────────────┘
```

### How a Request Actually Flows

When a user asks "summarise the latest PR and check if the ticket is closed":

```
   User             Host                  LLM              MCP Server
    │                 │                    │                    │
    │──1. prompt─────►│                    │                    │
    │                 │──2. forward───────►│                    │
    │                 │◄──3. "I need tool X│                    │
    │                 │    to answer this"─│                    │
    │                 │──────────4. call tool X────────────────►│
    │                 │◄─────────5. tool result─────────────────│
    │                 │──6. send result───►│                    │
    │                 │◄──7. final─────────│                    │
    │◄─8. response────│                    │                    │
```

The LLM never calls the tool directly — it tells the Host what it needs, and the Host's MCP Client does the actual work.

---

## One Client, Many Servers: The 1:1 Connection Model

Each MCP Client maintains a **dedicated 1:1 connection per server**. Think of it like a phone with multiple SIM cards — each SIM connects to exactly one provider, and they don't share state.

```
  ┌───────────────────────────────────────────────────────────────────┐
  │                         MCP Client                                │
  │                                                                   │
  │   ┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐ │
  │   │  Connection 1   │   │  Connection 2   │   │  Connection 3   │ │
  └───┴────────┬────────┴───┴────────┬────────┴───┴────────┬────────┴─┘
               │ 1:1                 │ 1:1                 │ 1:1
               ▼                     ▼                     ▼
  ┌─────────────────────┐ ┌─────────────────────┐ ┌─────────────────────┐
  │     MCP Server      │ │     MCP Server      │ │     MCP Server      │
  │   (Google Drive)    │ │      (GitHub)       │ │      (Slack)        │
  └─────────────────────┘ └─────────────────────┘ └─────────────────────┘
```

This decoupling means servers are isolated from each other — adding, removing, or updating one server has no effect on the others.

---

## What MCP Servers Expose: Primitives

Every MCP Server exposes its capabilities through three types of primitives:

### 1. Tools (dynamic)
Actions the AI can invoke. Examples: `list_files`, `get_commits`, `send_message`.

### 2. Resources (static)
Structured data the AI can read. Examples: database rows, file contents, API responses.

### 3. Prompts
Pre-built prompt templates that the server ships alongside its tools. Instead of users writing a detailed review prompt from scratch, the server provides an expert-crafted template — and every client benefits automatically.

**Example:** A GitHub MCP Server exposes a `review-pull-request` prompt:

```
   User              Host             GitHub MCP Server          LLM
    │                  │                     │                    │
    │─"review PR #42"─►│                     │                    │
    │                  │──prompts/list──────►│                    │
    │                  │◄──["review-pull-request", ...]           │
    │                  │──prompts/get────────►                    │
    │                  │  { pr_number: 42, focus: "security" }    │
    │                  │◄──rendered prompt───│                    │
    │                  │────inject into LLM context──────────────►│
    │◄──review result──│                     │                    │
```

The server is the source of truth for both *what to do* and *how to ask for it*.

Each primitive type has standard operations the client can call:

| Primitive | Operations |
|-----------|-----------|
| **Tools** | `tools/list`, `tools/call` |
| **Resources** | `resources/list`, `resources/read`, `resources/subscribe` |
| **Prompts** | `prompts/list`, `prompts/get` |

---

## The Data Layer: Why JSON-RPC 2.0, Not REST

All MCP messages are **JSON-RPC 2.0** — a lightweight RPC standard. Every interaction is one of three message types:

| Type | Direction | Purpose |
|------|-----------|---------|
| **Request** | Client → Server | Invoke an operation; expects a response |
| **Response** | Server → Client | Result or error for a prior request |
| **Notification** | Either direction | Fire-and-forget event; no response expected |

REST might seem like the obvious choice, but MCP's design makes JSON-RPC 2.0 the better fit for three reasons:

**1. MCP operations are procedure calls, not CRUD.**
REST is built around resources — you GET, POST, PUT, or DELETE a URL. MCP operations are actions: `tools/call`, `prompts/get`, `sampling/createMessage`. Forcing these into REST produces awkward patterns like `POST /tools/{name}/call` — which is just RPC in a REST costume.

**2. Transport agnosticism.**
REST is semantically tied to HTTP. JSON-RPC 2.0 is a message envelope — the same format works over `stdio`, WebSocket, or HTTP POST. This is essential for local MCP servers that run as a subprocess and communicate over standard input/output, with no HTTP layer at all.

**3. Native notifications.**
JSON-RPC 2.0 has built-in support for fire-and-forget notifications. MCP uses these for progress updates during long-running tool calls, log streaming, and resource change events. REST has no equivalent — you'd need to bolt on SSE or WebSockets as a separate concern.

---

## The Transport Layer: Local vs. Remote Servers

The transport layer is how JSON-RPC messages physically move between client and server. MCP supports two transports:

| Transport | Server type | Best for |
|-----------|-------------|---------|
| **STDIO** | Local (same machine) | Fast, secure, simple — ideal for CLI tools and plugins |
| **HTTP/SSE** | Local or Remote | Remote calls, HTTP-compatible auth and encryption |

A local file-system MCP server runs as a child process and communicates over `stdin`/`stdout`. A GitHub MCP server runs remotely and receives calls over HTTP.

---

## The Session Lifecycle

Every MCP session goes through three phases:

```
  ┌───────────────┐     ┌───────────────┐     ┌───────────────┐
  │ Initialization│────►│   Operation   │────►│   Shutdown    │
  └───────────────┘     └───────────────┘     └───────────────┘
```

### Initialization — the capability handshake

No work can begin until both sides agree on what they support:

```
   MCP Client                                MCP Server
       │──── 1. initialize ─────────────────────►│
       │        { protocolVersion, capabilities, │
       │          clientInfo }                   │
       │◄─── 2. initialize response ─────────────│
       │        { protocolVersion, capabilities, │
       │          serverInfo }                   │
       │──── 3. notifications/initialized ──────►|
                  ✅ Session is now active
```

If the protocol versions are incompatible, the server rejects the connection immediately.

### Operation — normal work

Once initialized, the client calls tools, reads resources, and fetches prompts. The server can push notifications at any time — progress updates, log messages, resource change events — without waiting for a request.

### Shutdown — clean teardown

The client always initiates shutdown, waits for in-flight requests to finish, then sends a `shutdown` request followed by an `exit` notification. If the transport drops unexpectedly, the server treats it as an implicit shutdown and cleans up.

---

## Putting It All Together

MCP's value is not any single feature — it's the whole system working together:

- **Primitives** define what servers can offer (tools, resources, prompts)
- **JSON-RPC 2.0** defines the common language for all messages
- **Transport layer** handles local and remote delivery
- **Lifecycle** guarantees clean session management end-to-end
- **1:1 connection model** keeps servers isolated and independently deployable

The result is an ecosystem where any AI client can talk to any MCP server, out of the box, with no custom glue code — and where adding a new service to the ecosystem instantly makes it available to every AI that speaks MCP.

> The N × M integration tax becomes N + M. That's the promise of MCP.
