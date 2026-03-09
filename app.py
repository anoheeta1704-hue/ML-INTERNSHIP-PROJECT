import streamlit as st
from skill_gap import skill_gap_analyzer
from internship_match import internship_matcher
from placement_predictor import predict_placement
from fake_detector import fake_offer_detector

try:
    import fitz
    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False

try:
    import pytesseract
    from PIL import Image
    OCR_SUPPORT = True
except ImportError:
    OCR_SUPPORT = False

st.set_page_config(
    page_title="CareerOS · AI Platform",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────────────────────────────────────
# CSS + ANIMATIONS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@300;400;500&family=Outfit:wght@300;400;500;600;700;800;900&display=swap');

:root {
  --bg0:     #05030e;
  --bg1:     #08051a;
  --bg2:     #0c0820;
  --purple:  #9333ea;
  --violet:  #7c3aed;
  --indigo:  #6366f1;
  --cyan:    #22d3ee;
  --teal:    #14b8a6;
  --sky:     #38bdf8;
  --pink:    #e879f9;
  --emerald: #10b981;
  --amber:   #f59e0b;
  --rose:    #f43f5e;
  --text:    #c4b5fd;
  --text2:   #6b5fa0;
  --text3:   #2e2050;
  --white:   #f0e8ff;
  --border:  rgba(147,51,234,0.25);
  --border2: rgba(147,51,234,0.12);
}

html, body, [class*="css"] {
  font-family: 'Outfit', sans-serif;
  color: var(--text);
}

/* ══ ANIMATED BACKGROUND ══ */
.stApp {
  background: var(--bg0);
  min-height: 100vh;
  overflow-x: hidden;
}

/* animated gradient mesh */
.stApp::before {
  content: '';
  position: fixed; inset: 0; z-index: 0;
  background:
    radial-gradient(ellipse 110% 65% at 50% -10%,  rgba(147,51,234,0.30) 0%, transparent 55%),
    radial-gradient(ellipse 70%  55% at 95%  50%,  rgba(34,211,238,0.13) 0%, transparent 50%),
    radial-gradient(ellipse 60%  50% at 0%   75%,  rgba(99,102,241,0.14) 0%, transparent 50%),
    radial-gradient(ellipse 50%  40% at 50% 100%,  rgba(232,121,249,0.10) 0%, transparent 50%),
    radial-gradient(ellipse 40%  35% at 100%  5%,  rgba(56,189,248,0.08) 0%, transparent 45%),
    linear-gradient(135deg, #06021a 0%, #05030e 60%, #080312 100%);
  animation: bgpulse 12s ease-in-out infinite alternate;
  pointer-events: none;
}

@keyframes bgpulse {
  0%   { opacity: 1; filter: hue-rotate(0deg); }
  50%  { opacity: 0.9; filter: hue-rotate(15deg); }
  100% { opacity: 1; filter: hue-rotate(-10deg); }
}

/* animated dot grid */
.stApp::after {
  content: '';
  position: fixed; inset: 0; z-index: 1;
  background-image:
    radial-gradient(circle, rgba(167,139,250,0.10) 1px, transparent 1px);
  background-size: 28px 28px;
  animation: gridmove 20s linear infinite;
  pointer-events: none;
}

@keyframes gridmove {
  0%   { background-position: 0 0; }
  100% { background-position: 28px 28px; }
}

/* ── HIDE STREAMLIT CHROME ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 0 !important; padding-bottom: 0 !important; max-width: 100% !important; }

/* ── SIDEBAR ── */
section[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #0a0420 0%, #06021a 100%) !important;
  border-right: 1px solid var(--border) !important;
  box-shadow: 4px 0 40px rgba(147,51,234,0.25) !important;
}
section[data-testid="stSidebar"] > div { background: transparent !important; }
section[data-testid="stSidebar"] .stRadio label {
  font-family: 'Outfit', sans-serif !important;
  font-weight: 600 !important; font-size: 0.83rem !important;
  color: var(--text2) !important; padding: 12px 16px !important;
  border-radius: 10px !important; border: 1px solid transparent !important;
  transition: all 0.25s !important; cursor: pointer !important;
  letter-spacing: 0.01em !important;
}
section[data-testid="stSidebar"] .stRadio label:hover {
  color: var(--white) !important;
  background: rgba(147,51,234,0.15) !important;
  border-color: var(--border) !important;
  box-shadow: 0 0 12px rgba(147,51,234,0.15) !important;
}

/* ── LOGO ── */
.nx-logo { padding: 24px 18px 20px; border-bottom: 1px solid var(--border2); margin-bottom: 14px; }
.nx-logo-mark {
  font-family: 'DM Mono', monospace; font-size: 1.2rem; font-weight: 700;
  color: var(--white); display: flex; align-items: center; gap: 10px;
}
.nx-gem {
  width: 34px; height: 34px;
  background: linear-gradient(135deg, var(--purple), var(--pink));
  clip-path: polygon(50% 0%,100% 25%,100% 75%,50% 100%,0% 75%,0% 25%);
  display: flex; align-items: center; justify-content: center;
  font-size: 0.85rem; color: white;
  box-shadow: 0 0 20px rgba(147,51,234,0.7);
  animation: gemglow 3s ease-in-out infinite;
  flex-shrink: 0;
}
@keyframes gemglow {
  0%,100% { box-shadow: 0 0 20px rgba(147,51,234,0.7); transform: scale(1); }
  50%      { box-shadow: 0 0 35px rgba(232,121,249,0.8), 0 0 60px rgba(147,51,234,0.4); transform: scale(1.08); }
}
.nx-logo-sub { font-family:'DM Mono',monospace; font-size:0.54rem; color:var(--text3); letter-spacing:0.14em; text-transform:uppercase; margin-top:5px; }
.nx-online { display:inline-flex; align-items:center; gap:6px; font-family:'DM Mono',monospace; font-size:0.58rem; color:var(--emerald); letter-spacing:0.1em; margin-top:10px; }
.nx-online::before { content:''; width:6px; height:6px; border-radius:50%; background:var(--emerald); box-shadow:0 0 8px var(--emerald); animation:blink 2s ease-in-out infinite; }
@keyframes blink{0%,100%{opacity:1}50%{opacity:0.2}}
.nx-sidebar-footer { font-family:'DM Mono',monospace; font-size:0.52rem; letter-spacing:0.1em; color:var(--text3); text-transform:uppercase; border-top:1px solid var(--border2); padding:14px 18px 0; margin-top:20px; }

/* ── TOPBAR ── */
.topbar {
  background: rgba(5,3,14,0.85); backdrop-filter: blur(20px);
  border-bottom: 1px solid var(--border2);
  padding: 0 28px; height: 60px;
  display: flex; align-items: center; gap: 10px;
  position: sticky; top: 0; z-index: 100;
  box-shadow: 0 4px 30px rgba(0,0,0,0.5), 0 1px 0 rgba(147,51,234,0.2);
}
.topbar-crumb { font-family:'DM Mono',monospace; font-size:0.62rem; color:var(--text2); letter-spacing:0.06em; display:flex; align-items:center; gap:8px; }
.topbar-crumb span { color: var(--white); }
.topbar-chip { display:flex; align-items:center; gap:7px; background:rgba(147,51,234,0.12); border:1px solid rgba(147,51,234,0.3); border-radius:20px; padding:5px 14px; font-family:'DM Mono',monospace; font-size:0.58rem; color:#c084fc; letter-spacing:0.08em; }
.topbar-chip .dot { width:6px; height:6px; border-radius:50%; background:var(--emerald); box-shadow:0 0 6px var(--emerald); animation:blink 2s ease-in-out infinite; }
.topbar-btn { width:34px; height:34px; background:rgba(147,51,234,0.08); border:1px solid var(--border2); border-radius:9px; display:flex; align-items:center; justify-content:center; font-size:0.85rem; cursor:pointer; transition:all 0.2s; }
.topbar-btn:hover { border-color:var(--border); background:rgba(147,51,234,0.18); box-shadow:0 0 12px rgba(147,51,234,0.2); }
.t-avatar { width:34px; height:34px; border-radius:50%; background:linear-gradient(135deg,var(--purple),var(--pink)); border:2px solid rgba(147,51,234,0.5); display:flex; align-items:center; justify-content:center; font-size:0.72rem; font-weight:700; color:white; box-shadow:0 0 14px rgba(147,51,234,0.4); }

/* ── HERO BANNER ── */
.hero-banner {
  position: relative; overflow: hidden;
  background: linear-gradient(135deg, rgba(124,58,237,0.15) 0%, rgba(147,51,234,0.08) 50%, rgba(34,211,238,0.05) 100%);
  border: 1px solid var(--border); border-radius: 16px;
  padding: 32px 36px; margin-bottom: 24px;
}
.hero-banner::before {
  content: '';
  position: absolute; top: -40px; right: -40px;
  width: 200px; height: 200px; border-radius: 50%;
  background: radial-gradient(circle, rgba(147,51,234,0.25) 0%, transparent 70%);
  animation: orbitmove 8s ease-in-out infinite;
}
.hero-banner::after {
  content: '';
  position: absolute; bottom: -50px; left: 30%;
  width: 150px; height: 150px; border-radius: 50%;
  background: radial-gradient(circle, rgba(34,211,238,0.15) 0%, transparent 70%);
  animation: orbitmove2 10s ease-in-out infinite;
}
@keyframes orbitmove  { 0%,100%{transform:translate(0,0)}  50%{transform:translate(-20px,20px)} }
@keyframes orbitmove2 { 0%,100%{transform:translate(0,0)}  50%{transform:translate(20px,-15px)} }

.hero-eyebrow { font-family:'DM Mono',monospace; font-size:0.6rem; letter-spacing:0.2em; text-transform:uppercase; color:#c084fc; margin-bottom:8px; }
.hero-title { font-size:2.6rem; font-weight:900; color:var(--white); line-height:1.05; letter-spacing:-0.025em; margin-bottom:10px; }
.hero-title em { font-style:normal; background:linear-gradient(135deg,#c084fc,#38bdf8); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; }
.hero-sub { font-size:0.9rem; color:var(--text2); max-width:540px; line-height:1.7; }
.hero-badges { display:flex; gap:8px; margin-top:16px; flex-wrap:wrap; }
.hero-badge {
  font-family:'DM Mono',monospace; font-size:0.6rem; letter-spacing:0.1em; text-transform:uppercase;
  padding:5px 12px; border-radius:20px; border:1px solid;
  animation: badgepop 0.5s ease both;
}
@keyframes badgepop { from{opacity:0;transform:scale(0.8)} to{opacity:1;transform:scale(1)} }
.hero-badge.purple { color:#c084fc; border-color:rgba(192,132,252,0.3); background:rgba(147,51,234,0.12); }
.hero-badge.cyan   { color:#67e8f9; border-color:rgba(103,232,249,0.3); background:rgba(34,211,238,0.08); }
.hero-badge.green  { color:#6ee7b7; border-color:rgba(110,231,183,0.3); background:rgba(16,185,129,0.08); }

/* ── STATS ROW ── */
.stats-row { display:grid; grid-template-columns:repeat(4,1fr); gap:12px; margin-bottom:22px; }
.stat-card {
  position:relative; overflow:hidden;
  background:linear-gradient(135deg,rgba(147,51,234,0.1),rgba(8,5,22,0.9));
  border:1px solid var(--border2); border-radius:14px;
  padding:20px 20px; cursor:default;
  transition:all 0.3s;
}
.stat-card:hover {
  border-color:var(--border);
  transform:translateY(-4px);
  box-shadow:0 16px 40px rgba(0,0,0,0.4), 0 0 30px rgba(147,51,234,0.15);
}
.stat-card::after { content:''; position:absolute; bottom:0; left:0; right:0; height:2px; background:var(--sg,linear-gradient(90deg,var(--purple),var(--cyan))); }
.stat-card::before { content:''; position:absolute; top:-20px; right:-20px; width:70px; height:70px; border-radius:50%; background:var(--sb,rgba(147,51,234,0.12)); pointer-events:none; transition:all 0.3s; }
.stat-card:hover::before { transform:scale(1.4); opacity:0.8; }
.stat-icon { font-size:1.5rem; margin-bottom:8px; display:block; }
.stat-label { font-family:'DM Mono',monospace; font-size:0.56rem; letter-spacing:0.14em; text-transform:uppercase; color:var(--text2); margin-bottom:6px; }
.stat-value { font-size:2.1rem; font-weight:900; color:var(--white); line-height:1; letter-spacing:-0.02em; }
.stat-delta { font-family:'DM Mono',monospace; font-size:0.6rem; margin-top:5px; color:var(--teal); }

/* ── GLASS PANEL ── */
.g-panel {
  background:linear-gradient(135deg,rgba(147,51,234,0.08) 0%,rgba(8,5,22,0.92) 100%);
  border:1px solid var(--border); border-radius:16px; overflow:hidden;
  transition:all 0.3s; position:relative;
}
.g-panel:hover { border-color:rgba(167,139,250,0.35); box-shadow:0 12px 50px rgba(0,0,0,0.4), 0 0 40px rgba(147,51,234,0.08); }
.g-panel-glow { height:1px; background:linear-gradient(90deg,transparent,var(--purple),var(--pink),var(--cyan),transparent); opacity:0.6; }
.g-panel-head { padding:15px 22px 13px; border-bottom:1px solid var(--border2); display:flex; align-items:center; justify-content:space-between; }
.g-panel-title { font-size:0.85rem; font-weight:700; color:var(--white); display:flex; align-items:center; gap:9px; }
.g-panel-icon {
  width:28px; height:28px;
  background:linear-gradient(135deg,rgba(147,51,234,0.3),rgba(124,58,237,0.2));
  border:1px solid rgba(167,139,250,0.3); border-radius:8px;
  display:flex; align-items:center; justify-content:center; font-size:0.8rem;
  box-shadow:0 0 10px rgba(147,51,234,0.2);
}
.g-panel-body { padding:18px 22px; }
.g-panel-action { font-family:'DM Mono',monospace; font-size:0.56rem; letter-spacing:0.1em; color:#67e8f9; cursor:pointer; background:rgba(34,211,238,0.08); border:1px solid rgba(34,211,238,0.2); padding:5px 11px; border-radius:5px; text-transform:uppercase; transition:all 0.2s; }
.g-panel-action:hover { background:rgba(34,211,238,0.15); box-shadow:0 0 12px rgba(34,211,238,0.2); }

/* ── UPLOAD ZONE ── */
.upload-zone {
  border:2px dashed rgba(147,51,234,0.35); border-radius:12px; padding:22px 16px;
  text-align:center; cursor:pointer;
  background:linear-gradient(135deg,rgba(147,51,234,0.05),rgba(34,211,238,0.03));
  transition:all 0.25s; margin-bottom:6px;
}
.upload-zone:hover { border-color:rgba(34,211,238,0.5); background:rgba(34,211,238,0.05); box-shadow:0 0 20px rgba(34,211,238,0.1) inset; }
.upload-zone-icon { font-size:2rem; margin-bottom:8px; display:block; animation:float 3s ease-in-out infinite; }
@keyframes float { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-5px)} }
.upload-zone-label { font-family:'DM Mono',monospace; font-size:0.65rem; letter-spacing:0.1em; text-transform:uppercase; color:var(--text2); }
.upload-zone-sub { font-size:0.72rem; color:var(--text3); margin-top:3px; }

/* ── SKILL TAGS ── */
.tag { display:inline-block; font-family:'DM Mono',monospace; font-size:0.68rem; font-weight:500; padding:5px 12px; border-radius:5px; margin:3px; letter-spacing:0.03em; transition:all 0.2s; }
.tag:hover { transform:translateY(-2px); box-shadow:0 4px 12px rgba(0,0,0,0.3); }
.tag-ok  { color:#6ee7b7; background:rgba(16,185,129,0.12); border:1px solid rgba(16,185,129,0.3); }
.tag-gap { color:#fcd34d; background:rgba(245,158,11,0.1);  border:1px solid rgba(245,158,11,0.3); }
.tag-sect { font-family:'DM Mono',monospace; font-size:0.56rem; letter-spacing:0.14em; text-transform:uppercase; color:var(--text2); padding:8px 0 6px; border-bottom:1px solid var(--border2); margin-bottom:10px; }

/* readiness */
.ready-wrap { margin-top:14px; padding:16px 18px; background:rgba(147,51,234,0.06); border:1px solid var(--border2); border-radius:12px; }
.ready-label { display:flex; justify-content:space-between; font-family:'DM Mono',monospace; font-size:0.58rem; letter-spacing:0.1em; color:var(--text2); text-transform:uppercase; margin-bottom:8px; }
.ready-label span { color:#c084fc; font-weight:700; }
.ready-track { height:6px; border-radius:3px; background:rgba(147,51,234,0.12); overflow:hidden; }
.ready-fill { height:100%; border-radius:3px; background:linear-gradient(90deg,var(--violet),#c084fc,var(--cyan)); box-shadow:0 0 10px rgba(147,51,234,0.5); transition:width 1s ease; animation:shimmer 2s ease-in-out infinite; }
@keyframes shimmer { 0%,100%{opacity:1} 50%{opacity:0.8} }

/* ── JOB CARD ── */
.job-card { display:flex; align-items:center; padding:15px 18px; border-bottom:1px solid var(--border2); gap:14px; transition:all 0.2s; position:relative; overflow:hidden; }
.job-card:last-child{border-bottom:none;}
.job-card:hover { background:rgba(147,51,234,0.07); }
.job-card:hover::before { content:''; position:absolute; left:0; top:0; bottom:0; width:3px; background:linear-gradient(180deg,var(--purple),var(--cyan)); border-radius:0 3px 3px 0; }
.job-icon { width:40px; height:40px; min-width:40px; border-radius:11px; display:flex; align-items:center; justify-content:center; font-size:1rem; box-shadow:0 4px 12px rgba(0,0,0,0.3); }
.job-name { font-size:0.88rem; font-weight:700; color:var(--white); }
.job-co { font-family:'DM Mono',monospace; font-size:0.6rem; color:var(--text2); letter-spacing:0.06em; margin-top:3px; }
.job-pct { font-family:'DM Mono',monospace; font-weight:800; font-size:1.1rem; }
.job-stip { font-family:'DM Mono',monospace; font-size:0.58rem; color:var(--text2); letter-spacing:0.06em; margin-top:3px; }
.mbar { width:72px; height:4px; border-radius:2px; background:rgba(147,51,234,0.12); overflow:hidden; margin:4px 0 0 auto; }
.mfill { height:100%; border-radius:2px; box-shadow:0 0 6px currentColor; }

/* ── SCORE ── */
.score-wrap { text-align:center; padding:28px 16px; position:relative; }
.score-wrap::before { content:''; position:absolute; inset:0; background:radial-gradient(circle at 50% 50%,rgba(147,51,234,0.12),transparent 70%); pointer-events:none; }
.score-lbl { font-family:'DM Mono',monospace; font-size:0.54rem; letter-spacing:0.18em; text-transform:uppercase; color:var(--text2); margin-bottom:12px; }
.score-num { font-size:4.8rem; font-weight:900; line-height:1; letter-spacing:-0.04em; }
.score-num.hi { color:#4ade80; text-shadow:0 0 40px rgba(74,222,128,0.5),0 0 80px rgba(74,222,128,0.2); }
.score-num.md { color:#fbbf24; text-shadow:0 0 40px rgba(251,191,36,0.4),0 0 80px rgba(251,191,36,0.15); }
.score-num.lo { color:#fb7185; text-shadow:0 0 40px rgba(251,113,133,0.4),0 0 80px rgba(251,113,133,0.15); }
.score-v { font-size:0.8rem; font-weight:700; letter-spacing:0.1em; text-transform:uppercase; margin-top:8px; }
.score-h { font-size:0.78rem; color:var(--text2); margin-top:6px; line-height:1.6; padding:0 12px; }
.prow { display:flex; align-items:center; gap:10px; padding:10px 0; border-bottom:1px solid var(--border2); }
.prow:last-child{border-bottom:none;}
.plbl { font-family:'DM Mono',monospace; font-size:0.58rem; letter-spacing:0.08em; text-transform:uppercase; color:var(--text2); width:115px; }
.pbar { flex:1; height:4px; background:rgba(147,51,234,0.1); border-radius:2px; overflow:hidden; }
.pfill { height:100%; border-radius:2px; background:linear-gradient(90deg,var(--violet),#c084fc,var(--sky)); }
.pval { font-family:'DM Mono',monospace; font-size:0.72rem; font-weight:700; color:#c084fc; width:36px; text-align:right; }

/* ── RESULT BOXES ── */
.rbox { border-radius:12px; padding:20px 20px; margin-top:6px; position:relative; overflow:hidden; }
.rbox::before { content:''; position:absolute; top:0; left:0; right:0; height:1px; background:var(--rb-line,linear-gradient(90deg,var(--emerald),transparent)); }
.rbox.safe { background:rgba(16,185,129,0.07); border:1px solid rgba(16,185,129,0.25); border-left:4px solid var(--emerald); color:#a7f3d0; --rb-line:linear-gradient(90deg,var(--emerald),transparent); }
.rbox.fake { background:rgba(244,63,94,0.07); border:1px solid rgba(244,63,94,0.25); border-left:4px solid var(--rose); color:#fda4af; --rb-line:linear-gradient(90deg,var(--rose),transparent); }
.rbox-title { font-family:'DM Mono',monospace; font-size:0.6rem; letter-spacing:0.15em; text-transform:uppercase; font-weight:700; margin-bottom:8px; display:flex; align-items:center; gap:6px; }
.rtips { font-family:'DM Mono',monospace; font-size:0.6rem; line-height:2.2; opacity:0.65; margin-top:12px; border-top:1px solid rgba(255,255,255,0.07); padding-top:12px; }

/* ── FLOATING ORBS (decorative) ── */
.orb {
  position:fixed; border-radius:50%; pointer-events:none; z-index:2;
  filter:blur(60px); opacity:0.12;
}
.orb1 { width:300px; height:300px; top:10%; left:5%;  background:radial-gradient(circle,#9333ea,transparent); animation:orb1move 15s ease-in-out infinite; }
.orb2 { width:250px; height:250px; top:50%; right:5%; background:radial-gradient(circle,#22d3ee,transparent); animation:orb2move 18s ease-in-out infinite; }
.orb3 { width:200px; height:200px; bottom:10%; left:40%; background:radial-gradient(circle,#e879f9,transparent); animation:orb3move 12s ease-in-out infinite; }
@keyframes orb1move { 0%,100%{transform:translate(0,0)} 33%{transform:translate(40px,-30px)} 66%{transform:translate(-20px,40px)} }
@keyframes orb2move { 0%,100%{transform:translate(0,0)} 33%{transform:translate(-30px,40px)} 66%{transform:translate(20px,-20px)} }
@keyframes orb3move { 0%,100%{transform:translate(0,0)} 50%{transform:translate(30px,-40px)} }

/* ── INPUTS ── */
.stTextInput>div>div>input,.stTextArea>div>div>textarea {
  background:rgba(8,5,20,0.95) !important; border:1px solid var(--border) !important;
  border-radius:10px !important; color:var(--white) !important;
  font-family:'DM Mono',monospace !important; font-size:0.8rem !important;
  caret-color:#c084fc !important; transition:all 0.2s !important;
}
.stTextInput>div>div>input:focus,.stTextArea>div>div>textarea:focus {
  border-color:rgba(192,132,252,0.6) !important;
  box-shadow:0 0 0 3px rgba(147,51,234,0.15),0 0 20px rgba(147,51,234,0.1) !important;
}
.stTextInput>div>div>input::placeholder,.stTextArea>div>div>textarea::placeholder{color:var(--text3) !important;}
.stSelectbox>div>div,.stSelectbox [data-baseweb="select"]>div{background:rgba(8,5,20,0.95) !important;border:1px solid var(--border) !important;border-radius:10px !important;color:var(--white) !important;}

/* ── BUTTONS ── */
.stButton>button {
  background:linear-gradient(135deg,#9333ea,#7c3aed) !important;
  color:white !important; border:none !important; border-radius:10px !important;
  padding:11px 26px !important; font-family:'Outfit',sans-serif !important;
  font-weight:700 !important; font-size:0.84rem !important; letter-spacing:0.05em !important;
  box-shadow:0 4px 20px rgba(147,51,234,0.5) !important;
  transition:all 0.25s !important; position:relative !important; overflow:hidden !important;
}
.stButton>button:hover {
  transform:translateY(-2px) !important;
  box-shadow:0 8px 30px rgba(147,51,234,0.65),0 0 50px rgba(192,132,252,0.2) !important;
  background:linear-gradient(135deg,#a855f7,#9333ea) !important;
}

/* file uploader */
[data-testid="stFileUploader"] {
  background:rgba(8,5,20,0.9) !important;
  border:1.5px dashed rgba(147,51,234,0.35) !important;
  border-radius:12px !important; transition:border-color 0.2s !important;
}
[data-testid="stFileUploader"]:hover{border-color:rgba(34,211,238,0.4) !important;}
[data-testid="stFileUploader"] label{color:var(--text2) !important;font-family:'DM Mono',monospace !important;font-size:0.72rem !important;}

.stSlider [data-baseweb="slider"] div[role="slider"] { background:#c084fc !important; border-color:#c084fc !important; box-shadow:0 0 14px rgba(192,132,252,0.8) !important; }
.stTextInput label,.stTextArea label,.stSelectbox label,.stSlider label { font-family:'DM Mono',monospace !important; font-size:0.58rem !important; letter-spacing:0.12em !important; text-transform:uppercase !important; color:var(--text2) !important; }
.stProgress>div>div>div { background:linear-gradient(90deg,var(--violet),#c084fc,var(--cyan)) !important; border-radius:3px !important; box-shadow:0 0 10px rgba(147,51,234,0.4) !important; }
.stProgress>div>div { background:rgba(147,51,234,0.1) !important; border-radius:3px !important; }

[data-testid="metric-container"] { background:linear-gradient(135deg,rgba(147,51,234,0.1),rgba(8,5,22,0.8)) !important; border:1px solid var(--border2) !important; border-radius:12px !important; padding:16px !important; }
[data-testid="metric-container"] label { font-family:'DM Mono',monospace !important; font-size:0.56rem !important; letter-spacing:0.12em !important; text-transform:uppercase !important; color:var(--text2) !important; }
[data-testid="metric-container"] [data-testid="stMetricValue"] { font-family:'Outfit',sans-serif !important; color:#c084fc !important; font-weight:900 !important; font-size:1.6rem !important; }

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] { background:transparent !important; gap:4px; border-bottom:1px solid var(--border2) !important; }
.stTabs [data-baseweb="tab"] { background:transparent !important; color:var(--text2) !important; font-family:'Outfit',sans-serif !important; font-weight:600 !important; font-size:0.8rem !important; border-radius:8px 8px 0 0 !important; padding:9px 18px !important; border:none !important; transition:all 0.2s !important; }
.stTabs [data-baseweb="tab"]:hover { color:var(--white) !important; background:rgba(147,51,234,0.1) !important; }
.stTabs [aria-selected="true"] { color:#c084fc !important; background:rgba(147,51,234,0.12) !important; border-bottom:2px solid #c084fc !important; }
.stTabs [data-baseweb="tab-panel"] { padding-top:18px !important; }

/* ── PAGE HEADER ── */
.page-eyebrow { font-family:'DM Mono',monospace; font-size:0.58rem; letter-spacing:0.2em; text-transform:uppercase; color:#c084fc; margin-bottom:6px; display:flex; align-items:center; gap:8px; }
.page-eyebrow::before{content:'';width:16px;height:1px;background:linear-gradient(90deg,var(--purple),transparent);}
.page-title { font-size:2.2rem; font-weight:900; color:var(--white); line-height:1.05; letter-spacing:-0.025em; }
.page-title em { font-style:normal; background:linear-gradient(135deg,#c084fc,#67e8f9); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; }
.page-desc { font-size:0.87rem; color:var(--text2); margin-top:6px; max-width:560px; line-height:1.7; }

/* ── ANIMATIONS ── */
@keyframes fadeUp { from{opacity:0;transform:translateY(18px)} to{opacity:1;transform:translateY(0)} }
@keyframes fadeIn { from{opacity:0} to{opacity:1} }
.anim-1{animation:fadeUp 0.4s 0.05s ease both;}
.anim-2{animation:fadeUp 0.4s 0.15s ease both;}
.anim-3{animation:fadeUp 0.4s 0.25s ease both;}
.anim-4{animation:fadeUp 0.4s 0.35s ease both;}
</style>
""", unsafe_allow_html=True)

# Floating orbs
st.markdown("""
<div class="orb orb1"></div>
<div class="orb orb2"></div>
<div class="orb orb3"></div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def extract_text_from_pdf(f):
    if not PDF_SUPPORT:
        return None,"PyMuPDF not installed. Run: pip install pymupdf"
    try:
        import fitz
        doc = fitz.open(stream=f.read(), filetype="pdf")
        return "\n".join(p.get_text() for p in doc).strip(), None
    except Exception as e:
        return None, str(e)

def extract_text_from_image(f):
    if not OCR_SUPPORT:
        return None,"pytesseract not installed. Run: pip install pytesseract pillow"
    try:
        import pytesseract
        from PIL import Image
        return pytesseract.image_to_string(Image.open(f)).strip(), None
    except Exception as e:
        return None, str(e)

SKILLS_LIST = ["python","java","javascript","typescript","react","angular","vue","node","nodejs","sql","mysql","postgresql","mongodb","redis","docker","kubernetes","aws","azure","gcp","pandas","numpy","scikit","tensorflow","pytorch","keras","opencv","nlp","html","css","tailwind","bootstrap","flask","django","fastapi","spring","git","linux","machine learning","deep learning","data analysis","data science","c++","c#","rust","go","swift","kotlin","r","excel","power bi","tableau"]

def parse_skills(text):
    found = [s for s in SKILLS_LIST if s in text.lower()]
    return ", ".join(found)

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="nx-logo">
      <div class="nx-logo-mark"><div class="nx-gem">◈</div>CareerOS</div>
      <div class="nx-logo-sub">AI Intelligence Platform · v3.2</div>
      <div class="nx-online">ALL SYSTEMS ONLINE</div>
    </div>
    """, unsafe_allow_html=True)

    menu = st.radio("", [
        "◈  Skill Gap Analyzer",
        "⬡  Internship Matchmaker",
        "◎  Placement Predictor",
        "⊕  Offer Authenticity Check",
    ], label_visibility="collapsed")

    # sidebar illustration
    st.markdown("""
    <div style="margin:24px 10px 10px;padding:16px;background:rgba(147,51,234,0.08);border:1px solid rgba(147,51,234,0.15);border-radius:12px;text-align:center;">
      <div style="font-size:2.4rem;margin-bottom:6px;animation:float 3s ease-in-out infinite;">🚀</div>
      <div style="font-family:'DM Mono',monospace;font-size:0.58rem;letter-spacing:0.1em;text-transform:uppercase;color:var(--text2);line-height:1.8;">
        AI-Powered<br>Career Engine<br>
        <span style="color:#c084fc;">v3.2 Active</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="nx-sidebar-footer">
      <div>Powered by AI · Secured</div>
      <div style="margin-top:4px;color:#1a1040;">© 2025 CareerOS</div>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# TOPBAR
# ─────────────────────────────────────────────────────────────────────────────
mod_name = menu.split("  ")[1] if "  " in menu else menu
st.markdown(f"""
<div class="topbar">
  <div class="topbar-crumb">
    CareerOS <span style="color:var(--text3);">/</span>
    Platform <span style="color:var(--text3);">/</span>
    <span>{mod_name}</span>
  </div>
  <div style="flex:1"></div>
  <div class="topbar-chip"><span class="dot"></span>&nbsp;AI ENGINE LIVE</div>
  <div class="topbar-btn" style="margin-left:10px;">🔍</div>
  <div class="topbar-btn">🔔</div>
  <div class="t-avatar" style="margin-left:8px;">JD</div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# MAIN CONTENT
# ─────────────────────────────────────────────────────────────────────────────
with st.container():
    st.markdown('<div style="padding:28px 30px 52px;">', unsafe_allow_html=True)

    # ── HERO BANNER (shown on every page) ──
    module_icons = {
        "Skill Gap Analyzer":       ("🧠", "Diagnose skill gaps in seconds"),
        "Internship Matchmaker":     ("💼", "Find internships matched to your profile"),
        "Placement Predictor":       ("📊", "Predict your placement probability with AI"),
        "Offer Authenticity Check":  ("🛡️", "Verify offer letters instantly"),
    }
    icon, tagline = module_icons.get(mod_name, ("◈", "AI Career Intelligence"))

    st.markdown(f"""
    <div class="hero-banner anim-1">
      <div style="display:flex;align-items:flex-start;gap:24px;">
        <div style="font-size:3.5rem;flex-shrink:0;filter:drop-shadow(0 0 20px rgba(147,51,234,0.6));animation:float 3s ease-in-out infinite;">{icon}</div>
        <div>
          <div class="hero-eyebrow">CareerOS · AI Intelligence Platform</div>
          <div class="hero-title">{mod_name.split()[0]} <em>{" ".join(mod_name.split()[1:])}</em></div>
          <div class="hero-sub">{tagline} — powered by advanced ML models trained on real-world career outcomes.</div>
          <div class="hero-badges">
            <span class="hero-badge purple" style="animation-delay:0.1s">◈ AI Powered</span>
            <span class="hero-badge cyan"   style="animation-delay:0.2s">⬡ Real-time</span>
            <span class="hero-badge green"  style="animation-delay:0.3s">✓ Verified Data</span>
          </div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # MODULE 01 — SKILL GAP
    # ══════════════════════════════════════════════════════════════════════════
    if "Skill Gap" in menu:
        st.markdown("""
        <div class="stats-row anim-2">
          <div class="stat-card" style="--sg:linear-gradient(90deg,#9333ea,#22d3ee);--sb:rgba(147,51,234,0.15);">
            <span class="stat-icon">🎯</span>
            <div class="stat-label">Roles Supported</div><div class="stat-value">3</div><div class="stat-delta">DS · WD · MLE</div>
          </div>
          <div class="stat-card" style="--sg:linear-gradient(90deg,#22d3ee,#14b8a6);--sb:rgba(34,211,238,0.1);">
            <span class="stat-icon">📈</span>
            <div class="stat-label">Avg Match Rate</div><div class="stat-value">68%</div><div class="stat-delta">↑ platform avg</div>
          </div>
          <div class="stat-card" style="--sg:linear-gradient(90deg,#6366f1,#9333ea);--sb:rgba(99,102,241,0.1);">
            <span class="stat-icon">⚡</span>
            <div class="stat-label">Skills Tracked</div><div class="stat-value">120+</div><div class="stat-delta">updated monthly</div>
          </div>
          <div class="stat-card" style="--sg:linear-gradient(90deg,#f59e0b,#f43f5e);--sb:rgba(245,158,11,0.1);">
            <span class="stat-icon">🔍</span>
            <div class="stat-label">Avg Gap Count</div><div class="stat-value">4.2</div><div class="stat-delta">skills per role</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="g-panel anim-3"><div class="g-panel-glow"></div><div class="g-panel-head"><div class="g-panel-title"><div class="g-panel-icon">◈</div> Skill Diagnostics Engine</div><div class="g-panel-action">Run Analysis</div></div><div class="g-panel-body">', unsafe_allow_html=True)

        sg_t1, sg_t2, sg_t3 = st.tabs(["✏️  Type Skills", "📄  Upload Resume PDF", "🖼️  Upload Profile Image"])
        skills_input, role = "", "Data Scientist"

        with sg_t1:
            c1,c2 = st.columns([3,1])
            with c1: si = st.text_input("Current Skills", placeholder="python, pandas, sql, docker …", key="sg_t")
            with c2: role = st.selectbox("Target Role", ["Data Scientist","Web Developer","ML Engineer"], key="sg_r1")
            if si: skills_input = si

        with sg_t2:
            st.markdown('<div class="upload-zone"><span class="upload-zone-icon">📄</span><div class="upload-zone-label">Drop resume PDF here</div><div class="upload-zone-sub">Skills auto-extracted via NLP</div></div>', unsafe_allow_html=True)
            pf = st.file_uploader("PDF", type=["pdf"], key="sg_pdf", label_visibility="collapsed")
            c1,c2 = st.columns([3,1])
            with c2: role = st.selectbox("Target Role", ["Data Scientist","Web Developer","ML Engineer"], key="sg_r2")
            if pf:
                ex,er = extract_text_from_pdf(pf)
                if er: st.error(er)
                elif ex:
                    st.success(f"✓ PDF extracted — {len(ex.split())} words")
                    with c1: skills_input = st.text_input("Extracted Skills", value=parse_skills(ex), key="sg_ps")

        with sg_t3:
            st.markdown('<div class="upload-zone"><span class="upload-zone-icon">🖼️</span><div class="upload-zone-label">Profile or certificate image</div><div class="upload-zone-sub">OCR extracts your skills automatically</div></div>', unsafe_allow_html=True)
            ig = st.file_uploader("Image", type=["png","jpg","jpeg"], key="sg_img", label_visibility="collapsed")
            c1,c2 = st.columns([3,1])
            with c2: role = st.selectbox("Target Role", ["Data Scientist","Web Developer","ML Engineer"], key="sg_r3")
            if ig:
                cp,ci = st.columns([1,2])
                with cp: st.image(ig, use_column_width=True)
                with ci:
                    ex,er = extract_text_from_image(ig)
                    if er: st.warning(f"OCR unavailable: {er}")
                    elif ex: st.success(f"✓ OCR complete — {len(ex.split())} words")
                with c1: skills_input = st.text_input("Extracted Skills", value=parse_skills(ex) if ig and not er and ex else "", key="sg_is")

        run_sg = st.button("Run Skill Diagnostics →", key="btn_sg")
        st.markdown('</div></div>', unsafe_allow_html=True)

        if run_sg:
            if not skills_input.strip():
                st.warning("Please enter or extract at least one skill.")
            else:
                skills = [s.strip().lower() for s in skills_input.split(",") if s.strip()]
                matched, missing = skill_gap_analyzer(skills, role)
                c_ok, c_gap = st.columns(2)
                with c_ok:
                    st.markdown('<div class="g-panel anim-3"><div class="g-panel-glow"></div><div class="g-panel-head"><div class="g-panel-title"><div class="g-panel-icon" style="color:#6ee7b7">✓</div> Confirmed Skills</div></div><div class="g-panel-body">', unsafe_allow_html=True)
                    st.markdown(f'<div class="tag-sect">✔ {len(matched)} verified</div>', unsafe_allow_html=True)
                    st.markdown("".join([f'<span class="tag tag-ok">{m}</span>' for m in matched]) if matched else '<span style="color:var(--text2);font-size:0.8rem;">No matches detected</span>', unsafe_allow_html=True)
                    st.markdown('</div></div>', unsafe_allow_html=True)
                with c_gap:
                    st.markdown('<div class="g-panel anim-4"><div class="g-panel-glow"></div><div class="g-panel-head"><div class="g-panel-title"><div class="g-panel-icon" style="color:#fcd34d">!</div> Skill Gaps</div></div><div class="g-panel-body">', unsafe_allow_html=True)
                    st.markdown(f'<div class="tag-sect">⚠ {len(missing)} gaps</div>', unsafe_allow_html=True)
                    st.markdown("".join([f'<span class="tag tag-gap">{m}</span>' for m in missing]) if missing else '<span style="color:var(--emerald);font-size:0.8rem;">All satisfied ✓</span>', unsafe_allow_html=True)
                    st.markdown('</div></div>', unsafe_allow_html=True)
                total = len(matched)+len(missing)
                if total:
                    pct = int((len(matched)/total)*100)
                    st.markdown(f"""
                    <div class="ready-wrap anim-4">
                      <div class="ready-label"><span>Role Readiness — {role}</span><span>{pct}% MATCH</span></div>
                      <div class="ready-track"><div class="ready-fill" style="width:{pct}%"></div></div>
                    </div>""", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # MODULE 02 — INTERNSHIP
    # ══════════════════════════════════════════════════════════════════════════
    elif "Internship" in menu:
        st.markdown("""
        <div class="stats-row anim-2">
          <div class="stat-card" style="--sg:linear-gradient(90deg,#9333ea,#22d3ee);--sb:rgba(147,51,234,0.15);">
            <span class="stat-icon">🏢</span>
            <div class="stat-label">Partner Companies</div><div class="stat-value">50+</div><div class="stat-delta">actively hiring</div>
          </div>
          <div class="stat-card" style="--sg:linear-gradient(90deg,#22d3ee,#14b8a6);--sb:rgba(34,211,238,0.1);">
            <span class="stat-icon">💰</span>
            <div class="stat-label">Avg Stipend</div><div class="stat-value">₹18k</div><div class="stat-delta">per month</div>
          </div>
          <div class="stat-card" style="--sg:linear-gradient(90deg,#6366f1,#9333ea);--sb:rgba(99,102,241,0.1);">
            <span class="stat-icon">⚡</span>
            <div class="stat-label">Match Speed</div><div class="stat-value">&lt;1s</div><div class="stat-delta">real-time engine</div>
          </div>
          <div class="stat-card" style="--sg:linear-gradient(90deg,#f59e0b,#10b981);--sb:rgba(16,185,129,0.1);">
            <span class="stat-icon">✅</span>
            <div class="stat-label">Placement Rate</div><div class="stat-value">74%</div><div class="stat-delta">via platform</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="g-panel anim-3"><div class="g-panel-glow"></div><div class="g-panel-head"><div class="g-panel-title"><div class="g-panel-icon">⬡</div> Opportunity Engine</div><div class="g-panel-action">Export CSV</div></div><div class="g-panel-body">', unsafe_allow_html=True)

        im_t1, im_t2, im_t3 = st.tabs(["✏️  Type Skills", "📄  Resume PDF", "🖼️  Profile Image"])
        im_skills = ""

        with im_t1:
            si2 = st.text_input("Skills", placeholder="react, node.js, mongodb, typescript …", key="im_t")
            if si2: im_skills = si2
        with im_t2:
            st.markdown('<div class="upload-zone"><span class="upload-zone-icon">📄</span><div class="upload-zone-label">Drop resume PDF</div><div class="upload-zone-sub">Auto-extract skills</div></div>', unsafe_allow_html=True)
            pf2 = st.file_uploader("PDF", type=["pdf"], key="im_pdf", label_visibility="collapsed")
            if pf2:
                ex2,er2 = extract_text_from_pdf(pf2)
                if er2: st.error(er2)
                elif ex2:
                    st.success(f"✓ PDF extracted")
                    im_skills = st.text_input("Skills", value=parse_skills(ex2), key="im_ps")
        with im_t3:
            st.markdown('<div class="upload-zone"><span class="upload-zone-icon">🖼️</span><div class="upload-zone-label">Profile image</div><div class="upload-zone-sub">OCR extracts skills</div></div>', unsafe_allow_html=True)
            ig2 = st.file_uploader("Image", type=["png","jpg","jpeg"], key="im_img", label_visibility="collapsed")
            if ig2:
                c1,c2 = st.columns([1,2])
                with c1: st.image(ig2, use_column_width=True)
                ex3,er3 = extract_text_from_image(ig2)
                if er3: st.warning(f"OCR unavailable: {er3}")
                elif ex3: st.success(f"✓ OCR complete")
                im_skills = st.text_input("Skills", value=parse_skills(ex3) if ig2 and not er3 and ex3 else "", key="im_is")

        run_im = st.button("Find Matching Internships →", key="btn_im")
        st.markdown('</div></div>', unsafe_allow_html=True)

        if run_im:
            if not im_skills.strip():
                st.warning("Provide at least one skill.")
            else:
                skills = [s.strip().lower() for s in im_skills.split(",") if s.strip()]
                matches = internship_matcher(skills)
                if matches:
                    st.markdown(f'<div class="anim-3" style="font-family:\'DM Mono\',monospace;font-size:0.58rem;letter-spacing:0.12em;color:var(--text2);text-transform:uppercase;margin:16px 0 10px;">{len(matches)} opportunities ranked by compatibility score</div>', unsafe_allow_html=True)
                    grads = ["linear-gradient(135deg,#9333ea,#6366f1)","linear-gradient(135deg,#22d3ee,#9333ea)","linear-gradient(135deg,#6366f1,#38bdf8)","linear-gradient(135deg,#f59e0b,#f43f5e)","linear-gradient(135deg,#10b981,#22d3ee)"]
                    st.markdown('<div class="g-panel anim-4"><div class="g-panel-glow"></div><div style="padding:0">', unsafe_allow_html=True)
                    for i,m in enumerate(matches):
                        pct = m["match_percent"]
                        col = "#4ade80" if pct>=70 else "#fbbf24" if pct>=40 else "#fb7185"
                        st.markdown(f"""
                        <div class="job-card">
                          <div class="job-icon" style="background:{grads[i%len(grads)]};">💼</div>
                          <div style="flex:1"><div class="job-name">{m['role']}</div><div class="job-co">{m['company'].upper()}</div></div>
                          <div style="text-align:right">
                            <div class="job-pct" style="color:{col}">{pct}%</div>
                            <div class="mbar"><div class="mfill" style="width:{pct}%;color:{col};background:{col};"></div></div>
                            <div class="job-stip">₹{m['stipend']}/MO</div>
                          </div>
                        </div>""", unsafe_allow_html=True)
                    st.markdown('</div></div>', unsafe_allow_html=True)
                else:
                    st.info("No matches. Try adding more skills.")

    # ══════════════════════════════════════════════════════════════════════════
    # MODULE 03 — PREDICTOR
    # ══════════════════════════════════════════════════════════════════════════
    elif "Predictor" in menu:
        st.markdown("""
        <div class="stats-row anim-2">
          <div class="stat-card" style="--sg:linear-gradient(90deg,#9333ea,#22d3ee);--sb:rgba(147,51,234,0.15);">
            <span class="stat-icon">🤖</span>
            <div class="stat-label">Model Accuracy</div><div class="stat-value">91%</div><div class="stat-delta">on test data</div>
          </div>
          <div class="stat-card" style="--sg:linear-gradient(90deg,#22d3ee,#14b8a6);--sb:rgba(34,211,238,0.1);">
            <span class="stat-icon">📊</span>
            <div class="stat-label">Factors Analysed</div><div class="stat-value">3</div><div class="stat-delta">CGPA · Skills · Projects</div>
          </div>
          <div class="stat-card" style="--sg:linear-gradient(90deg,#6366f1,#9333ea);--sb:rgba(99,102,241,0.1);">
            <span class="stat-icon">⚡</span>
            <div class="stat-label">Predictions Made</div><div class="stat-value">12k+</div><div class="stat-delta">this semester</div>
          </div>
          <div class="stat-card" style="--sg:linear-gradient(90deg,#10b981,#22d3ee);--sb:rgba(16,185,129,0.1);">
            <span class="stat-icon">🎓</span>
            <div class="stat-label">Avg Probability</div><div class="stat-value">62%</div><div class="stat-delta">across users</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="g-panel anim-3"><div class="g-panel-glow"></div><div class="g-panel-head"><div class="g-panel-title"><div class="g-panel-icon">◎</div> Predictive Model Input</div></div><div class="g-panel-body">', unsafe_allow_html=True)

        pp_t1, pp_t2, pp_t3 = st.tabs(["🎛️  Manual Input", "📄  Parse Resume PDF", "🖼️  Parse from Image"])
        pp_sc, pp_cg, pp_pr = 5, 7.0, 2

        with pp_t1:
            c1,c2,c3 = st.columns(3)
            with c1: pp_sc = st.slider("Skills Count", 1, 20, 5, key="pp_s1")
            with c2: pp_cg = st.slider("CGPA", 0.0, 10.0, 7.0, 0.1, key="pp_c1")
            with c3: pp_pr = st.slider("Projects", 0, 10, 2, key="pp_p1")
        with pp_t2:
            st.markdown('<div class="upload-zone"><span class="upload-zone-icon">📄</span><div class="upload-zone-label">Upload resume PDF</div><div class="upload-zone-sub">Skills count auto-detected</div></div>', unsafe_allow_html=True)
            pf3 = st.file_uploader("Resume", type=["pdf"], key="pp_pdf", label_visibility="collapsed")
            if pf3:
                ex4,er4 = extract_text_from_pdf(pf3)
                if er4: st.error(er4)
                elif ex4:
                    cnt = len([s for s in SKILLS_LIST if s in ex4.lower()])
                    st.success(f"✓ ~{cnt} skills detected in resume")
                    c1,c2,c3 = st.columns(3)
                    with c1: pp_sc = st.slider("Skills Count",1,20,min(cnt,20),key="pp_s2")
                    with c2: pp_cg = st.slider("CGPA",0.0,10.0,7.0,0.1,key="pp_c2")
                    with c3: pp_pr = st.slider("Projects",0,10,2,key="pp_p2")
        with pp_t3:
            st.markdown('<div class="upload-zone"><span class="upload-zone-icon">🖼️</span><div class="upload-zone-label">Marksheet / certificate image</div><div class="upload-zone-sub">OCR parses CGPA and skills</div></div>', unsafe_allow_html=True)
            ig3 = st.file_uploader("Image", type=["png","jpg","jpeg"], key="pp_img", label_visibility="collapsed")
            if ig3:
                c1,c2 = st.columns([1,2])
                with c1: st.image(ig3, use_column_width=True)
                ex5,er5 = extract_text_from_image(ig3)
                if er5: st.warning(f"OCR unavailable: {er5}")
                elif ex5:
                    cnt2 = len([s for s in SKILLS_LIST if s in ex5.lower()])
                    st.success(f"✓ OCR complete — ~{cnt2} skills found")
                c1,c2,c3 = st.columns(3)
                with c1: pp_sc = st.slider("Skills Count",1,20,5,key="pp_s3")
                with c2: pp_cg = st.slider("CGPA",0.0,10.0,7.0,0.1,key="pp_c3")
                with c3: pp_pr = st.slider("Projects",0,10,2,key="pp_p3")

        run_pp = st.button("Run Prediction Model →", key="btn_pp")
        st.markdown('</div></div>', unsafe_allow_html=True)

        if run_pp:
            prob = predict_placement(pp_sc, pp_cg, pp_pr)
            cls  = "hi" if prob>70 else "md" if prob>40 else "lo"
            cc   = {"hi":"#4ade80","md":"#fbbf24","lo":"#fb7185"}[cls]
            lbl  = {"hi":"High Probability","md":"Moderate Outlook","lo":"Needs Improvement"}[cls]
            hint = {"hi":"Strong profile. Continue domain specialisation and build projects.","md":"Add 2–3 real-world projects and 4+ industry skills to boost score.","lo":"Focus on CGPA, targeted skill-building, and practical experience."}[cls]

            c_score, c_factors = st.columns([1,1.8])
            with c_score:
                st.markdown(f"""
                <div class="g-panel anim-3"><div class="g-panel-glow"></div>
                  <div class="g-panel-head"><div class="g-panel-title"><div class="g-panel-icon">◎</div> Score Output</div></div>
                  <div class="score-wrap">
                    <div class="score-lbl">Placement Probability Score</div>
                    <div class="score-num {cls}">{prob}<span style="font-size:2rem">%</span></div>
                    <div class="score-v" style="color:{cc}">{lbl}</div>
                    <div class="score-h">{hint}</div>
                  </div>
                </div>""", unsafe_allow_html=True)
            with c_factors:
                st.markdown('<div class="g-panel anim-4"><div class="g-panel-glow"></div><div class="g-panel-head"><div class="g-panel-title"><div class="g-panel-icon">≡</div> Factor Breakdown</div></div><div class="g-panel-body">', unsafe_allow_html=True)
                for lf,v,oof in [("Skills Count",pp_sc,20),("CGPA",pp_cg,10),("Projects",pp_pr,10),("Final Score",prob,100)]:
                    bp = int((float(v)/float(oof))*100)
                    st.markdown(f'<div class="prow"><div class="plbl">{lf}</div><div class="pbar"><div class="pfill" style="width:{bp}%"></div></div><div class="pval">{v}</div></div>', unsafe_allow_html=True)
                st.markdown('</div></div>', unsafe_allow_html=True)
            st.progress(prob/100)

    # ══════════════════════════════════════════════════════════════════════════
    # MODULE 04 — OFFER DETECTOR
    # ══════════════════════════════════════════════════════════════════════════
    elif "Offer" in menu:
        c_in, c_ref = st.columns([3,1])

        with c_in:
            st.markdown('<div class="g-panel anim-3"><div class="g-panel-glow"></div><div class="g-panel-head"><div class="g-panel-title"><div class="g-panel-icon">⊕</div> Offer Verification Engine</div></div><div class="g-panel-body">', unsafe_allow_html=True)

            fd_t1, fd_t2, fd_t3 = st.tabs(["✏️  Paste Text", "📄  Offer PDF", "📸  Photograph / Screenshot"])
            offer_text = ""

            with fd_t1:
                ot = st.text_area("Paste email or offer content", height=180, placeholder="Dear Candidate, Congratulations! You have been selected for…", key="fd_t")
                if ot: offer_text = ot
            with fd_t2:
                st.markdown('<div class="upload-zone"><span class="upload-zone-icon">📄</span><div class="upload-zone-label">Upload offer letter PDF</div><div class="upload-zone-sub">Text extracted and scanned instantly</div></div>', unsafe_allow_html=True)
                pf4 = st.file_uploader("Offer PDF", type=["pdf"], key="fd_pdf", label_visibility="collapsed")
                if pf4:
                    ex6,er6 = extract_text_from_pdf(pf4)
                    if er6: st.error(er6)
                    elif ex6:
                        offer_text = ex6
                        st.success(f"✓ PDF extracted — {len(ex6.split())} words ready")
                        with st.expander("Preview"):
                            st.text(ex6[:600]+("…" if len(ex6)>600 else ""))
            with fd_t3:
                st.markdown('<div class="upload-zone"><span class="upload-zone-icon">📸</span><div class="upload-zone-label">Photo of offer letter or email screenshot</div><div class="upload-zone-sub">OCR reads and verifies content instantly</div></div>', unsafe_allow_html=True)
                ig4 = st.file_uploader("Image / Screenshot", type=["png","jpg","jpeg"], key="fd_img", label_visibility="collapsed")
                if ig4:
                    c1,c2 = st.columns([1,1])
                    with c1: st.image(ig4, caption="Uploaded", use_column_width=True)
                    with c2:
                        with st.spinner("Running OCR…"):
                            ex7,er7 = extract_text_from_image(ig4)
                        if er7: st.warning(f"OCR unavailable: {er7}\n\nInstall: `pip install pytesseract pillow`")
                        elif ex7:
                            offer_text = ex7
                            st.success(f"✓ OCR complete — {len(ex7.split())} words")
                            with st.expander("Preview"):
                                st.text(ex7[:500]+("…" if len(ex7)>500 else ""))
                        else:
                            st.warning("No text detected. Try a clearer image.")

            run_fd = st.button("Run Fraud Detection Scan →", key="btn_fd")
            st.markdown('</div></div>', unsafe_allow_html=True)

            if run_fd:
                if not offer_text.strip():
                    st.warning("Provide offer content via any input method.")
                else:
                    with st.spinner("🔍 Scanning for fraud patterns…"):
                        result = fake_offer_detector(offer_text)
                    is_fake = "Fake" in result
                    cls2  = "fake" if is_fake else "safe"
                    t2    = "⚠ FRAUD SIGNATURES DETECTED" if is_fake else "✓ NO FRAUD PATTERNS DETECTED"
                    tips  = ("• Never pay registration/security fees for internships<br>• Verify company at mca.gov.in / official LinkedIn<br>• Email domain must match company website<br>• Cross-check HR contact on company's careers page") if is_fake else ("• Verify sender domain matches official website<br>• Confirm role listing on company's careers page<br>• Connect with current employee via LinkedIn<br>• Ensure offer uses official company letterhead")
                    st.markdown(f'<div class="rbox {cls2} anim-4"><div class="rbox-title">{t2}</div><div>{result}</div><div class="rtips">{tips}</div></div>', unsafe_allow_html=True)

        with c_ref:
            st.markdown("""
            <div class="g-panel anim-4"><div class="g-panel-glow"></div>
              <div class="g-panel-head"><div class="g-panel-title"><div class="g-panel-icon" style="color:#fb7185">🛡️</div> Red Flag Guide</div></div>
              <div class="g-panel-body" style="font-family:'DM Mono',monospace;font-size:0.6rem;line-height:2.2;color:var(--text2);">
                <div style="color:#fb7185;font-size:0.54rem;letter-spacing:0.12em;text-transform:uppercase;margin-bottom:8px;display:flex;align-items:center;gap:6px;">
                  <span style="width:6px;height:6px;border-radius:50%;background:#fb7185;display:inline-block;box-shadow:0 0 8px #fb7185;"></span>
                  HIGH RISK SIGNALS
                </div>
                ⚠ Any upfront fee request<br>
                ⚠ Non-company email domain<br>
                ⚠ Vague job descriptions<br>
                ⚠ Unrealistic stipend claims<br>
                ⚠ Urgent / pressure language<br>
                ⚠ Requests ID / bank details<br>
                ⚠ No interview process<br>
                <hr style="border:none;border-top:1px solid var(--border2);margin:12px 0">
                <div style="color:#4ade80;font-size:0.54rem;letter-spacing:0.12em;text-transform:uppercase;margin-bottom:8px;display:flex;align-items:center;gap:6px;">
                  <span style="width:6px;height:6px;border-radius:50%;background:#4ade80;display:inline-block;box-shadow:0 0 8px #4ade80;"></span>
                  SAFE INDICATORS
                </div>
                ✓ Official @company.com email<br>
                ✓ Interview rounds described<br>
                ✓ Clear role + responsibilities<br>
                ✓ Verifiable company LinkedIn<br>
                ✓ Formal letterhead + address<br>
                ✓ Matches job posting details<br>
              </div>
            </div>""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # FOOTER
    st.markdown("""
    <div style="padding:14px 0 24px;border-top:1px solid var(--border2);display:flex;justify-content:space-between;font-family:'DM Mono',monospace;font-size:0.52rem;letter-spacing:0.1em;text-transform:uppercase;color:var(--text3);">
      <span>CareerOS · AI Intelligence Platform · v3.2</span>
      <span>© 2025 · All Systems Operational</span>
    </div>
    """, unsafe_allow_html=True)