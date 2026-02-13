import React, { useState, useEffect } from "react";
import { Button } from "../../components/ui/Button";
import { Card } from "../../components/ui/Card";
import { Scan, FileText, Zap, Shield, CheckCircle, PenLine, ShieldCheck } from "lucide-react";

interface HomePageProps {
  onNavigate: (page: "upload") => void;
}

const HomePage: React.FC<HomePageProps> = ({ onNavigate }) => {
  const [mousePos, setMousePos] = useState({ x: 0, y: 0 });

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      setMousePos({
        x: (e.clientX / window.innerWidth - 0.5) * 20,
        y: (e.clientY / window.innerHeight - 0.5) * 20,
      });
    };
    window.addEventListener("mousemove", handleMouseMove);
    return () => window.removeEventListener("mousemove", handleMouseMove);
  }, []);

  return (
    <div className="relative min-h-screen overflow-hidden bg-[#0B0F19]">
      {/* Mesh Background Pattern */}
      <div className="absolute inset-0 -z-30 opacity-20">
        <div className="absolute inset-0 bg-[radial-gradient(at_top_right,rgba(99,102,241,0.1),transparent_50%),radial-gradient(at_bottom_left,rgba(216,180,254,0.05),transparent_50%)]" />
      </div>

      {/* Interactive Background Layer */}
      <div 
        className="absolute inset-0 -z-20 transition-transform duration-75 ease-out pointer-events-none"
        style={{ 
          transform: `translate(${mousePos.x}px, ${mousePos.y}px)` 
        }}
      >
        {/* Animated Gradient Orbs */}
        <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-action-primary/20 blur-[120px] rounded-full animate-pulse-slow" />
        <div className="absolute bottom-[-10%] right-[-10%] w-[50%] h-[50%] bg-ai-highlight1/15 blur-[150px] rounded-full animate-float" />
        <div className="absolute top-[20%] right-[10%] w-[30%] h-[30%] bg-ai-highlight2/10 blur-[100px] rounded-full animate-pulse-slow [animation-delay:2s]" />
        
        {/* Moving Light Beam */}
        <div 
          className="absolute top-0 left-0 w-full h-full opacity-30 mix-blend-soft-light"
          style={{
            background: `radial-gradient(circle at ${50 + mousePos.x}% ${50 + mousePos.y}%, rgba(99, 102, 241, 0.15) 0%, transparent 50%)`
          }}
        />
      </div>

      {/* Grid & Noise Overlays */}
      <div className="absolute inset-0 -z-10 pointer-events-none">
        <div className="absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-20 mix-blend-overlay" />
        <div className="absolute inset-0 bg-[linear-gradient(to_right,#80808012_1px,transparent_1px),linear-gradient(to_bottom,#80808012_1px,transparent_1px)] bg-[size:40px_40px] [mask-image:radial-gradient(ellipse_60%_50%_at_50%_0%,#000_70%,transparent_100%)]" />
      </div>

      <div className="relative z-10 animate-fade-in">
        {/* Hero Section */}
        <section className="pt-24 pb-32 relative max-w-7xl mx-auto px-4">
          <div className="flex flex-col lg:flex-row items-start gap-12 lg:gap-20">
            {/* Left Column: Content (60%) */}
            <div className="lg:w-[60%] text-left space-y-8 flex flex-col items-start">
              <div className="inline-flex items-center justify-center p-1 rounded-full bg-white/5 backdrop-blur-md border border-white/10 group hover:scale-105 transition-all duration-300 shadow-xl shadow-black/20">
                <div className="bg-[#0B0F19]/60 rounded-full px-5 py-1.5 flex items-center gap-2.5">
                  <Scan className="w-4 h-4 text-action-primary animate-pulse" />
                  <span className="text-xs font-bold text-text-neutral/70 tracking-widest uppercase">Next-Gen OCR Engine</span>
                </div>
              </div>
              
              <h1 
                className="text-6xl md:text-7xl lg:text-8xl font-bold tracking-tight leading-[1.05] transition-transform duration-300 ease-out text-left"
                style={{ transform: `translate(${mousePos.x * -0.1}px, ${mousePos.y * -0.1}px)` }}
              >
                Unlock the Power of <br />
                <span className="text-transparent bg-clip-text bg-gradient-to-r from-action-primary via-ai-highlight1 to-action-primary bg-[length:200%_auto] animate-gradient">
                  Your Documents
                </span>
              </h1>
              
              <p className="max-w-2xl text-lg md:text-xl text-text-secondary leading-relaxed font-normal opacity-70 text-left">
                DocVision AI uses enterprise-grade transformers to extract structured data 
                from invoices, forms, and handwritten notes with human-level accuracy.
              </p>
              
              <div className="flex flex-col sm:flex-row justify-start items-center gap-5 pt-4">
                <Button size="lg" onClick={() => onNavigate("upload")} className="text-lg px-8 py-6 h-auto rounded-xl shadow-[0_0_20px_rgba(168,85,247,0.3)] hover:shadow-[0_0_30px_rgba(168,85,247,0.5)] transition-all duration-500 group relative overflow-hidden bg-action-primary border-none">
                  <span className="relative z-10 flex items-center font-bold">
                    Start Free Extraction
                    <Zap className="ml-2 w-5 h-5 group-hover:fill-current group-hover:scale-125 transition-transform duration-300" />
                  </span>
                </Button>
                <Button variant="outline" size="lg" className="text-lg px-8 py-6 h-auto rounded-xl border-white/10 bg-transparent hover:bg-white/5 backdrop-blur-sm transition-all duration-300 font-bold text-text-neutral">
                  Enterprise Demo
                </Button>
              </div>
            </div>

            {/* Right Column: Dashboard Mockup (40%) */}
            <div className="lg:w-[40%] w-full relative group">
              <div className="relative rounded-2xl overflow-hidden border border-white/10 bg-white/5 backdrop-blur-xl shadow-[0_0_50px_rgba(0,0,0,0.5)] animate-slide-up transition-transform duration-500 hover:scale-[1.02]">
                <div className="p-1 bg-gradient-to-br from-white/10 to-transparent">
                  <div className="relative aspect-[16/12] bg-[#0B0F19]/80 rounded-xl overflow-hidden">
                    {/* Floating Glows */}
                    <div className="absolute top-0 right-0 w-32 h-32 bg-action-primary/20 blur-[60px] rounded-full" />
                    <div className="absolute bottom-0 left-0 w-32 h-32 bg-ai-highlight1/10 blur-[60px] rounded-full" />

                    <div className="absolute inset-0 p-6 flex flex-col">
                      <div className="flex items-center justify-between mb-6 border-b border-white/5 pb-4">
                        <div className="flex items-center gap-2">
                          <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
                          <span className="text-[10px] font-bold text-white/50 tracking-widest uppercase">Live Processing</span>
                        </div>
                        <div className="flex gap-1.5">
                          <div className="w-2 h-2 rounded-full bg-white/10" />
                          <div className="w-2 h-2 rounded-full bg-white/10" />
                          <div className="w-2 h-2 rounded-full bg-white/10" />
                        </div>
                      </div>

                      <div className="flex-1 flex gap-4 overflow-hidden">
                        {/* Left side: Document */}
                        <div className="flex-1 bg-white/5 rounded-lg border border-white/10 p-4 space-y-3 opacity-60 overflow-hidden">
                          <div className="h-1.5 w-1/2 bg-white/20 rounded" />
                          <div className="h-10 w-full border border-white/10 rounded-md bg-white/5" />
                          <div className="h-10 w-full border border-white/10 rounded-md bg-white/5" />
                          <div className="h-10 w-full border border-white/10 rounded-md bg-white/5" />
                          <div className="h-1.5 w-3/4 bg-white/20 rounded pt-2" />
                        </div>
                        
                        {/* Right side: JSON Code */}
                        <div className="flex-1 bg-black/60 rounded-lg border border-action-primary/30 p-4 font-mono text-[11px] text-action-primary overflow-hidden relative shadow-[0_0_20px_rgba(99,102,241,0.2)]">
                          <div className="text-white/40 mb-1">{"{"}</div>
                          <div className="pl-3"><span className="text-ai-highlight1">"type"</span>: "Invoice",</div>
                          <div className="pl-3"><span className="text-ai-highlight1">"id"</span>: <span className="text-ai-highlight2">"INV-001"</span>,</div>
                          <div className="pl-3"><span className="text-ai-highlight1">"date"</span>: <span className="text-ai-highlight2">"2024-02"</span>,</div>
                          <div className="pl-3"><span className="text-ai-highlight1">"total"</span>: <span className="text-ai-highlight2">1240.50</span>,</div>
                          <div className="pl-3"><span className="text-ai-highlight1">"status"</span>: <span className="text-ai-highlight2">"parsed"</span></div>
                          <div className="text-white/40 mt-1">{"}"}</div>
                          
                          {/* Inner glow for JSON */}
                          <div className="absolute inset-0 shadow-[inset_0_0_15px_rgba(99,102,241,0.1)] pointer-events-none" />
                        </div>
                      </div>

                      {/* Scanning Line */}
                      <div className="absolute inset-x-0 top-0 h-[1px] bg-gradient-to-r from-transparent via-action-primary to-transparent animate-[scan_4s_ease-in-out_infinite] pointer-events-none opacity-50" />
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Features & About Section */}
        <section id="features" className="py-32 relative overflow-hidden">
          <div className="max-w-7xl mx-auto px-4 relative z-10">
            <div className="flex flex-col items-center text-center mb-20">
              <h2 className="text-4xl md:text-5xl font-bold text-white mb-6 tracking-tight">
                Enterprise-Grade <span className="text-action-primary">Capabilities</span>
              </h2>
              <p className="max-w-2xl text-text-secondary text-lg opacity-70">
                DocVision AI combines state-of-the-art vision transformers with enterprise security 
                to transform how your organization handles document data.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <FeatureCard 
                icon={<CheckCircle className="w-8 h-8 text-ai-highlight2" />}
                title="Automatic Data Extraction"
                description="Zero-shot extraction of structured fields from any document type without pre-defined templates or manual rules."
              />
              <FeatureCard 
                icon={<PenLine className="w-8 h-8 text-action-primary" />}
                title="Handwritten Text Recognition"
                description="Human-level accuracy on cursive, messy, or faded handwriting using our proprietary deep learning models."
              />
              <FeatureCard 
                icon={<ShieldCheck className="w-8 h-8 text-ai-highlight1" />}
                title="Enterprise-Grade Security"
                description="End-to-end encryption, SOC2 compliance, and automated PII masking to keep your sensitive data protected."
              />
            </div>
          </div>

          {/* Background depth for features */}
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[400px] bg-action-primary/5 blur-[120px] rounded-full pointer-events-none" />
        </section>

        {/* Trust Section / Stats */}
        <section className="pb-32">
          <div className="max-w-4xl mx-auto px-4">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-8 py-16 border-y border-white/10 relative group bg-white/5 backdrop-blur-sm rounded-3xl overflow-hidden">
              <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/5 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-1000 ease-in-out pointer-events-none" />
              <StatItem label="Accuracy" value="99.9%" />
              <StatItem label="Processing" value="< 2s" />
              <StatItem label="Formats" value="50+" />
              <StatItem label="Secure" value="SOC2" />
            </div>
          </div>
        </section>
      </div>
    </div>
  );
};

const FeatureCard: React.FC<{ icon: React.ReactNode; title: string; description: string }> = ({ icon, title, description }) => (
  <div className="group relative">
    {/* Subtle glow behind card */}
    <div className="absolute -inset-0.5 bg-gradient-to-r from-action-primary/20 to-ai-highlight1/20 rounded-[2rem] blur opacity-0 group-hover:opacity-100 transition duration-500" />
    
    <div className="relative h-full bg-[#161B26] border border-white/5 rounded-[2rem] p-10 hover:border-action-primary/50 transition-all duration-500 flex flex-col items-start text-left shadow-2xl shadow-black/50">
      <div className="w-16 h-16 rounded-2xl bg-white/5 flex items-center justify-center mb-8 group-hover:scale-110 transition-transform duration-500 ring-1 ring-white/10">
        {icon}
      </div>
      <h3 className="text-2xl font-bold text-white mb-4 group-hover:text-action-primary transition-colors">
        {title}
      </h3>
      <p className="text-text-secondary leading-relaxed opacity-70 group-hover:opacity-100 transition-opacity">
        {description}
      </p>
    </div>
  </div>
);

const StatItem: React.FC<{ label: string; value: string }> = ({ label, value }) => (
  <div className="text-center relative z-10">
    <div className="text-3xl font-bold text-white mb-1">{value}</div>
    <div className="text-xs text-text-secondary uppercase tracking-widest font-bold opacity-50">{label}</div>
  </div>
);

export default HomePage;
