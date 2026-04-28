import React, { useState } from 'react';
import { 
  Play, Plus, Calendar, Clock, History, MoreVertical, 
  RotateCcw, Edit3, Archive, CheckSquare, Shield,
  Flame, HeartPulse, Lock, MapPin, Users, Footprints,
  Utensils, UserPlus, ShieldAlert, Square
} from 'lucide-react';
import { cn } from '../lib/utils';

export default function DrillManagement() {
  const [activeTab, setActiveTab] = useState('Upcoming');

  return (
    <div className="space-y-8 font-sans pb-12">
      {/* Page Header */}
      <div className="flex justify-between items-end mt-4">
        <div>
          <h1 className="text-[36px] font-bold tracking-tight text-on-surface mb-1">Drill Management</h1>
          <p className="text-on-surface-variant text-[15px]">Coordinate and evaluate property-wide emergency preparedness.</p>
        </div>
        <button className="bg-primary text-white px-5 py-2.5 rounded-full font-medium text-[14px] flex items-center gap-2 hover:bg-[#5a4691] transition-colors shadow-sm">
          <Plus className="w-4 h-4" />
          Schedule New Drill
        </button>
      </div>

      <div className="flex gap-6 h-[calc(100vh-14rem)]">
        {/* Left Drill List */}
        <div className="w-[35%] flex flex-col bg-surface-container-low rounded-[28px] overflow-hidden">
          {/* Tabs */}
          <div className="flex px-6 pt-6 gap-6 bg-surface-container-low shrink-0 border-b border-black/5">
             {['Upcoming', 'In Progress', 'Completed'].map(t => (
               <button 
                 key={t}
                 onClick={() => setActiveTab(t)}
                 className={cn(
                   "pb-3 text-[14px] font-semibold transition-all relative",
                   activeTab === t ? "text-on-surface" : "text-on-surface-variant hover:text-on-surface"
                 )}
               >
                 {t}
                 {activeTab === t && (
                   <div className="absolute bottom-0 left-0 right-0 h-[3px] bg-primary rounded-t-full" />
                 )}
               </button>
             ))}
          </div>

          <div className="flex-1 overflow-y-auto p-4 space-y-3 no-scrollbar">
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
        <div className="w-[65%] bg-surface-container-low rounded-[28px] flex flex-col overflow-hidden">
           <div className="p-8 pb-6 bg-surface-container-low relative shrink-0">
              <div className="flex justify-between items-start relative z-10 mb-6">
                 <div className="flex items-center gap-4">
                    <span className="bg-[#f9dedc] text-[#410e0b] px-3 py-1 rounded-full text-[10px] font-bold uppercase tracking-widest">Fire Evacuation</span>
                    <span className="text-[14px] font-bold text-on-surface-variant flex items-center gap-1.5">
                      <Clock className="w-4 h-4" />
                      Scheduled for Tomorrow, 10:00 AM
                    </span>
                 </div>
                 <div className="flex gap-2">
                    <ActionButton icon={RotateCcw} label="Repeat" />
                    <ActionButton icon={Edit3} label="Edit" />
                    <ActionButton icon={Archive} label="Archive" />
                 </div>
              </div>
              <h2 className="text-[32px] font-bold text-on-surface tracking-tight leading-none relative z-10">Zone C Full Clear</h2>
           </div>

           <div className="flex-1 overflow-y-auto px-8 pb-8 space-y-8 no-scrollbar bg-white rounded-[28px] pt-8 m-1 mt-0 shadow-sm">
              <section className="space-y-4">
                 <h4 className="text-[12px] font-bold uppercase tracking-widest text-on-surface-variant">Scenario Description</h4>
                 <div className="leading-[1.6] text-on-surface font-medium text-[15px]">
                    Simulated grease fire in the Main Dining Room kitchen during peak prep hours. The objective is to evaluate the speed and efficiency of the kitchen staff's initial suppression attempts, communication protocol with centralized security, and the subsequent directed evacuation of Zone C by designated floor wardens. Special attention should be paid to guest bottlenecking near Exit C-2.
                 </div>
              </section>

              <section className="space-y-4">
                 <h4 className="text-[12px] font-bold uppercase tracking-widest text-on-surface-variant">Targeted Personnel</h4>
                 <div className="flex flex-wrap gap-3">
                    <TargetBadge icon={Shield} label="Security Team Alpha" />
                    <TargetBadge icon={Utensils} label="Main Kitchen Staff" />
                    <TargetBadge icon={UserPlus} label="Zone C Floor Wardens" />
                 </div>
              </section>

              <section className="space-y-4">
                 <div className="flex justify-between items-end">
                    <h4 className="text-[12px] font-bold uppercase tracking-widest text-on-surface-variant">Execution Checklist</h4>
                    <span className="bg-surface-container-highest px-3 py-1 rounded-full text-[11px] font-bold text-on-surface tracking-wider">0 / 4 Steps</span>
                 </div>
                 <div className="grid gap-3">
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
  const isFire = type === "Fire Evacuation";
  const isLockdown = type === "Lockdown";
  return (
    <div className={cn(
      "p-5 rounded-[20px] cursor-pointer transition-all group",
      active 
        ? "bg-white shadow-sm border-l-[4px] border-primary" 
        : "bg-white hover:bg-surface-container border-l-[4px] border-transparent"
    )}>
       <div className="flex justify-between items-center mb-3">
          <span className={cn(
            "text-[9px] font-bold uppercase tracking-widest px-2.5 py-1 rounded-full",
            isFire ? "bg-[#f9dedc] text-[#410e0b]" : isLockdown ? "bg-primary-container text-on-primary-container" : "bg-surface-container-highest text-on-surface-variant"
          )}>{type}</span>
          <span className="text-[12px] font-bold text-on-surface">{time}</span>
       </div>
       <h3 className="text-[16px] font-bold text-on-surface mb-1 group-hover:text-primary transition-colors">{title}</h3>
       <p className="text-[13px] font-medium text-on-surface-variant leading-relaxed mb-4">{target}</p>
       <div className={cn(
         "flex items-center gap-1.5 text-[12px] font-semibold",
         active ? "text-primary" : "text-on-surface-variant"
       )}>
          <Calendar className="w-4 h-4" />
          Scheduled
       </div>
    </div>
  );
}

function ActionButton({ icon: Icon, label }: any) {
  return (
    <button className="px-4 py-2 bg-surface-container text-on-surface rounded-full text-[13px] font-semibold hover:bg-surface-container-high transition-all flex items-center gap-2">
      <Icon className="w-4 h-4 text-on-surface" />
      {label}
    </button>
  );
}

function TargetBadge({ icon: Icon, label }: any) {
  return (
    <div className="flex items-center gap-2.5 px-4 py-2.5 bg-surface-container rounded-full transition-all cursor-pointer hover:bg-surface-container-high">
       <Icon className="w-4 h-4 text-on-surface" />
       <span className="text-[13px] font-bold text-on-surface">{label}</span>
    </div>
  );
}

function CheckItem({ title, sub }: any) {
  return (
    <div className="flex items-start gap-4 p-5 bg-white hover:bg-surface-container transition-all rounded-[24px] border border-black/5 cursor-pointer">
       <div className="mt-0.5">
          <Square className="w-[22px] h-[22px] text-on-surface-variant/40" strokeWidth={2.5} />
       </div>
       <div className="space-y-1">
          <h5 className="text-[15px] font-bold text-on-surface">{title}</h5>
          <p className="text-[13px] text-on-surface-variant leading-[1.6]">{sub}</p>
       </div>
    </div>
  );
}
