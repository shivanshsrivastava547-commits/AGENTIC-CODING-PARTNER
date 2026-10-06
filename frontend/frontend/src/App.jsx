import { useState, useRef, useEffect } from "react";
import { ingestRepo, sendMessage } from "./services/api";
import "./App.css";

const AGENT_CONFIG = {
  architecture: { label: "Architecture", color: "#a78bfa", icon: "⬡", bg: "rgba(167,139,250,0.12)" },
  code_generation: { label: "Code Gen", color: "#60a5fa", icon: "⌨", bg: "rgba(96,165,250,0.12)" },
  testing: { label: "Testing", color: "#34d399", icon: "✓", bg: "rgba(52,211,153,0.12)" },
  review: { label: "PR Review", color: "#fb923c", icon: "⊙", bg: "rgba(251,146,60,0.12)" },
  debug: { label: "Debug", color: "#f87171", icon: "⚡", bg: "rgba(248,113,113,0.12)" },
  documentation: { label: "Docs", color: "#22d3ee", icon: "⊞", bg: "rgba(34,211,238,0.12)" },
  issue: { label: "Issue", color: "#f472b6", icon: "◎", bg: "rgba(244,114,182,0.12)" },
  error: { label: "Error", color: "#f87171", icon: "✕", bg: "rgba(248,113,113,0.12)" },
  default: { label: "Agent", color: "#94a3b8", icon: "◈", bg: "rgba(148,163,184,0.12)" },
};

const FEATURE_CARDS = [
  { icon: "⬡", color: "#a78bfa", title: "Architecture Analysis", desc: "Map dependencies, layers, and system design across your entire codebase." },
  { icon: "⌨", color: "#60a5fa", title: "Code Generation", desc: "Generate production-quality code, functions, and modules from plain language." },
  { icon: "✓", color: "#34d399", title: "Automated Testing", desc: "Write unit, integration, and E2E tests with full coverage in seconds." },
  { icon: "⊙", color: "#fb923c", title: "PR Review", desc: "Get detailed code reviews with suggestions, risks, and improvement paths." },
  { icon: "⊞", color: "#22d3ee", title: "Documentation", desc: "Auto-generate READMEs, API docs, and inline comments from source code." },
  { icon: "◎", color: "#f472b6", title: "Issue Resolution", desc: "Diagnose bugs, trace root causes, and get actionable fix suggestions." },
];

const DEMO_PROMPTS = [
  { label: "Explain the architecture", prompt: "Explain the architecture of this codebase", agent: "architecture" },
  { label: "Generate unit tests", prompt: "Generate unit tests for the main backend routes", agent: "testing" },
  { label: "Add JWT middleware", prompt: "Create a JWT authentication middleware for this project", agent: "code_generation" },
  { label: "Suggest improvements", prompt: "Review this project and suggest improvements", agent: "review" },
  { label: "Write a README", prompt: "Generate a professional README for this project", agent: "documentation" },
];

function getAgentInfo(agent) {
  if (!agent) return AGENT_CONFIG.default;
  const key = Object.keys(AGENT_CONFIG).find(k => agent.toLowerCase().includes(k.replace("_", ""))) || "default";
  return AGENT_CONFIG[key] || AGENT_CONFIG.default;
}

function AgentBadge({ agent }) {
  const info = getAgentInfo(agent);
  return (
    <span className="agentBadge" style={{ color: info.color, background: info.bg, borderColor: `${info.color}33` }}>
      <span className="agentIcon">{info.icon}</span>
      {info.label}
    </span>
  );
}

function Message({ msg }) {
  const isUser = msg.role === "user";
  return (
    <div className={`message ${isUser ? "user" : "ai"}`}>
      {!isUser && msg.agent && <AgentBadge agent={msg.agent} />}
      <div className="messageBubble">
        <pre className="messageText">{msg.text}</pre>
      </div>
    </div>
  );
}

function EmptyState({ onPromptClick }) {
  return (
    <div className="emptyState">
      <div className="heroGlow" />
      <div className="heroOrb" />
      <div className="heroContent">
        <div className="heroBadge">Multi-Agent Copilot</div>
        <h1 className="heroTitle">Your codebase,<br /><span className="heroGradient">fully understood.</span></h1>
        <p className="heroSubtitle">
          Index any GitHub repository. Ask anything. Seven specialized agents collaborate to answer with depth and precision.
        </p>
        <div className="featureGrid">
          {FEATURE_CARDS.map((card) => (
            <div className="featureCard" key={card.title} style={{ "--card-color": card.color }}>
              <span className="featureIcon" style={{ color: card.color }}>{card.icon}</span>
              <div>
                <div className="featureTitle">{card.title}</div>
                <div className="featureDesc">{card.desc}</div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

function RepoCard({ url, status }) {
  const short = url.replace("https://github.com/", "");
  return (
    <div className="repoCard">
      <div className="repoCardHeader">
        <span className="repoCardIcon">⎇</span>
        <span className="repoCardLabel">Indexed Repository</span>
        <span className="repoStatusDot" />
      </div>
      <div className="repoCardUrl">{short}</div>
      {status && <div className="repoCardStatus">{status}</div>}
    </div>
  );
}

export default function App() {
  const [repoUrl, setRepoUrl] = useState("");
  const [repoStatus, setRepoStatus] = useState("");
  const [indexedRepo, setIndexedRepo] = useState("");
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [indexing, setIndexing] = useState(false);
  const [agentActivity, setAgentActivity] = useState(null);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const handleIngest = async () => {
    if (!repoUrl.trim()) { setRepoStatus("Enter a GitHub repository URL."); return; }
    try {
      setIndexing(true);
      setRepoStatus("Indexing…");
      const res = await ingestRepo(repoUrl);
      if (res.data.success === false) {
        setRepoStatus(res.data.error || res.data.message);
      } else {
        setIndexedRepo(repoUrl);
        setRepoStatus(`${res.data.total_files} files · ${res.data.chunks || "—"} chunks`);
      }
    } catch (err) {
      setRepoStatus(err.response?.data?.error || "Failed to index repository.");
    } finally {
      setIndexing(false);
    }
  };

  const handleSend = async () => {
    if (!query.trim()) return;
    const currentQuery = query;
    setMessages(prev => [...prev, { role: "user", text: currentQuery }]);
    setQuery("");
    setLoading(true);
    setAgentActivity("Routing…");
    try {
      const res = await sendMessage(currentQuery);
      setAgentActivity(res.data.agent_used || null);
      if (res.data.success === false) {
        setMessages(prev => [...prev, { role: "ai", text: res.data.error || "Chat failed.", agent: "error" }]);
      } else {
        setMessages(prev => [...prev, { role: "ai", text: res.data.response, agent: res.data.agent_used }]);
      }
    } catch (err) {
      setMessages(prev => [...prev, { role: "ai", text: err.response?.data?.error || "Something went wrong.", agent: "error" }]);
    } finally {
      setLoading(false);
      setTimeout(() => setAgentActivity(null), 2000);
    }
  };

  return (
    <div className="app">
      <div className="bgGrid" />
      <div className="bgBlob blob1" />
      <div className="bgBlob blob2" />
      <div className="bgBlob blob3" />

      {/* SIDEBAR */}
      <aside className="sidebar">
        <div className="sidebarLogo">
          <div className="logoMark">
            <span className="logoHex">⬡</span>
          </div>
          <div>
            <div className="logoName">DevGraph<span className="logoAi">AI</span></div>
            <div className="logoTagline">Engineering Copilot</div>
          </div>
        </div>

        <div className="sidebarSection">
          <div className="sectionLabel">Repository</div>
          <div className="inputGroup">
            <input
              className="repoInput"
              placeholder="github.com/owner/repo"
              value={repoUrl}
              onChange={e => setRepoUrl(e.target.value)}
              onKeyDown={e => e.key === "Enter" && handleIngest()}
            />
            <button className="indexBtn" onClick={handleIngest} disabled={indexing}>
              {indexing ? <span className="spinner" /> : "Index"}
            </button>
          </div>
          {repoStatus && !indexedRepo && (
            <div className="statusMsg">{repoStatus}</div>
          )}
          {indexedRepo && <RepoCard url={indexedRepo} status={repoStatus} />}
        </div>

        <div className="sidebarSection">
          <div className="sectionLabel">Quick Prompts</div>
          <div className="promptList">
            {DEMO_PROMPTS.map((p) => {
              const info = getAgentInfo(p.agent);
              return (
                <button key={p.label} className="promptBtn" onClick={() => setQuery(p.prompt)}>
                  <span className="promptIcon" style={{ color: info.color }}>{info.icon}</span>
                  <span>{p.label}</span>
                </button>
              );
            })}
          </div>
        </div>

        <div className="sidebarSection">
          <div className="sectionLabel">Agents</div>
          <div className="agentList">
            {Object.entries(AGENT_CONFIG).filter(([k]) => k !== "error" && k !== "default").map(([key, info]) => (
              <div key={key} className="agentListItem">
                <span className="agentDot" style={{ background: info.color }} />
                <span className="agentListLabel">{info.label}</span>
                <span className="agentListIcon" style={{ color: info.color }}>{info.icon}</span>
              </div>
            ))}
          </div>
        </div>
      </aside>

      {/* MAIN */}
      <div className="mainWrapper">
        {/* HEADER */}
        <header className="topHeader">
          <div className="headerLeft">
            <h1 className="headerTitle">Codebase Copilot</h1>
            <p className="headerSub">Powered by LangGraph · ChromaDB · Groq</p>
          </div>
          <div className="headerRight">
            {agentActivity && (
              <div className="agentActivityPill">
                <span className="pulsingDot" />
                <span>{agentActivity}</span>
              </div>
            )}
            {indexedRepo && (
              <div className="headerRepoPill">
                <span className="repoPillDot" />
                <span className="repoPillText">{indexedRepo.replace("https://github.com/", "")}</span>
              </div>
            )}
          </div>
        </header>

        {/* MESSAGES */}
        <main className="chat">
          {messages.length === 0 ? (
            <EmptyState onPromptClick={setQuery} />
          ) : (
            <div className="messageList">
              {messages.map((msg, i) => <Message key={i} msg={msg} />)}
              {loading && (
                <div className="message ai">
                  <div className="thinkingBubble">
                    <span className="dot" /><span className="dot" /><span className="dot" />
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>
          )}
        </main>

        {/* INPUT */}
        <div className="inputArea">
          {!indexedRepo && (
            <div className="inputWarning">⚠ Index a repository first to enable the copilot.</div>
          )}
          <div className="inputRow">
            <input
              className="chatInput"
              placeholder={indexedRepo ? "Ask about the codebase…" : "Index a repo to get started"}
              value={query}
              onChange={e => setQuery(e.target.value)}
              onKeyDown={e => e.key === "Enter" && !loading && handleSend()}
              disabled={loading || !indexedRepo}
            />
            <button className="sendBtn" onClick={handleSend} disabled={loading || !indexedRepo || !query.trim()}>
              {loading ? <span className="spinner white" /> : <SendIcon />}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

function SendIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
      <line x1="22" y1="2" x2="11" y2="13" />
      <polygon points="22 2 15 22 11 13 2 9 22 2" />
    </svg>
  );
}