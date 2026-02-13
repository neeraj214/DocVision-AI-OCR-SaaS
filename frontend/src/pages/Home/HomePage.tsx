import React, { useState, useEffect } from "react";
import { Button } from "../../components/ui/Button";
import { Card } from "../../components/ui/Card";
import { Scan, FileText, Zap, Shield } from "lucide-react";

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
    <div className="relative min-h-screen overflow-hidden bg-primary-base">
      {/* Mesh Background Pattern */}
      <div className="absolute inset-0 -z-30 opacity-30">
        <div className="absolute inset-0 bg-[radial-gradient(at_top_right,rgba(99,102,241,0.15),transparent_50%),radial-gradient(at_bottom_left,rgba(216,180,254,0.1),transparent_50%)]" />
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
        <section className="pt-20 pb-32 relative max-w-7xl mx-auto px-4">
          <div className="flex flex-col lg:flex-row items-center gap-16">
            {/* Left Column: Content */}
            <div className="flex-1 text-left space-y-10">
              <div className="inline-flex items-center justify-center p-1 rounded-full bg-white/5 backdrop-blur-md border border-white/10 p-[1px] group hover:scale-105 transition-all duration-300 shadow-xl shadow-black/20">
                <div className="bg-primary-base/40 rounded-full px-6 py-2 flex items-center gap-3">
                  <Scan className="w-5 h-5 text-action-primary animate-pulse" />
                  <span className="text-sm font-bold text-text-neutral/80 tracking-wider uppercase">Next-Gen OCR Engine</span>
                </div>
              </div>
              
              <h1 
                className="text-6xl md:text-7xl lg:text-8xl tracking-tight leading-[1.1] transition-transform duration-300 ease-out"
                style={{ transform: `translate(${mousePos.x * -0.2}px, ${mousePos.y * -0.2}px)` }}
              >
                <span className="font-bold text-text-neutral">Unlock the Power of</span> <br />
                <span className="font-bold text-transparent bg-clip-text bg-gradient-to-r from-action-primary via-ai-highlight1 to-action-primary bg-[length:200%_auto] animate-gradient">
                  Your Documents
                </span>
              </h1>
              
              <p className="max-w-[50ch] text-xl text-text-secondary leading-relaxed font-normal opacity-80">
                DocVision AI uses enterprise-grade transformers to extract structured data 
                from invoices, forms, and handwritten notes with human-level accuracy.
              </p>
              
              <div className="flex flex-col sm:flex-row justify-start items-center gap-6 pt-4">
                <Button size="lg" onClick={() => onNavigate("upload")} className="text-lg px-8 py-6 h-auto rounded-xl shadow-2xl shadow-action-primary/30 hover:shadow-action-primary/50 transition-all duration-500 group relative overflow-hidden bg-action-primary">
                  <span className="relative z-10 flex items-center font-bold">
                    Start Free Extraction
                    <Zap className="ml-2 w-5 h-5 group-hover:fill-current group-hover:scale-125 transition-transform duration-300" />
                  </span>
                </Button>
                <Button variant="secondary" size="lg" className="text-lg px-8 py-6 h-auto rounded-xl border-white/10 bg-white/5 hover:bg-white/10 backdrop-blur-sm transition-all duration-300 font-bold text-text-neutral">
                  Enterprise Demo
                </Button>
              </div>
            </div>

            {/* Right Column: Product Preview */}
            <div className="flex-1 w-full max-w-2xl">
              <div className="relative rounded-2xl overflow-hidden border border-white/10 bg-white/5 backdrop-blur-xl shadow-2xl animate-slide-up group">
                <div className="flex flex-col items-stretch">
                  {/* Before/After Visualization */}
                  <div className="p-1 bg-gradient-to-br from-white/10 to-transparent">
                    <div className="relative aspect-[16/10] bg-black/40 rounded-xl overflow-hidden">
                      {/* Image representation matching the screenshot */}
                      <div className="absolute inset-0 p-8 flex gap-4">
                        {/* Left side: Doc representation */}
                        <div className="flex-1 bg-white/5 rounded-lg border border-white/10 p-4 space-y-3 opacity-60">
                          <div className="h-2 w-1/2 bg-white/20 rounded" />
                          <div className="h-12 w-full border border-white/10 rounded" />
                          <div className="h-12 w-full border border-white/10 rounded" />
                          <div className="h-12 w-full border border-white/10 rounded" />
                        </div>
                        {/* Right side: Code representation */}
                        <div className="flex-1 bg-black/60 rounded-lg border border-white/10 p-4 font-mono text-[10px] text-action-primary/80 overflow-hidden">
                          <div className="text-white/40">{"{"}</div>
                          <div className="pl-2">"id": "INV-001",</div>
                          <div className="pl-2">"date": "2024-02-12",</div>
                          <div className="pl-2">"total": 1240.50,</div>
                          <div className="pl-2">"items": [...]</div>
                          <div className="text-white/40">{"}"}</div>
                        </div>
                        {/* Connecting arrows animation */}
                        <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
                          <div className="w-full h-[1px] bg-gradient-to-r from-transparent via-action-primary/50 to-transparent animate-pulse" />
                        </div>
                      </div>
                      
                      {/* Scanning line */}
                      <div className="absolute inset-0 bg-gradient-to-b from-transparent via-action-primary/20 to-transparent h-1/2 w-full animate-[scan_4s_ease-in-out_infinite] pointer-events-none" />
                      
                      {/* Floating UI Elements */}
                      <div className="absolute top-4 left-4 flex items-center gap-2 px-2 py-1 rounded bg-black/60 border border-white/10">
                        <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
                        <span className="text-[10px] font-bold text-white/60">LIVE PROCESSING</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Logo Cloud Section - Redesigned to match image */}
        <section className="bg-white py-16">
          <div className="max-w-7xl mx-auto px-4">
            <div className="flex flex-col lg:flex-row items-center justify-between gap-12">
              <div className="text-left">
                <h3 className="text-2xl font-bold text-primary-base mb-4">Trusted by</h3>
                <div className="flex items-center gap-4">
                  <div className="flex items-center gap-2 bg-primary-base text-white px-4 py-2 rounded-lg text-sm font-bold">
                    <Shield className="w-4 h-4 text-ai-highlight2" />
                    SOC2 Compliant
                  </div>
                  <div className="text-primary-base/40 font-bold text-sm">
                    AES-256 Encrypted
                  </div>
                </div>
              </div>

              <div className="flex flex-wrap justify-center items-center gap-8 md:gap-12 lg:gap-16 opacity-60 grayscale hover:grayscale-0 transition-all duration-700">
                <LogoItemDark name="InnovateCorp" />
                <LogoItemDark name="GlobalFlow" />
                <LogoItemDark name="DataPrime" />
                <LogoItemDark name="NexusTech" />
              </div>
            </div>
          </div>
        </section>

        {/* Stats / Proof Section */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-8 max-w-4xl mx-auto py-24 border-y border-white/5 relative group">
          <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/5 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-1000 ease-in-out pointer-events-none" />
          <StatItem label="Accuracy" value="99.9%" />
          <StatItem label="Processing" value="< 2s" />
          <StatItem label="Formats" value="50+" />
          <StatItem label="Secure" value="SOC2" />
        </div>

        {/* Security Trust Badges */}
        <div className="flex justify-center gap-8 py-8 opacity-60">
          <div className="flex items-center gap-2 text-xs font-bold text-text-secondary border border-white/10 rounded-lg px-4 py-2 backdrop-blur-sm">
            <Shield className="w-4 h-4 text-ai-highlight2" />
            SOC2 COMPLIANT
          </div>
          <div className="flex items-center gap-2 text-xs font-bold text-text-secondary border border-white/10 rounded-lg px-4 py-2 backdrop-blur-sm">
            <Zap className="w-4 h-4 text-action-primary" />
            AES-256 ENCRYPTED
          </div>
        </div>

        {/* Features Grid */}
        <section className="grid md:grid-cols-3 gap-8 px-4 max-w-7xl mx-auto">
          <FeatureCard
            icon={<Zap className="w-8 h-8 text-ai-highlight2" />}
            title="Transformer OCR"
            description="Leverage TrOCR and Vision Transformers for unmatched character recognition even in low-quality scans."
          />
          <FeatureCard
            icon={<FileText className="w-8 h-8 text-action-primary" />}
            title="Intelligent Routing"
            description="Our AI classifier automatically routes documents to the specialized engine for the best possible results."
          />
          <FeatureCard
            icon={<Shield className="w-8 h-8 text-ai-highlight1" />}
            title="Data Governance"
            description="Enterprise-grade encryption and PII masking ensure your sensitive financial data remains private."
          />
        </section>
      </div>
    </div>
  );
};

const LogoItemDark: React.FC<{ name: string }> = ({ name }) => (
  <div className="flex items-center gap-2 group/logo">
    <div className="w-8 h-8 rounded bg-primary-base/10 flex items-center justify-center font-black text-xs text-primary-base group-hover/logo:bg-action-primary group-hover/logo:text-white transition-colors">
      {name[0]}
    </div>
    <span className="font-bold tracking-tight text-lg text-primary-base group-hover/logo:text-action-primary transition-colors">{name}</span>
  </div>
);

const LogoItem: React.FC<{ name: string }> = ({ name }) => (
  <div className="flex items-center gap-2 group/logo">
    <div className="w-8 h-8 rounded bg-white/10 flex items-center justify-center font-black text-xs group-hover/logo:bg-action-primary/20 group-hover/logo:text-action-primary transition-colors">
      {name[0]}
    </div>
    <span className="font-bold tracking-tight text-lg group-hover/logo:text-white transition-colors">{name}</span>
  </div>
);

const StatItem: React.FC<{ label: string; value: string }> = ({ label, value }) => (
  <div className="text-center">
    <div className="text-2xl font-bold text-text-neutral">{value}</div>
    <div className="text-sm text-text-secondary uppercase tracking-widest">{label}</div>
  </div>
);

const FeatureCard: React.FC<{
  icon: React.ReactNode;
  title: string;
  description: string;
}> = ({ icon, title, description }) => (
  <Card className="p-8 hover:bg-white/10 transition-colors group border-white/5">
    <div className="mb-6 p-3 bg-white/5 w-fit rounded-lg group-hover:scale-110 transition-transform duration-300 ring-1 ring-white/10">
      {icon}
    </div>
    <h3 className="text-xl font-bold text-text-neutral mb-3">{title}</h3>
    <p className="text-text-secondary leading-relaxed">{description}</p>
  </Card>
);

export default HomePage;
