import React, { useState } from 'react';
import { 
  Play, Plus, Calendar, Clock, History, MoreVertical, 
  RotateCcw, Edit3, Archive, CheckSquare, ShieldCheck,
  Flame, HeartPulse, Lock, MapPin, Users, Footprints
} from 'lucide-react';
import { cn } from '../lib/utils';

export default function DrillManagement() {
  const [activeTab, setActiveTab] = useState('Upcoming');

  return (
    <div className="space-y-8">
      {/* Page Header */}
      <div className="flex justify-between items-end">
        <div>
          <h1 className="text-[2.5rem] font-sans font-extrabold tracking-tight text-on-surface leading-none mb-3">Drill Management</h1>
          <p className="text-on-surface-variant text-lg font-medium">Coordinate and evaluate property-wide emergency preparedness.</p>
        </div>
        <button className="signature-gradient text-on-primary px-6 py-3.5 rounded-2xl font-black text-sm uppercase tracking-widest flex items-center gap-2 shadow-xl hover:shadow-primary/30 transition-all active:scale-95">
          <Plus className="w-5 h-5" />
          Schedule New Drill
        </button>
      </div>

      <div className="flex gap-8 h-[calc(100vh-14rem)]">
        {/* Left Drill List */}
        <div className="w-1/3 flex flex-col bg-surface-container-low rounded-[40px] overflow-hidden shadow-xl border border-secondary/5">
          {/* Tabs */}
          <div className="flex px-6 pt-5 gap-8 bg-surface-container-low border-b border-secondary/10 shrink-0">
             {['Upcoming', 'In Progress', 'Completed'].map(t => (
               <button 
                 key={t}
                 onClick={() => setActiveTab(t)}
                 className={cn(
                   "pb-4 text-xs font-black uppercase tracking-widest transition-all",
                   activeTab === t ? "text-primary border-b-2 border-primary" : "text-on-surface-variant opacity-60 hover:opacity-100"
                 )}
               >{t}</button>
             ))}
          </div>

          <div className="flex-1 overflow-y-auto p-4 space-y-4 no-scrollbar">
             <DrillCard 
               type="Fire Evacuation" 
               time="Tomorrow, 10:00" 
               title="Zone C Full Clear" 
               target="Security Alpha, Kitchen Staff, Zone C Floor Wardens" 
               active 
             />
             <DrillCard 
               type="Medical Emergency" 
               time="Oct 24, 14:00" 
               title="Lobby Cardiac Arrest" 
               target="First Responders, Guest Services Desk" 
             />
             <DrillCard 
               type="Lockdown" 
               time="Nov 02, 09:30" 
               title="Active Threat Response" 
               target="All Property Staff, Executive Team" 
             />
             <DrillCard 
               type="Fire Evacuation" 
               time="Nov 15, 11:00" 
               title="Tower B Stairwell Test" 
               target="Tower B Residents, Maintenance" 
             />
          </div>
        </div>

        {/* Right Detail Pane */}
        <div className="w-2/3 bg-surface-container-lowest rounded-[40px] shadow-2xl flex flex-col border border-secondary/5 overflow-hidden">
           <div className="p-10 pb-8 bg-surface-container-low/50 relative overflow-hidden border-b border-secondary/5">
              <div className="flex justify-between items-start relative z-10">
                 <div className="space-y-4">
                    <div className="flex items-center gap-4">
                       <span className="bg-error/10 text-error px-3 py-1 rounded-full text-[10px] font-black uppercase tracking-widest border border-error/20">Fire Evacuation</span>
                       <span className="text-sm font-bold text-on-surface-variant flex items-center gap-2">
                         <Clock className="w-4 h-4" />
                         Scheduled for Tomorrow, 10:00 AM
                       </span>
                    </div>
                    <h2 className="text-4xl font-extrabold text-on-surface tracking-tight leading-none">Zone C Full Clear</h2>
                 </div>
                 <div className="flex gap-3">
                    <ActionButton icon={RotateCcw} label="Repeat" />
                    <ActionButton icon={Edit3} label="Edit" />
                    <ActionButton icon={Archive} label="Archive" />
                 </div>
              </div>
              <div className="absolute top-0 right-0 w-80 h-80 bg-primary/5 rounded-full blur-[100px] -translate-y-1/2 translate-x-1/2" />
           </div>

           <div className="flex-1 overflow-y-auto p-10 space-y-12">
              <section className="space-y-4">
                 <h4 className="text-[10px] font-black uppercase tracking-[0.3em] text-on-surface-variant">Scenario Description</h4>
                 <div className="bg-surface p-6 rounded-3xl border border-secondary/5 leading-relaxed text-on-surface font-medium">
                    Simulated grease fire in the Main Dining Room kitchen during peak prep hours. The objective is to evaluate the speed and efficiency of the kitchen staff's initial suppression attempts, communication protocol with centralized security, and the subsequent directed evacuation of Zone C by designated floor wardens. Special attention should be paid to guest bottlenecking near Exit C-2.
                 </div>
              </section>

              <section className="space-y-6">
                 <h4 className="text-[10px] font-black uppercase tracking-[0.3em] text-on-surface-variant">Targeted Personnel</h4>
                 <div className="flex flex-wrap gap-3">
                    <TargetBadge icon={ShieldCheck} label="Security Team Alpha" color="text-primary" />
                    <TargetBadge icon={HeartPulse} label="Main Kitchen Staff" color="text-error" />
                    <TargetBadge icon={Users} label="Zone C Floor Wardens" color="text-secondary" />
                 </div>
              </section>

              <section className="space-y-6">
                 <div className="flex justify-between items-end">
                    <h4 className="text-[10px] font-black uppercase tracking-[0.3em] text-on-surface-variant">Execution Checklist</h4>
                    <span className="bg-surface-container px-3 py-1 rounded-full text-[10px] font-black text-on-surface-variant tracking-widest border border-secondary/5">0 / 4 STEPS</span>
                 </div>
                 <div className="grid gap-2">
                    <CheckItem title="Initiate Alarm Sequence" sub="Trigger silent alarm to dispatch center, followed immediately by localized audible alarm in Zone C." />
                    <CheckItem title="Warden Radio Check-in" sub="All active Zone C wardens must report via dedicated radio channel within 90 seconds of audible alarm sounding." />
                    <CheckItem title="Kitchen Suppression Simulation" sub="Kitchen manager to verbally confirm location of nearest Class K extinguisher and manual pull station to observer." />
                    <CheckItem title="Final Sweep Report" sub="Log completion time of final room-by-room sweep by designated security personnel and declare 'All Clear'." />
                 </div>
              </section>
           </div>
        </div>
      </div>
    </div>
  );
}

function DrillCard({ type, time, title, target, active }: any) {
  return (
    <div className={cn(
      "p-6 rounded-3xl cursor-pointer transition-all border-l-4 group",
      active 
        ? "bg-surface-container-lowest shadow-xl border-primary" 
        : "hover:bg-surface-container-highest border-transparent"
    )}>
       <div className="flex justify-between items-start mb-4">
          <span className={cn(
            "text-[9px] font-black uppercase tracking-widest px-3 py-1 rounded-full",
            active ? "bg-error/10 text-error" : "bg-surface-container text-on-surface-variant opacity-60"
          )}>{type}</span>
          <span className="text-[11px] font-bold text-on-surface-variant">{time}</span>
       </div>
       <h3 className="text-lg font-extrabold text-on-surface mb-2 group-hover:text-primary transition-colors">{title}</h3>
       <p className="text-xs font-medium text-on-surface-variant leading-relaxed mb-4">{target}</p>
       <div className={cn(
         "flex items-center gap-2 text-[10px] font-black uppercase tracking-widest",
         active ? "text-primary" : "text-on-surface-variant opacity-40"
       )}>
          <Calendar className="w-3.5 h-3.5" />
          Scheduled
       </div>
    </div>
  );
}

function ActionButton({ icon: Icon, label }: any) {
  return (
    <button className="px-5 py-2.5 bg-white text-on-surface border border-secondary/10 rounded-full text-xs font-black shadow-sm hover:bg-surface-container transition-all flex items-center gap-2 uppercase tracking-widest">
      <Icon className="w-4 h-4 text-on-surface-variant" />
      {label}
    </button>
  );
}

function TargetBadge({ icon: Icon, label, color }: any) {
  return (
    <div className="flex items-center gap-3 px-5 py-3 bg-surface-container-low rounded-2xl border border-secondary/5 shadow-sm group hover:scale-105 transition-all">
       <Icon className={cn("w-5 h-5", color)} />
       <span className="text-sm font-black text-on-surface">{label}</span>
    </div>
  );
}

function CheckItem({ title, sub }: any) {
  return (
    <div className="flex items-start gap-5 p-6 bg-surface hover:bg-surface-container transition-all rounded-3xl border border-secondary/5 group cursor-pointer">
       <div className="mt-1">
          <CheckSquare className="w-6 h-6 text-on-surface-variant/20 group-hover:text-primary transition-colors" />
       </div>
       <div className="space-y-1">
          <h5 className="text-base font-black text-on-surface">{title}</h5>
          <p className="text-sm font-medium text-on-surface-variant leading-relaxed">{sub}</p>
       </div>
    </div>
  );
}
