import React, { useState, useEffect } from 'react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import { 
  Bot, 
  Zap, 
  CheckCircle2, 
  Loader2, 
  Copy, 
  Trophy, 
  Clock, 
  Sparkles,
  Info,
  Globe 
} from 'lucide-react';

const API_URL = "http://localhost:8000";

const Nav = () => (
    <nav className="nav-container animate-fade-in">
        <div className="logo">
           <div className="p-2 border border-blue-500/20 rounded-xl bg-blue-500/5">
                <Bot className="w-5 h-5 text-blue-500" />
           </div>
           <span>AI Agent Manager</span>
        </div>
    </nav>
);

const LoadingModal = () => (
    <div className="modal-overlay">
        <div className="honeycomb scale-[2] translate-y-[-20px]">
            <div></div>
            <div></div>
            <div></div>
            <div></div>
            <div></div>
            <div></div>
            <div></div>
        </div>
    </div>
);

function App() {
  const [topic, setTopic] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [showModal, setShowModal] = useState(false);
  
  const [steps, setSteps] = useState([
    { title: "Market Trend Analysis", description: "Scraping competitor gaps and content opportunities.", status: 'idle' },
    { title: "Semantic Keyword Mapping", description: "Generating primary and LSI keyword clusters.", status: 'idle' },
    { title: "Brand Identity Sync", description: "Infecting model context with Cubemoons brand voice.", status: 'idle' },
    { title: "SEO Content Blueprint", description: "Calculating optimal H1-H3 hierarchy and metadata.", status: 'idle' },
    { title: "AI Core Generation", description: "Drafting high-fidelity content via Llama 3 API.", status: 'idle' },
    { title: "SEO Health Validation", description: "Calculated scoring and keyword density polishing.", status: 'idle' },
  ]);

  const handleGenerate = async () => {
    if (!topic) return;
    setLoading(true);
    setResult(null);
    setError(null);
    setShowModal(true);
    setSteps(prev => prev.map(s => ({ ...s, status: 'idle' })));

    try {
      const updateStep = (index, status) => {
        setSteps(prev => {
          const newSteps = [...prev];
          newSteps[index].status = status;
          return newSteps;
        });
      };

      updateStep(0, 'active');
      const response = await axios.post(`${API_URL}/generate-blog`, { topic });
      
      // Visual feedback loop
      for(let i = 0; i < steps.length; i++) {
        updateStep(i, 'active');
        await new Promise(r => setTimeout(r, 600));
        updateStep(i, 'completed');
      }

      setResult(response.data);
      setShowModal(false);
    } catch (err) {
      setError(err.response?.data?.detail || "System connection timeout. Please check your internet or correct API keys.");
      console.error(err);
      setShowModal(false);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen">
      <div className="glow-bg">
        <div className="glow-1" />
        <div className="glow-2" />
      </div>

      <Nav />

      {showModal && <LoadingModal />}

      <main className="w-full max-w-7xl mx-auto px-6 flex flex-col items-center">
        {/* Hero Section */}
        <section className="hero-section text-center max-w-4xl w-full mx-auto">
          <div className="flex items-center justify-center gap-2 mb-6 px-4 py-1.5 bg-white/5 border border-white/10 rounded-full w-fit mx-auto animate-fade-in">
             <Sparkles className="w-3.5 h-3.5 text-[#ff00ff]" />
             <span className="text-[10px] font-bold tracking-[0.2em] text-white/50 uppercase">Autonomous Intelligence</span>
          </div>

          <h1 className="gradient-text leading-[1.1]">
            Unlimited <br /> 
            Digital Blog Engine
          </h1>
          
          <p className="sub-heading mt-6 leading-relaxed">
             The autonomous SEO-pipeline designed for hyper-growth enterprises.
             Enter a topic to activate the multi-agent orchestration.
          </p>

          <div className="input-container glass transition-all focus-within:ring-1 ring-[#ff00ff]/30">
            <input 
              type="text" 
              placeholder="e.g. How to use AI in Web Design..." 
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleGenerate()}
            />
            <button 
              onClick={handleGenerate}
              className="main-button text-sm"
              disabled={loading}
            >
              {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : "Initiate Gen Pipeline"}
            </button>
          </div>
        </section>

        {/* Status Error Display */}
        {error && (
            <div className="max-w-md p-4 bg-red-500/10 border border-red-500/20 rounded-xl mt-8 text-red-500 text-xs font-medium flex items-center gap-3">
                <Info className="w-4 h-4" />
                {error}
            </div>
        )}

        {/* Result Area */}
        {result && (
          <div className="w-full flex justify-center">
            <div className="result-card mb-24 animate-fade-in max-w-4xl w-full" style={{ animationDelay: '0.2s' }}>
                <div className="result-header">
                <div className="w-full text-left">
                    <h2 className="text-4xl font-bold mb-4 leading-tight">{result.title}</h2>
                    <div className="flex items-center gap-6 mt-4 text-xs text-white/40 font-medium">
                    <span className="flex items-center gap-1.5 font-bold"><Trophy className="w-3.5 h-3.5 text-[#ff00ff]" /> {result.seo_score}% SEO Health</span>
                    </div>
                </div>
                <div className="flex gap-2">
                    <button 
                    onClick={() => navigator.clipboard.writeText(result.content)}
                    className="p-3 bg-white/5 border border-white/10 rounded-xl hover:bg-white/10 transition-all text-white/70"
                    >
                    <Copy className="w-4 h-4" />
                    </button>
                </div>
                </div>

                <div className="mt-12 pt-12 border-t border-white/5 w-full">
                    {/* Meta Summary at Top */}
                    <div className="mb-12 p-8 bg-white/5 border border-white/10 rounded-2xl text-left italic text-white/50 font-light leading-relaxed">
                    "{result.meta}"
                    </div>

                    {/* Content */}
                    <div className="prose max-w-none text-left">
                    <ReactMarkdown>{result.content}</ReactMarkdown>
                    </div>

                    {/* Keywords at Bottom */}
                    <div className="mt-16 pt-8 border-t border-white/5 flex flex-wrap gap-3">
                    {Array.isArray(result.keywords?.primary) ? result.keywords.primary.map((k, i) => (
                        <span key={i} className="px-3 py-1.5 bg-[#ff00ff]/10 text-[#ff00ff] border border-[#ff00ff]/20 rounded-lg text-xs font-bold">#{k}</span>
                    )) : result.keywords?.primary && (
                        <span className="px-3 py-1.5 bg-[#ff00ff]/10 text-[#ff00ff] border border-[#ff00ff]/20 rounded-lg text-xs font-bold">#{result.keywords.primary}</span>
                    )}
                    
                    {Array.isArray(result.keywords?.secondary) && result.keywords.secondary.map((k, i) => (
                        <span key={i} className="px-3 py-1.5 bg-white/5 text-white/40 border border-white/10 rounded-lg text-xs font-bold">#{k}</span>
                    ))}
                    </div>
                </div>
            </div>
          </div>
        )}
      </main>

      <footer className="py-12 border-t border-white/5 mt-20 opacity-30 text-center">
          <div className="flex items-center justify-center gap-2 mb-4">
             <div className="w-2 h-2 rounded-full bg-emerald-500" />
             <span className="text-[10px] font-bold tracking-widest uppercase">Nodes Online - Pipeline Ready</span>
          </div>
          <p className="text-[10px] text-white/40">© 2026 AI Agent Engine. Dynamic Content Synthesis Ready.</p>
      </footer>
    </div>
  );
}

export default App;
