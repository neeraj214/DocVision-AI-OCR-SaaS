import React from "react";
import { Button } from "../../components/ui/Button";
import { Card } from "../../components/ui/Card";
import { Scan, FileText, Zap, Shield } from "lucide-react";

interface HomePageProps {
  onNavigate: (page: "upload") => void;
}

const HomePage: React.FC<HomePageProps> = ({ onNavigate }) => {
  return (
    <div className="space-y-16 animate-fade-in">
      {/* Hero Section */}
      <section className="text-center space-y-8 py-20 relative">
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[500px] h-[500px] bg-action-primary/20 blur-[100px] rounded-full -z-10" />
        
        <div className="inline-flex items-center justify-center p-4 bg-action-primary/10 rounded-full mb-4 ring-1 ring-action-primary/20 shadow-lg shadow-action-primary/20">
          <Scan className="w-10 h-10 text-action-primary" />
        </div>
        
        <h1 className="text-5xl md:text-7xl font-extrabold text-text-neutral tracking-tight leading-tight">
          Transform Images into <br />
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-action-primary via-ai-highlight1 to-action-primary bg-[length:200%_auto] animate-gradient">
            Actionable Text
          </span>
        </h1>
        
        <p className="max-w-2xl mx-auto text-xl text-text-secondary leading-relaxed">
          DocVision AI uses advanced optical character recognition to extract text,
          tables, and structure from your documents in seconds.
        </p>
        
        <div className="flex flex-col sm:flex-row justify-center gap-4 pt-8">
          <Button size="lg" onClick={() => onNavigate("upload")} className="text-lg px-8 py-4 h-auto">
            Start OCR Now
          </Button>
          <Button variant="secondary" size="lg" className="text-lg px-8 py-4 h-auto">
            View Documentation
          </Button>
        </div>
      </section>

      {/* Features Grid */}
      <section className="grid md:grid-cols-3 gap-8">
        <FeatureCard
          icon={<Zap className="w-6 h-6 text-ai-highlight2" />}
          title="Lightning Fast"
          description="Process documents in milliseconds with our optimized inference engine."
        />
        <FeatureCard
          icon={<FileText className="w-6 h-6 text-action-primary" />}
          title="Structured Output"
          description="Get results in plain text, structured JSON, or searchable PDF formats."
        />
        <FeatureCard
          icon={<Shield className="w-6 h-6 text-ai-highlight1" />}
          title="Secure & Private"
          description="Your documents are processed in ephemeral containers and never stored."
        />
      </section>
    </div>
  );
};

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
