import { useEffect, useMemo, useState } from "react";
import {
  Activity,
  CheckCircle2,
  ChevronRight,
  CircleHelp,
  FileAudio,
  Menu,
  MessageSquareText,
  Play,
  Search,
  Settings2,
  Sparkles,
  Upload,
  Users,
  X,
} from "lucide-react";

const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";
const DEMO_SESSION_ID = "frontend-demo-session";

const demoTranscript = [
  {
    segment_id: "frontend-demo-001",
    revision: 1,
    is_final: true,
    start_ms: 0,
    end_ms: 3200,
    speaker_id: "SPEAKER_00",
    text: "We will ship the audio pipeline on Friday.",
    asr_confidence: 0.98,
  },
  {
    segment_id: "frontend-demo-002",
    revision: 1,
    is_final: true,
    start_ms: 3200,
    end_ms: 6100,
    speaker_id: "SPEAKER_01",
    text: "Priya owns the release checklist and will send it before the review.",
    asr_confidence: 0.96,
  },
  {
    segment_id: "frontend-demo-003",
    revision: 1,
    is_final: true,
    start_ms: 6100,
    end_ms: 9100,
    speaker_id: "SPEAKER_00",
    text: "Let us keep the launch decision open until QA finishes.",
    asr_confidence: 0.94,
  },
];

const initialSessions = [
  { id: DEMO_SESSION_ID, title: "Audio pipeline launch", date: "Today", status: "Live", color: "violet" },
  { id: "planning-session", title: "Product planning sync", date: "Yesterday", status: "Ready", color: "blue" },
  { id: "research-session", title: "Research review", date: "Oct 18", status: "Ready", color: "amber" },
];

function formatTime(milliseconds) {
  const seconds = Math.floor(milliseconds / 1000);
  return `${String(Math.floor(seconds / 60)).padStart(2, "0")}:${String(seconds % 60).padStart(2, "0")}`;
}

function App() {
  const [sessions] = useState(initialSessions);
  const [activeSession, setActiveSession] = useState(DEMO_SESSION_ID);
  const [transcript, setTranscript] = useState([]);
  const [query, setQuery] = useState("");
  const [answer, setAnswer] = useState("");
  const [apiStatus, setApiStatus] = useState("checking");
  const [notice, setNotice] = useState("");
  const [mobileNav, setMobileNav] = useState(false);

  const active = sessions.find((session) => session.id === activeSession) || sessions[0];
  const filteredTranscript = useMemo(() => {
    const normalized = query.trim().toLowerCase();
    if (!normalized) return transcript;
    return transcript.filter((item) => item.text.toLowerCase().includes(normalized));
  }, [query, transcript]);

  useEffect(() => {
    checkApi();
    loadTranscript(DEMO_SESSION_ID);
  }, []);

  async function checkApi() {
    try {
      const response = await fetch(`${API_BASE}/health`);
      setApiStatus(response.ok ? "online" : "offline");
    } catch {
      setApiStatus("offline");
    }
  }

  async function loadTranscript(sessionId) {
    setActiveSession(sessionId);
    try {
      const response = await fetch(`${API_BASE}/v1/sessions/${sessionId}/transcript-segments`);
      if (!response.ok) throw new Error("Transcript unavailable");
      const payload = await response.json();
      setTranscript(payload.segments || []);
      setNotice("");
    } catch {
      setTranscript(sessionId === DEMO_SESSION_ID ? demoTranscript : []);
      setNotice("Showing the local demo transcript while the API is unavailable.");
    }
  }

  async function seedDemoSession() {
    setNotice("Sending demo transcript to the backend…");
    try {
      for (const [index, segment] of demoTranscript.entries()) {
        await fetch(`${API_BASE}/v1/transcript-segments`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            schema_version: "1.0",
            event_id: `frontend-demo-event-${index + 1}`,
            session_id: DEMO_SESSION_ID,
            created_at: new Date().toISOString(),
            payload: segment,
          }),
        });
      }
      setApiStatus("online");
      await loadTranscript(DEMO_SESSION_ID);
      setNotice("Demo transcript synced to PostgreSQL through FastAPI.");
    } catch {
      setTranscript(demoTranscript);
      setNotice("Backend unavailable; the demo transcript is still available locally.");
    }
  }

  function askQuestion(event) {
    event.preventDefault();
    const normalized = query.trim().toLowerCase();
    if (!normalized) return setAnswer("");
    const matches = transcript.filter((item) => item.text.toLowerCase().includes(normalized));
    setAnswer(matches.length
      ? `I found ${matches.length} cited transcript ${matches.length === 1 ? "segment" : "segments"} mentioning “${query.trim()}”.`
      : "No matching evidence was found in this session yet.");
  }

  return (
    <div className="app-shell">
      <aside className={`sidebar ${mobileNav ? "sidebar-open" : ""}`}>
        <div className="brand-row">
          <div className="brand-mark"><Sparkles size={17} /></div>
          <span>recall</span>
          <button className="icon-button close-nav" onClick={() => setMobileNav(false)} aria-label="Close navigation"><X size={18} /></button>
        </div>
        <button className="new-session" onClick={seedDemoSession}><Upload size={17} /> Import recording</button>
        <div className="nav-label">Workspace</div>
        <nav>
          <button className="nav-item active"><Activity size={17} /> Overview</button>
          <button className="nav-item"><MessageSquareText size={17} /> Ask your memory <span className="nav-pill">AI</span></button>
          <button className="nav-item"><Users size={17} /> People & topics</button>
        </nav>
        <div className="nav-label session-label">Recent sessions</div>
        <div className="session-list">
          {sessions.map((session) => (
            <button key={session.id} className={`session-item ${session.id === activeSession ? "selected" : ""}`} onClick={() => loadTranscript(session.id)}>
              <span className={`session-dot ${session.color}`} />
              <span className="session-copy"><strong>{session.title}</strong><small>{session.date}</small></span>
              {session.status === "Live" && <span className="live-dot" />}
            </button>
          ))}
        </div>
        <div className="sidebar-footer"><button className="nav-item"><Settings2 size={17} /> Settings</button><button className="nav-item"><CircleHelp size={17} /> Help center</button></div>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <button className="icon-button menu-button" onClick={() => setMobileNav(true)} aria-label="Open navigation"><Menu size={20} /></button>
          <div className="breadcrumbs"><span>Overview</span><ChevronRight size={14} /><strong>{active.title}</strong></div>
          <div className="topbar-actions"><span className={`api-indicator ${apiStatus}`}><span /> API {apiStatus === "online" ? "online" : apiStatus === "offline" ? "offline" : "checking"}</span><div className="avatar">HV</div></div>
        </header>

        <div className="content-wrap">
          <section className="hero-row"><div><div className="eyebrow">{active.status === "Live" ? "Live session" : "Session recap"}</div><h1>{active.title}</h1><p className="muted">Your meeting memory, organized as it happens.</p></div><button className="secondary-button" onClick={seedDemoSession}><Play size={16} /> Sync demo</button></section>
          {notice && <div className="notice"><CheckCircle2 size={16} /> {notice}</div>}

          <section className="metric-grid"><div className="metric-card"><span className="metric-icon violet-bg"><MessageSquareText size={17} /></span><div><span className="metric-label">Transcript turns</span><strong>{transcript.length || "—"}</strong></div></div><div className="metric-card"><span className="metric-icon blue-bg"><Users size={17} /></span><div><span className="metric-label">Speakers detected</span><strong>{new Set(transcript.map((item) => item.speaker_id)).size || "—"}</strong></div></div><div className="metric-card"><span className="metric-icon amber-bg"><CheckCircle2 size={17} /></span><div><span className="metric-label">Evidence coverage</span><strong>{transcript.length ? "100%" : "—"}</strong></div></div></section>

          <section className="workspace-grid"><div className="panel transcript-panel"><div className="panel-heading"><div><span className="panel-kicker">Source evidence</span><h2>Transcript</h2></div><div className="panel-actions"><span className="confidence-label">{transcript.length ? "Synced" : "Waiting"}</span><button className="icon-button"><FileAudio size={17} /></button></div></div><div className="search-box"><Search size={16} /><input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search this transcript…" /></div><div className="transcript-list">{filteredTranscript.length ? filteredTranscript.map((item) => <article className="transcript-row" key={`${item.segment_id}-${item.revision}`}><time>{formatTime(item.start_ms)}</time><div className="speaker-chip">{item.speaker_id.replace("SPEAKER_", "S")}</div><p>{item.text}</p><span className="confidence">{Math.round((item.asr_confidence || 0) * 100)}%</span></article>) : <div className="empty-state"><FileAudio size={25} /><strong>No transcript loaded</strong><span>Sync the demo session or start the backend.</span></div>}</div></div>

            <div className="right-column"><div className="panel summary-panel"><div className="panel-heading"><div><span className="panel-kicker">AI synthesis</span><h2>Running summary</h2></div><span className="sparkle-badge"><Sparkles size={14} /> Live</span></div><p className="summary-text">The team is preparing to ship the audio pipeline on Friday. Priya owns the release checklist, while the final launch decision remains open until QA finishes.</p><div className="citation"><span className="citation-bar" /><div><strong>Based on 3 transcript turns</strong><small>Evidence-linked summary</small></div></div></div><div className="panel actions-panel"><div className="panel-heading"><div><span className="panel-kicker">Follow-up</span><h2>Action items</h2></div><span className="count-badge">1</span></div><div className="action-item"><span className="check-box" /><div><strong>Ship the audio pipeline</strong><span>Due Friday · Owner unresolved</span></div><span className="status-open">Open</span></div></div></div></section>

          <section className="ask-panel"><div className="ask-copy"><span className="ask-icon"><Sparkles size={18} /></span><div><span className="panel-kicker">Across your memory</span><h2>Ask about this meeting</h2><p>Search the evidence captured in this session.</p></div></div><form onSubmit={askQuestion} className="ask-form"><input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="What did we decide about the launch?" /><button type="submit">Ask <ChevronRight size={16} /></button></form>{answer && <div className="answer"><strong>Answer</strong><span>{answer}</span></div>}</section>
        </div>
      </main>
    </div>
  );
}

export default App;
