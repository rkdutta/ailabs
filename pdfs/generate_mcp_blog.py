import os
import tempfile
from datetime import date
from fpdf import FPDF
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "model_context_protocol.pdf")


class BlogPDF(FPDF):
    """Custom PDF class with header/footer."""

    def __init__(self, title: str):
        super().__init__()
        self.doc_title = title
        self.set_auto_page_break(auto=True, margin=25)

    def header(self):
        if self.page_no() > 1:
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(128, 128, 128)
            self.cell(0, 10, self.doc_title, align="C")
            self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

    def add_title_page(self, title: str, subtitle: str, abstract: str):
        self.add_page()
        self.ln(60)
        self.set_font("Helvetica", "B", 28)
        self.set_text_color(26, 60, 110)
        self.multi_cell(0, 12, title, align="C")
        self.ln(8)
        self.set_font("Helvetica", "", 14)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, subtitle, align="C")
        self.ln(20)
        self.set_font("Helvetica", "", 11)
        self.set_text_color(60, 60, 60)
        self.multi_cell(0, 6, abstract, align="C")

    def add_section(self, heading: str):
        self.ln(8)
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(26, 60, 110)
        self.cell(0, 10, heading)
        self.ln(10)

    def add_subsection(self, heading: str):
        self.ln(4)
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(40, 80, 140)
        self.cell(0, 8, heading)
        self.ln(9)

    def add_paragraph(self, text: str):
        self.set_font("Helvetica", "", 11)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 7, text)
        self.ln(4)

    def add_quote(self, text: str):
        self.set_font("Helvetica", "I", 11)
        self.set_text_color(80, 80, 80)
        self.set_x(30)
        self.multi_cell(self.w - 60, 7, f'"{text}"')
        self.ln(4)

    def add_bullet(self, text: str):
        self.set_font("Helvetica", "", 11)
        self.set_text_color(0, 0, 0)
        x = self.get_x()
        self.set_x(x + 8)
        self.cell(5, 7, "-")
        self.multi_cell(self.w - 40 - 13, 7, text)
        self.ln(1)

    def add_table(self, headers: list[str], rows: list[list[str]], col_widths: list[float] | None = None):
        if col_widths is None:
            col_width_each = (self.w - 40) / len(headers)
            col_widths = [col_width_each] * len(headers)
        # Header row
        self.set_font("Helvetica", "B", 10)
        self.set_fill_color(26, 60, 110)
        self.set_text_color(255, 255, 255)
        for i, h in enumerate(headers):
            self.cell(col_widths[i], 8, h, border=1, fill=True, align="C")
        self.ln()
        # Data rows
        self.set_font("Helvetica", "", 10)
        self.set_text_color(0, 0, 0)
        for i, row in enumerate(rows):
            if i % 2 == 0:
                self.set_fill_color(240, 240, 240)
            else:
                self.set_fill_color(255, 255, 255)
            for j, val in enumerate(row):
                self.cell(col_widths[j], 8, str(val), border=1, fill=True, align="C")
            self.ln()
        self.ln(6)

    def add_chart(self, chart_path: str, width: int = 160):
        self.image(chart_path, x=(self.w - width) / 2, w=width)
        self.ln(8)

    def add_code_block(self, text: str):
        self.set_font("Courier", "", 9)
        self.set_text_color(30, 30, 30)
        self.set_fill_color(245, 245, 245)
        x = self.get_x()
        self.set_x(x + 5)
        w = self.w - 40 - 10
        self.multi_cell(w, 5, text, fill=True)
        self.ln(4)


def create_chart(fig, ax, filepath: str):
    """Save a matplotlib chart to a temp file for embedding."""
    fig.tight_layout()
    fig.savefig(filepath, dpi=150, bbox_inches="tight")
    plt.close(fig)


def build_integration_chart(tmpdir: str) -> str:
    """Bar chart comparing N*M vs N+M integrations."""
    filepath = os.path.join(tmpdir, "integration_chart.png")
    scenarios = ["3 clients\n5 tools", "5 clients\n10 tools", "10 clients\n20 tools", "20 clients\n50 tools"]
    n_vals = [3, 5, 10, 20]
    m_vals = [5, 10, 20, 50]
    n_times_m = [n * m for n, m in zip(n_vals, m_vals)]
    n_plus_m = [n + m for n, m in zip(n_vals, m_vals)]

    fig, ax = plt.subplots(figsize=(8, 4.5))
    x = np.arange(len(scenarios))
    width = 0.35
    bars1 = ax.bar(x - width / 2, n_times_m, width, label="Without MCP (N x M)", color="#c0392b", alpha=0.85)
    bars2 = ax.bar(x + width / 2, n_plus_m, width, label="With MCP (N + M)", color="#1a6e3c", alpha=0.85)

    ax.set_ylabel("Number of Integrations", fontsize=11)
    ax.set_title("Integration Effort: N x M vs N + M", fontsize=13, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(scenarios, fontsize=9)
    ax.legend(fontsize=10)

    for bar in bars1:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 8,
                str(int(bar.get_height())), ha="center", va="bottom", fontsize=9, fontweight="bold")
    for bar in bars2:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 8,
                str(int(bar.get_height())), ha="center", va="bottom", fontsize=9, fontweight="bold")

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    create_chart(fig, ax, filepath)
    return filepath


def build_primitives_chart(tmpdir: str) -> str:
    """Pie chart of MCP primitive types."""
    filepath = os.path.join(tmpdir, "primitives_chart.png")
    labels = ["Tools\n(Dynamic Actions)", "Resources\n(Static Data)", "Prompts\n(Templates)"]
    sizes = [50, 30, 20]
    colors = ["#2980b9", "#27ae60", "#e67e22"]
    explode = (0.05, 0.05, 0.05)

    fig, ax = plt.subplots(figsize=(6, 4.5))
    wedges, texts, autotexts = ax.pie(
        sizes, explode=explode, labels=labels, colors=colors,
        autopct="%1.0f%%", startangle=140, textprops={"fontsize": 10}
    )
    for at in autotexts:
        at.set_fontweight("bold")
        at.set_color("white")
    ax.set_title("MCP Server Primitives", fontsize=13, fontweight="bold")
    create_chart(fig, ax, filepath)
    return filepath


def build_lifecycle_chart(tmpdir: str) -> str:
    """Horizontal bar chart showing lifecycle phases."""
    filepath = os.path.join(tmpdir, "lifecycle_chart.png")
    phases = ["Initialization", "Operation", "Shutdown"]
    durations = [1, 8, 0.5]
    colors = ["#3498db", "#2ecc71", "#e74c3c"]
    descriptions = [
        "Capability handshake\n& version negotiation",
        "Tool calls, resource reads,\nprompt fetches, notifications",
        "Clean teardown &\nresource release"
    ]

    fig, ax = plt.subplots(figsize=(8, 3.5))
    bars = ax.barh(phases, durations, color=colors, height=0.5, alpha=0.85)
    for bar, desc in zip(bars, descriptions):
        ax.text(bar.get_width() + 0.15, bar.get_y() + bar.get_height() / 2,
                desc, va="center", fontsize=9)

    ax.set_xlabel("Relative Duration", fontsize=10)
    ax.set_title("MCP Session Lifecycle Phases", fontsize=13, fontweight="bold")
    ax.set_xlim(0, 12)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    create_chart(fig, ax, filepath)
    return filepath


def build_transport_comparison_chart(tmpdir: str) -> str:
    """Grouped bar chart comparing transport characteristics."""
    filepath = os.path.join(tmpdir, "transport_chart.png")

    categories = ["Speed", "Security", "Simplicity", "Remote Support", "Auth Support"]
    stdio_scores = [9, 8, 9, 1, 2]
    http_sse_scores = [6, 7, 5, 9, 9]

    fig, ax = plt.subplots(figsize=(8, 4))
    x = np.arange(len(categories))
    width = 0.3
    ax.bar(x - width / 2, stdio_scores, width, label="STDIO", color="#2980b9", alpha=0.85)
    ax.bar(x + width / 2, http_sse_scores, width, label="HTTP/SSE", color="#e67e22", alpha=0.85)

    ax.set_ylabel("Score (1-10)", fontsize=10)
    ax.set_title("Transport Layer Comparison: STDIO vs HTTP/SSE", fontsize=13, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=9)
    ax.set_ylim(0, 11)
    ax.legend(fontsize=10)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    create_chart(fig, ax, filepath)
    return filepath


def main():
    tmpdir = tempfile.mkdtemp()
    pdf = BlogPDF("Model Context Protocol (MCP): The Standard That Makes AI Actually Useful")
    pdf.alias_nb_pages()

    # --- Title Page ---
    pdf.add_title_page(
        title="Model Context Protocol (MCP):\nThe Standard That Makes AI\nActually Useful",
        subtitle=f"Published {date.today().strftime('%B %d, %Y')}",
        abstract=(
            "Modern AI assistants are impressive in isolation, but their real value comes from "
            "connecting to the systems where your work actually lives: your codebase, your database, "
            "your Slack, your docs. The problem is that every such connection has historically been "
            "a one-off engineering project. MCP fixes that. This blog explores the architecture, "
            "protocol design, and practical implementation of the Model Context Protocol."
        ),
    )

    # --- Section 1: The Problem ---
    pdf.add_page()
    pdf.add_section("1. The Problem: Context Is Scattered")
    pdf.add_paragraph(
        "When an AI generates a response, it can only work with what it can 'see' -- its context. "
        "Context can be as simple as a chat history, or as complex as a distributed system spread "
        "across multiple services. In a real-world engineering environment, context is scattered across:"
    )
    pdf.add_bullet("Jira -- feature descriptions and ticket details")
    pdf.add_bullet("Databases -- schemas, data, and migration history")
    pdf.add_bullet("Slack -- team communication and decisions")
    pdf.add_bullet("Google Drive -- guidelines, design docs, and specs")
    pdf.add_bullet("GitHub -- code, pull requests, and CI/CD pipelines")
    pdf.ln(4)
    pdf.add_paragraph(
        "All of that scattered context must be assembled and fed into the model before it can do "
        "anything useful. Context assembly is a great toil. Historically, every team built their "
        "own bespoke glue code to pull this off -- custom scripts, API wrappers, and fragile "
        "integrations that break at the worst possible time."
    )

    # --- Section 2: Integration Tax ---
    pdf.add_section("2. The Integration Tax: N x M")
    pdf.add_paragraph(
        "If you have N AI chatbots (ChatGPT, Claude, Gemini, Perplexity, etc.) and M tools "
        "(GitHub, Slack, Jira, databases, etc.), you're on the hook for N x M custom integrations. "
        "Each one requires:"
    )
    pdf.add_bullet("Custom API clients for each service")
    pdf.add_bullet("Authentication and authorization logic")
    pdf.add_bullet("Error handling and retry mechanisms")
    pdf.add_bullet("Ongoing maintenance, security reviews, and version updates")
    pdf.ln(4)
    pdf.add_paragraph(
        "This does not scale. With 5 AI clients and 10 tools, you need 50 integrations. "
        "With 20 clients and 50 tools, that's 1,000. The operational burden grows multiplicatively, "
        "and security fragmentation becomes a serious risk."
    )

    # Integration chart
    chart_path = build_integration_chart(tmpdir)
    pdf.add_chart(chart_path, width=150)

    # --- Section 3: What Is MCP? ---
    pdf.add_section("3. What Is MCP?")
    pdf.add_quote("Giving LLMs the power of calling functions.")
    pdf.add_paragraph(
        "MCP -- the Model Context Protocol -- is an open standard that defines a common protocol "
        "for AI clients (hosts) to connect to external tools and data sources. Instead of every AI "
        "tool inventing its own integration format, MCP provides a shared language."
    )
    pdf.add_paragraph(
        "The math changes dramatically. Instead of N x M custom integrations, you build N MCP clients "
        "and M MCP servers -- a total of N + M components. Add a new MCP Server for a service, and "
        "every MCP-compatible client can use it immediately. Add a new MCP Client, and it instantly "
        "gains access to every existing server. Zero additional integration work on either side."
    )

    # --- Section 4: Business Case ---
    pdf.add_section("4. The Business Case: MCP Ecosystem")
    pdf.add_paragraph(
        "The MCP ecosystem creates a powerful network effect. On the supply side, service providers "
        "(Salesforce, GitHub, Slack, Google Drive) build MCP Servers -- each wraps a tool or service "
        "behind a standard interface. On the demand side, AI chatbots (ChatGPT, Claude, Gemini) become "
        "MCP Client compliant -- they can connect to any MCP Server out of the box."
    )
    pdf.add_paragraph(
        "The result: A x B integrations with zero custom code per pair. Every new server is instantly "
        "usable by every client. Every new client gains access to every server. The ecosystem grows "
        "multiplicatively with no extra integration work. Becoming AI-native via MCPs is a strategic "
        "advantage that scales."
    )

    pdf.add_table(
        headers=["Side", "Role", "Examples"],
        rows=[
            ["MCP Servers (A)", "Wrap services behind MCP", "Salesforce, GitHub, Slack"],
            ["MCP Clients (B)", "AI apps that consume MCP", "ChatGPT, Claude, Gemini"],
            ["Integrations", "A x B with zero glue code", "Every pair works instantly"],
        ],
        col_widths=[40, 55, 75],
    )

    # --- Section 5: Architecture ---
    pdf.add_section("5. Architecture: Host, LLM, and MCP Server")
    pdf.add_paragraph(
        "MCP introduces three distinct components that work together in a layered architecture:"
    )

    pdf.add_table(
        headers=["Component", "Role", "Examples"],
        rows=[
            ["Host", "AI app the user interacts with", "Claude Code, GitHub Copilot, LangChain"],
            ["LLM", "Model that reasons & generates", "Gemini, GPT-4, Claude"],
            ["MCP Server", "Backend wrapped in MCP protocol", "Google Drive, GitHub, Slack"],
        ],
        col_widths=[35, 55, 80],
    )

    pdf.add_paragraph(
        "The Host contains both an LLM and an MCP Client -- the component responsible for "
        "discovering and calling MCP Servers on the LLM's behalf. The LLM never calls tools "
        "directly; it tells the Host what it needs, and the Host's MCP Client does the actual work."
    )

    pdf.add_subsection("Request Dataflow: 8-Step Process")
    pdf.add_paragraph(
        "When a user asks something like 'summarize the latest PR and check if the ticket is closed', "
        "the request flows through all three components:"
    )

    pdf.add_table(
        headers=["Step", "Direction", "Action"],
        rows=[
            ["1", "User -> Host", "User sends prompt"],
            ["2", "Host -> LLM", "Host forwards prompt to LLM"],
            ["3", "LLM -> Host", "LLM requests tool call (not a final answer)"],
            ["4", "Host -> MCP Server", "MCP Client calls the appropriate server"],
            ["5", "MCP Server -> Host", "Server returns tool result"],
            ["6", "Host -> LLM", "Host sends tool result as additional context"],
            ["7", "LLM -> Host", "LLM generates final response"],
            ["8", "Host -> User", "Host delivers response to user"],
        ],
        col_widths=[15, 45, 110],
    )

    # --- Section 6: 1:1 Connection Model ---
    pdf.add_section("6. The 1:1 Connection Model")
    pdf.add_paragraph(
        "Each MCP Client maintains a dedicated 1:1 connection per server. The client manages "
        "multiple such connections, but each channel is exclusive to one server -- servers are "
        "never shared across connections. Think of it like a mobile phone with multiple SIM cards: "
        "each SIM connects to exactly one provider, and they don't share state."
    )
    pdf.add_paragraph("This design delivers two key benefits:")
    pdf.add_bullet(
        "Decoupling -- servers are isolated from each other. Adding, removing, or updating one "
        "server has no effect on the others."
    )
    pdf.add_bullet(
        "Parallelism -- multiple tool calls to different servers can execute concurrently without "
        "contention or shared state."
    )

    # --- Section 7: MCP Primitives ---
    pdf.add_page()
    pdf.add_section("7. MCP Primitives")
    pdf.add_paragraph(
        "Every MCP Server exposes its capabilities through three types of primitives:"
    )

    pdf.add_subsection("7.1 Tools (Dynamic)")
    pdf.add_paragraph(
        "Actions the AI can invoke on the server. Examples: list_files, get_commits, send_message. "
        "Tools are the primary way LLMs interact with external systems -- they represent the verbs "
        "of the MCP vocabulary."
    )

    pdf.add_subsection("7.2 Resources (Static)")
    pdf.add_paragraph(
        "Structured data the AI can read. Examples: database rows, file contents, API responses. "
        "Resources represent the nouns -- the data that tools operate on or that the LLM needs "
        "for context."
    )

    pdf.add_subsection("7.3 Prompts")
    pdf.add_paragraph(
        "Pre-built prompt templates that the server ships alongside its tools. Instead of users "
        "writing a detailed review prompt from scratch, the server provides an expert-crafted "
        "template -- and every client benefits automatically. This ensures reliability and "
        "consistent output quality across all AI clients."
    )

    # Primitives chart
    chart_path = build_primitives_chart(tmpdir)
    pdf.add_chart(chart_path, width=120)

    pdf.add_subsection("Prompt Primitive Example: GitHub Code Review")
    pdf.add_paragraph(
        "A GitHub MCP Server exposes a 'review-pull-request' prompt. When a user says "
        "'review PR #42', the Host fetches the template from the server, fills in the arguments "
        "(pr_number=42, focus='security'), and injects the rendered prompt into the LLM context. "
        "The user gets an expert-quality review without writing a single line of prompt engineering."
    )

    pdf.add_table(
        headers=["Without Prompt Primitive", "With Prompt Primitive"],
        rows=[
            ["User writes detailed review prompt", "Host fetches template automatically"],
            ["Prompt quality varies per client", "Server ships expert prompts"],
            ["Every client re-implements logic", "Update once, all clients benefit"],
        ],
        col_widths=[85, 85],
    )

    # --- Section 8: Standard Operations ---
    pdf.add_section("8. Standard Operations")
    pdf.add_paragraph(
        "Each primitive type has standard operations that the client can call via JSON-RPC 2.0:"
    )

    pdf.add_table(
        headers=["Primitive", "Operation", "Description"],
        rows=[
            ["Tools", "tools/list", "Discover available tools"],
            ["Tools", "tools/call", "Invoke a tool with arguments"],
            ["Resources", "resources/list", "List available resources"],
            ["Resources", "resources/read", "Read a specific resource"],
            ["Resources", "resources/subscribe", "Watch for resource changes"],
            ["Prompts", "prompts/list", "List available prompt templates"],
            ["Prompts", "prompts/get", "Retrieve a rendered prompt"],
        ],
        col_widths=[35, 55, 80],
    )

    # --- Section 9: Data Layer ---
    pdf.add_section("9. Data Layer: Why JSON-RPC 2.0, Not REST")
    pdf.add_paragraph(
        "All MCP messages use JSON-RPC 2.0 -- a lightweight RPC standard. Every interaction is one "
        "of three message types: Request (client to server, expects response), Response (server to "
        "client, result or error), or Notification (either direction, fire-and-forget)."
    )
    pdf.add_paragraph(
        "REST might seem like the obvious choice, but MCP's design makes JSON-RPC 2.0 the better "
        "fit for three reasons:"
    )

    pdf.add_subsection("Reason 1: Procedure Calls, Not CRUD")
    pdf.add_paragraph(
        "REST is built around resources -- you GET, POST, PUT, or DELETE a URL. MCP operations "
        "are actions: tools/call, prompts/get, sampling/createMessage. Forcing these into REST "
        "produces awkward patterns like POST /tools/{name}/call -- which is just RPC in a REST costume."
    )

    pdf.add_subsection("Reason 2: Transport Agnosticism")
    pdf.add_paragraph(
        "REST is semantically tied to HTTP. JSON-RPC 2.0 is a message envelope -- the same format "
        "works over stdio, WebSocket, or HTTP POST. This is essential for local MCP servers that "
        "run as a subprocess and communicate over standard input/output, with no HTTP layer at all."
    )

    pdf.add_subsection("Reason 3: Native Notifications")
    pdf.add_paragraph(
        "JSON-RPC 2.0 has built-in support for fire-and-forget notifications. MCP uses these for "
        "progress updates during long-running tool calls, log streaming, and resource change events. "
        "REST has no native equivalent -- you'd need to bolt on SSE or WebSockets as a separate concern."
    )

    pdf.add_table(
        headers=["Aspect", "REST", "JSON-RPC 2.0"],
        rows=[
            ["Mental model", "Nouns (resources)", "Verbs (procedures)"],
            ["Transport", "HTTP only", "Any: stdio, WS, HTTP"],
            ["Bidirectional", "No", "Yes (notifications)"],
            ["Batching", "Not standard", "Built-in"],
            ["MCP fit", "Awkward", "Natural"],
        ],
        col_widths=[40, 65, 65],
    )

    # --- Section 10: Transport Layer ---
    pdf.add_section("10. Transport Layer: Local vs. Remote")
    pdf.add_paragraph(
        "The transport layer is how JSON-RPC messages physically move between client and server. "
        "MCP supports two transports, each suited to different deployment scenarios:"
    )

    pdf.add_table(
        headers=["Transport", "Server Type", "Best For"],
        rows=[
            ["STDIO", "Local (same machine)", "Fast, secure, simple -- CLI tools & plugins"],
            ["HTTP/SSE", "Local or Remote", "Remote calls, HTTP-compatible auth & encryption"],
        ],
        col_widths=[40, 50, 80],
    )

    pdf.add_paragraph(
        "A local file-system MCP server runs as a child process and communicates over stdin/stdout. "
        "A GitHub MCP server runs remotely and receives calls over HTTP. SSE (Server-Sent Events) "
        "enables streaming -- sending data incrementally over a single open connection."
    )

    # Transport chart
    chart_path = build_transport_comparison_chart(tmpdir)
    pdf.add_chart(chart_path, width=150)

    # --- Section 11: Lifecycle ---
    pdf.add_section("11. MCP Session Lifecycle")
    pdf.add_paragraph(
        "Every MCP session passes through three phases in order: Initialization, Operation, and "
        "Shutdown. This guarantees that both sides know each other's capabilities before any work "
        "begins, and that every session closes cleanly."
    )

    pdf.add_subsection("Phase 1: Initialization")
    pdf.add_paragraph(
        "A three-step handshake establishes a shared understanding of what both sides can do. "
        "The client sends its protocol version and capabilities, the server responds with its own, "
        "and the client confirms with a notifications/initialized message. If protocol versions "
        "are incompatible, the server rejects the connection immediately. No tool calls or resource "
        "reads can happen until initialization completes."
    )

    pdf.add_subsection("Phase 2: Operation")
    pdf.add_paragraph(
        "Once initialized, the client calls tools, reads resources, and fetches prompts. The server "
        "can push notifications at any time -- progress updates, log messages, resource change "
        "events -- without waiting for a request. This is where all the real work happens."
    )

    pdf.add_subsection("Phase 3: Shutdown")
    pdf.add_paragraph(
        "The client always initiates shutdown. It waits for in-flight requests to finish, sends a "
        "shutdown request, then sends an exit notification. If the transport drops unexpectedly "
        "(crash, network loss), the server treats it as an implicit shutdown and releases all "
        "session resources."
    )

    # Lifecycle chart
    chart_path = build_lifecycle_chart(tmpdir)
    pdf.add_chart(chart_path, width=150)

    # --- Section 12: Libraries ---
    pdf.add_section("12. MCP Libraries and FastAPI Compatibility")
    pdf.add_paragraph(
        "Currently there are two main libraries for implementing MCP servers and clients:"
    )

    pdf.add_table(
        headers=["Library", "Source", "Version", "Notes"],
        rows=[
            ["mcp", "Anthropic (official SDK)", "Includes FastMCP 1.0", "pip install mcp"],
            ["fastmcp", "Community fork", "v2.0", "pip install fastmcp"],
        ],
        col_widths=[30, 50, 45, 45],
    )

    pdf.add_paragraph(
        "Both libraries share the same interfaces and are largely code-compatible. Notably, "
        "FastMCP is designed to be compatible with FastAPI by design. If a company has an existing "
        "FastAPI server, it can be wrapped as an MCP server with minimal effort:"
    )

    pdf.add_code_block(
        'from main import app  # existing FastAPI application\n'
        'from fastmcp import FastMCP\n\n'
        'mcp = FastMCP.from_fastapi(app=app, name="mymcp")\n'
        '# Now the existing app is MCP-compatible!'
    )

    # --- Section 13: Demo Examples ---
    pdf.add_section("13. Demo: Building MCP Servers")

    pdf.add_subsection("Demo 1: Simple Server (add & greet)")
    pdf.add_paragraph(
        "The simplest MCP server exposes basic tools using the @mcp.tool() decorator. "
        "Each function becomes a callable tool that any MCP client can discover and invoke:"
    )
    pdf.add_code_block(
        'from fastmcp import FastMCP\n\n'
        'mcp = FastMCP("Demo Server")\n\n'
        '@mcp.tool()\n'
        'def add(a: int, b: int) -> int:\n'
        '    """Add two numbers together."""\n'
        '    return a + b\n\n'
        '@mcp.tool()\n'
        'def greet(name: str) -> str:\n'
        '    """Return a greeting for the given name."""\n'
        '    return f"Hello, {name}!"\n\n'
        'if __name__ == "__main__":\n'
        '    mcp.run()'
    )

    pdf.add_subsection("Demo 2: Expense Tracker with SQLite")
    pdf.add_paragraph(
        "A more realistic example: an expense tracker MCP server backed by SQLite. It exposes "
        "full CRUD operations as MCP tools, allowing any AI client to manage expenses through "
        "natural language:"
    )

    pdf.add_table(
        headers=["Tool", "Parameters", "Description"],
        rows=[
            ["add_expense", "description, amount", "Add a new expense"],
            ["get_expenses", "(none)", "List all expenses"],
            ["update_expense", "id, description, amount", "Update an expense"],
            ["delete_expense", "expense_id", "Delete an expense by ID"],
            ["get_total_expenses", "(none)", "Sum of all expenses"],
            ["get_expenses_by_date", "start_date, end_date", "Filter by date range"],
        ],
        col_widths=[50, 50, 70],
    )

    pdf.add_paragraph(
        "The server initializes a SQLite database on startup and each tool function handles "
        "its own database connection. This pattern -- wrapping an existing data store behind "
        "MCP tool decorators -- is the most common way to build production MCP servers."
    )

    # --- Conclusion ---
    pdf.add_page()
    pdf.add_section("Conclusion: Key Takeaways")
    pdf.add_paragraph(
        "MCP's value is not any single feature -- it's the whole system working together:"
    )
    pdf.add_bullet("Primitives define what servers can offer: tools, resources, and prompts.")
    pdf.add_bullet("JSON-RPC 2.0 defines the common language for all messages.")
    pdf.add_bullet("The transport layer handles local (STDIO) and remote (HTTP/SSE) delivery.")
    pdf.add_bullet("The lifecycle guarantees clean session management end-to-end.")
    pdf.add_bullet("The 1:1 connection model keeps servers isolated and independently deployable.")
    pdf.ln(6)
    pdf.add_paragraph(
        "The result is an ecosystem where any AI client can talk to any MCP server, out of the box, "
        "with no custom glue code. Adding a new service to the ecosystem instantly makes it available "
        "to every AI that speaks MCP."
    )
    pdf.ln(4)
    pdf.add_quote("The N x M integration tax becomes N + M. That's the promise of MCP.")

    # --- Output ---
    pdf.output(OUTPUT_PATH)
    print(f"PDF generated: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
