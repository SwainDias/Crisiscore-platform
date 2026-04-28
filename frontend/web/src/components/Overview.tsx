import React from 'react';
import { motion } from 'motion/react';
import { 
  Users, AlertCircle, MapPin, Timer, 
  ChevronRight, Phone, MessageSquare, ShieldCheck
} from 'lucide-react';
import { cn } from '../lib/utils';

export default function Overview() {
  return (
    <div className="space-y-10">
      {/* Header */}
      <div className="max-w-2xl">
         <h2 className="text-6xl font-sans font-black tracking-tighter text-on-surface leading-none mb-4 uppercase">Command</h2>
         <div className="flex items-center gap-3">
            <div className="w-2.5 h-2.5 rounded-full bg-primary animate-pulse shadow-lg shadow-primary/40" />
            <p className="text-xs font-black text-primary tracking-[0.4em] uppercase">Precision Control System v4.2</p>
         </div>
      </div>

      <div className="center-grid grid grid-cols-12 gap-10">
        {/* Main Perspective */}
        <div className="col-span-12 lg:col-span-8 flex flex-col gap-10">
           {/* Interactive Floor Overview */}
           <div className="relative h-[600px] bg-surface-dim rounded-[48px] overflow-hidden shadow-2xl border border-secondary/5 group">
              <img 
                src="https://images.unsplash.com/photo-1542661062-843818e98031?auto=format&fit=crop&q=80&w=2000" 
                className="w-full h-full object-cover opacity-40 grayscale contrast-150 scale-110 group-hover:scale-100 transition-transform duration-[20s] linear"
                alt="Floor Plan"
              />
              <div className="absolute inset-0 bg-gradient-to-tr from-primary/5 to-transparent shadow-inner" />
              
              <div className="absolute bottom-10 left-1/2 -translate-x-1/2 flex gap-3 bg-surface-container-highest/80 backdrop-blur-2xl p-2 rounded-full border border-white/10 shadow-2xl">
                 {['FL1', 'FL2', 'FL3', 'FL4'].map(fl => (
                   <button key={fl} className={cn(
                     "w-14 h-14 rounded-full font-black text-xs transition-all",
                     fl === 'FL3' ? "bg-primary text-on-primary shadow-xl" : "hover:bg-surface-variant text-on-surface-variant"
                   )}>{fl}</button>
                 ))}
              </div>

              {/* Ping Marker */}
              <div className="absolute top-1/3 left-1/2 -translate-x-1/2 -translate-y-1/2">
                <div className="w-48 h-48 bg-error/20 rounded-full animate-ping absolute -top-16 -left-16" />
                <div className="w-16 h-16 bg-error text-on-error rounded-full flex items-center justify-center shadow-2xl relative z-20 ring-4 ring-white/10">
                   <AlertCircle className="w-8 h-8 fill-current" />
                </div>
              </div>

              {/* Floating Alert Panel at bottom of map */}
              <div className="absolute bottom-28 left-10 right-10 z-30">
                <motion.div 
                  initial={{ y: 20, opacity: 0 }}
                  animate={{ y: 0, opacity: 1 }}
                  className="bg-error-container text-on-error-container rounded-[40px] p-8 flex items-center justify-between shadow-2xl border border-error/10 backdrop-blur-3xl"
                >
                   <div className="flex items-center gap-8">
                     <div className="w-16 h-16 bg-on-error-container rounded-3xl flex items-center justify-center text-error-container shadow-lg">
                        <AlertCircle className="w-10 h-10 animate-pulse" />
                     </div>
                     <div className="space-y-1">
                        <h2 className="text-2xl font-black tracking-tight uppercase leading-none">Active Incident: Fire - Floor 3, Wing B</h2>
                        <p className="text-sm font-bold opacity-80 uppercase tracking-widest">12 Responders Deployed • 45 Guests in Danger Zone</p>
                     </div>
                   </div>
                   <button className="bg-surface-container-lowest text-error-container px-10 py-5 rounded-3xl uppercase tracking-widest font-black text-xs hover:bg-error-container hover:text-white transition-all shadow-xl active:scale-95">
                      View Full Incident
                   </button>
                </motion.div>
              </div>
           </div>
        </div>

        {/* Analytics Aside */}
        <aside className="col-span-12 lg:col-span-4 flex flex-col gap-10">
           <div>
              <h3 className="text-xs font-black text-primary tracking-[0.4em] uppercase mb-8">System Analytics</h3>
              <div className="grid grid-cols-1 gap-6">
                 <AnalyticsMetric label="Staff On-Duty" value="142" />
                 <AnalyticsMetric label="Active Incidents" value="01" isError />
                 <AnalyticsMetric label="Guests Tracked" value="856" />
                 <AnalyticsMetric label="Avg Response" value="2" sub="m" value2="14" sub2="s" />
              </div>
           </div>

           <div>
              <div className="flex items-center justify-between mb-6">
                <h3 className="text-xs font-black text-on-surface-variant tracking-[0.4em] uppercase">Live Responders</h3>
                <div className="w-2 h-2 rounded-full bg-primary animate-pulse" />
              </div>
              <div className="space-y-4">
                 <ResponderMini init="JD" name="John Doe" role="Security Lead" status="En Route" />
                 <ResponderMini init="AS" name="Alice Smith" role="Medical" status="On Scene" />
              </div>
           </div>

           <div className="mt-4">
              <h3 className="text-xs font-black text-on-surface-variant tracking-[0.4em] uppercase mb-6">Historical Queue</h3>
              <div className="space-y-8 ml-2 border-l-2 border-secondary/5 pr-4">
                 <HistoryItem title="Medical Assist" time="10M AGO" location="Pool Deck • Resolved" />
                 <HistoryItem title="Noise Complaint" time="1H AGO" location="Room 402 • Closed" />
              </div>
           </div>
        </aside>
      </div>
    </div>
  );
}

function AnalyticsMetric({ label, value, sub, value2, sub2, isError }: any) {
  return (
    <div className={cn(
      "p-8 rounded-[40px] border border-secondary/5 transition-all group cursor-default",
      isError ? "bg-error/10 border-error/10" : "bg-surface-container-high hover:border-primary/20"
    )}>
       <div className={cn("text-[10px] font-black uppercase tracking-widest mb-2", isError ? "text-error" : "text-on-surface-variant")}>{label}</div>
       <div className="flex items-baseline gap-1">
          <span className={cn("text-6xl font-black font-sans leading-none", isError ? "text-error" : "text-on-surface")}>{value}</span>
          {sub && <span className="text-2xl font-bold opacity-50 lowercase">{sub}</span>}
          {value2 && <span className="text-6xl font-black font-sans leading-none ml-2">{value2}</span>}
          {sub2 && <span className="text-2xl font-bold opacity-50 lowercase">{sub2}</span>}
       </div>
    </div>
  );
}

function ResponderMini({ init, name, role, status }: any) {
  return (
    <div className="bg-surface-container-high/50 p-5 rounded-[32px] flex items-center justify-between border border-secondary/5 hover:bg-surface-container-high transition-all">
       <div className="flex items-center gap-4">
          <div className="w-12 h-12 bg-secondary-container text-on-secondary-container rounded-2xl flex items-center justify-center font-black text-sm shadow-sm">{init}</div>
          <div>
            <div className="text-sm font-black text-on-surface">{name}</div>
            <div className="text-[10px] font-bold text-on-surface-variant uppercase tracking-tighter">{role}</div>
          </div>
       </div>
       <span className="text-[9px] font-black px-4 py-2 bg-primary/10 text-primary rounded-full uppercase tracking-widest">{status}</span>
    </div>
  );
}

function HistoryItem({ title, time, location }: any) {
  return (
    <div className="relative pl-8">
       <div className="absolute -left-[7px] top-1 w-3 h-3 rounded-full bg-secondary ring-4 ring-surface" />
       <div className="flex justify-between items-center mb-1">
          <span className="text-xs font-black uppercase text-on-surface tracking-tight">{title}</span>
          <span className="text-[10px] font-bold opacity-40 uppercase tracking-widest">{time}</span>
       </div>
       <p className="text-[10px] font-bold text-on-surface-variant uppercase tracking-widest flex items-center gap-2">
          <MapPin className="w-3 h-3" />
          {location}
       </p>
    </div>
  );
}
