import React from 'react';
import { motion } from 'motion/react';
import { 
  ArrowLeft, Clock, MapPin, Users, FireExtinguisher, BadgeAlert, 
  MessageSquare, ShieldAlert, CheckCircle2, MoreVertical, 
  Fullscreen, MonitorPlay, Send, History, Phone,
  Activity, Siren, HelpCircle, Megaphone, Shield, HeartPulse
} from 'lucide-react';
import { cn } from '../lib/utils';

export default function ActiveIncidentDetail({ onBack }: { onBack?: () => void }) {
  return (
    <div className="space-y-6 font-sans pb-12">
      {/* Contextual Header */}
      <div className="flex items-center justify-between pb-2 px-1">
        <div className="flex items-center gap-4">
          <button 
            onClick={onBack}
            className="flex items-center gap-2 text-on-surface-variant hover:text-on-surface py-1.5 px-2 rounded-xl transition-all font-semibold text-[14px]"
          >
            <ArrowLeft className="w-4 h-4" />
            Active Incidents
          </button>
          <div className="h-4 w-[1px] bg-secondary/20" />
          <span className="font-medium text-[14px] text-on-surface-variant">Incident ID: #INC-2023-8842</span>
        </div>
        <div className="flex items-center gap-2 text-on-surface font-semibold text-[14px]">
          <Clock className="w-4 h-4 text-on-surface-variant" />
          14:42:05 Local Time
        </div>
      </div>

      {/* Hero Header Card */}
      <section className="bg-surface-container-low rounded-[28px] relative overflow-hidden">
        <div className="absolute top-0 left-6 right-6 h-1.5 bg-error rounded-b-md" />
        <div className="p-8 pt-10">
          <div className="flex flex-col lg:flex-row lg:items-start justify-between gap-8">
            <div className="space-y-4">
              <div className="flex items-center gap-3">
                <div className="bg-error text-on-error px-3 py-1.5 rounded-full font-bold text-[11px] tracking-widest flex items-center gap-1.5 uppercase">
                  <ShieldAlert className="w-3.5 h-3.5 fill-current" />
                  P1 Severity
                </div>
                <div className="flex items-center gap-2 bg-white/20 text-error px-3 py-1.5 rounded-full font-bold text-[11px] tracking-widest uppercase">
                  <div className="relative flex h-2 w-2">
                    <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-error opacity-75" />
                    <span className="relative inline-flex rounded-full h-2 w-2 bg-error" />
                  </div>
                  Active
                </div>
              </div>
              <h1 className="text-[32px] font-bold tracking-tight text-on-surface uppercase leading-none">Fire - Floor 3, Wing B</h1>
              <p className="font-medium text-[15px] text-on-surface-variant flex items-center gap-2">
                <MapPin className="w-4 h-4" />
                Main Property, North Tower, Zone 4
              </p>
            </div>

            <div className="flex items-center gap-3">
              <ActionButton icon={MessageSquare} label="Log Update" />
              <ActionButton icon={ShieldAlert} label="Escalate" isWarning />
              <button className="bg-[#4a4458] text-white font-semibold text-[14px] px-6 py-2.5 rounded-full flex items-center gap-2 hover:bg-[#322f3b] transition-colors">
                <CheckCircle2 className="w-5 h-5" />
                Resolve Incident
              </button>
            </div>
          </div>

          <div className="flex gap-4 mt-8 overflow-x-auto pb-2 no-scrollbar">
             <BentoStat label="Elapsed Time" value="00:14:32" />
             <BentoStat label="Responders" value="8" badge="On-Scene" badgeColor="bg-[#e8def8] text-[#21005d]" />
             <BentoStat label="Guests" value="12" isError badge="Unaccounted" badgeColor="bg-[#f9dedc] text-[#410e0b]" />
             <BentoStat label="Services Notified" custom={
               <div className="flex items-center gap-2 mt-2">
                 <FireExtinguisher className="w-[18px] h-[18px] text-error" />
                 <Shield className="w-[18px] h-[18px] text-[#21005d] opacity-60" />
                 <HeartPulse className="w-[18px] h-[18px] text-on-surface-variant opacity-40" />
               </div>
             } />
             <BentoStat label="SOP Progress" custom={
                <div className="space-y-2 mt-3 w-[150px]">
                  <div className="flex justify-between items-center text-[12px] font-bold">
                    <span className="text-on-surface-variant text-[11px] font-medium">SOP Progress</span>
                    <span className="text-on-surface">45%</span>
                  </div>
                  <div className="w-full h-1.5 bg-surface-container-high rounded-full overflow-hidden">
                    <div className="h-full bg-[#4a4458] rounded-full transition-all duration-1000" style={{ width: '45%' }} />
                  </div>
                </div>
             } hideLabel />
          </div>
        </div>
      </section>

      {/* Main Grid Content */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column */}
        <div className="lg:col-span-7 flex flex-col gap-6">
          {/* Live Tactical Map */}
          <section className="bg-surface-container-low rounded-[28px] overflow-hidden flex flex-col h-[450px]">
            <div className="p-6 flex justify-between items-center relative z-10">
              <h2 className="text-[18px] font-bold text-on-surface flex items-center gap-3">
                <MapPin className="w-6 h-6 text-[#21005d]" />
                Live Tactical Map
              </h2>
              <div className="flex items-center gap-4">
                <span className="text-[12px] font-bold bg-white text-on-surface px-3 py-1.5 rounded-full uppercase tracking-widest">Floor 3</span>
                <button className="text-on-surface-variant hover:text-on-surface transition-colors p-1">
                  <Fullscreen className="w-5 h-5" />
                </button>
              </div>
            </div>
            <div className="relative flex-1 bg-white overflow-hidden rounded-[20px] mx-6 mb-6">
               <img 
                 src="https://images.unsplash.com/photo-1542661062-843818e98031?auto=format&fit=crop&q=80&w=2000" 
                 className="absolute inset-0 w-full h-full object-cover opacity-60 mix-blend-multiply opacity-20 filter grayscale contrast-150 scale-150"
                 alt="Floor Plan"
               />
               <div className="absolute inset-0 p-8">
                 {/* Incident Hotspot */}
                 <div className="absolute top-[40%] left-[30%]">
                    <motion.div 
                      animate={{ scale: [1, 1.2, 1] }} 
                      transition={{ repeat: Infinity, duration: 2 }}
                    >
                      <div className="w-10 h-10 rounded-full bg-error/20 flex items-center justify-center border border-error/40 backdrop-blur-sm">
                        <FireExtinguisher className="w-5 h-5 text-error fill-current" />
                      </div>
                    </motion.div>
                 </div>
                 {/* Responders */}
                 <div className="absolute top-[45%] left-[45%] bg-[#4a4458] text-white h-7 w-7 rounded-full flex items-center justify-center text-[10px] font-black shadow-xl ring-2 ring-white">R1</div>
                 <div className="absolute top-[35%] left-[25%] bg-[#4a4458] text-white h-7 w-7 rounded-full flex items-center justify-center text-[10px] font-black shadow-xl ring-2 ring-white">R2</div>
                 {/* Sweep Zone */}
                 <div className="absolute top-[55%] right-[20%] w-40 h-40 border-2 border-dashed border-[#21005d]/40 bg-white/50 rounded-[20px] flex items-center justify-center backdrop-blur-sm">
                    <span className="text-[10px] font-bold text-on-surface tracking-widest bg-white px-3 py-1.5 rounded-full uppercase shadow-sm">Zone B - Sweep Req.</span>
                 </div>
               </div>
            </div>
          </section>

          {/* Responder Assignments */}
          <section className="bg-surface-container-low rounded-[28px] p-6">
             <h2 className="text-[18px] font-bold text-on-surface mb-6 flex items-center gap-3">
                <Users className="w-6 h-6 text-[#21005d]" />
                Responder Assignments
             </h2>
             <div className="space-y-1 bg-white rounded-[20px] p-4">
               <TableHead items={['Personnel', 'Status', 'ETA', 'Action']} cols="grid-cols-[5fr_3fr_2fr_1fr]" />
               <ResponderRow name="Cmdr. Sarah Jenkins" role="Incident Commander" status="On Scene" eta="-" active />
               <ResponderRow name="Team Alpha" role="Fire Suppression" status="En Route" eta="2 min" />
             </div>
          </section>

          {/* Guest Accountability */}
          <section className="bg-surface-container-low rounded-[28px] p-6">
             <div className="flex justify-between items-center mb-6">
                <h2 className="text-[18px] font-bold text-on-surface flex items-center gap-3">
                  <BadgeAlert className="w-6 h-6 text-[#21005d]" />
                  Guest Accountability
                </h2>
                <span className="text-[11px] font-bold text-error bg-[#f9dedc] px-3 py-1.5 rounded-full uppercase tracking-widest">12 Unaccounted</span>
             </div>
             <div className="space-y-1 bg-white rounded-[20px] p-4">
               <TableHead items={['Room', 'Guest Name', 'Status', 'Actions']} cols="grid-cols-[2fr_5fr_3fr_2fr]" />
               <GuestRow room="312" name="Robert & Mary Higgins" status="Unknown" isError />
               <GuestRow room="314" name="David Chen" status="Evacuated" isSuccess />
             </div>
          </section>
        </div>

        {/* Right Column */}
        <div className="lg:col-span-5 flex flex-col gap-6">
          {/* External Services */}
          <section className="bg-surface-container-low rounded-[28px] p-6">
            <h2 className="text-[18px] font-bold text-on-surface mb-6 flex items-center gap-3">
               <ShieldAlert className="w-6 h-6 text-[#21005d]" />
               External Services
            </h2>
            <div className="space-y-3">
               <ServiceItem icon={FireExtinguisher} label="Fire Department" status="On Scene" color="border-error" iconColor="text-error" badgeColor="bg-[#f9dedc] text-[#410e0b]" />
               <ServiceItem icon={Shield} label="Police" status="En Route (5m)" color="border-[#21005d]" iconColor="text-on-surface" badgeColor="bg-[#e6e0e9] text-on-surface-variant" />
               <ServiceItem icon={HeartPulse} label="Medical" status="Standby" color="border-transparent" iconColor="text-on-surface-variant" badgeColor="bg-[#dad8dc] text-on-surface-variant" />
            </div>
          </section>

          {/* Broadcast Communication */}
          <section className="bg-surface-container-low rounded-[28px] p-6 flex flex-col h-[400px]">
            <h2 className="text-[18px] font-bold text-on-surface mb-6 flex items-center gap-3">
               <Megaphone className="w-6 h-6 text-[#21005d]" />
               Broadcast Communication
            </h2>
            <div className="bg-white rounded-[24px] p-6 flex flex-col gap-6 flex-1 shadow-sm">
               <div className="space-y-3">
                 <p className="text-[11px] font-medium text-on-surface-variant uppercase tracking-widest">Audience</p>
                 <div className="flex gap-2">
                   {['All Guests', 'Affected Floor', 'Specific Room'].map(a => (
                     <button key={a} className={cn(
                       "px-4 py-2 rounded-full text-[12px] font-semibold transition-all border",
                       a === 'Affected Floor' ? "bg-[#e8def8] text-[#21005d] border-transparent" : "bg-transparent text-on-surface-variant border-secondary/20 hover:border-[#21005d]/40"
                     )}>{a}</button>
                   ))}
                 </div>
               </div>

               <div className="flex-1 flex flex-col space-y-2">
                  <div className="flex justify-between items-center">
                    <p className="text-[11px] font-medium text-on-surface-variant uppercase tracking-widest">Message</p>
                    <button className="text-[11px] font-bold text-[#21005d] hover:underline underline-offset-4">Use Template</button>
                  </div>
                  <textarea 
                    className="flex-1 w-full bg-[#f5f3f7] border-none rounded-[16px] p-4 text-[14px] font-medium text-on-surface resize-none focus:outline-none focus:bg-[#e6e0e9] transition-colors placeholder:text-on-surface-variant/40" 
                    placeholder="Type emergency broadcast message..."
                  />
               </div>

               <div className="flex justify-between items-center pt-2">
                  <div className="flex items-center gap-4">
                    <Checkbox label="App Push" defaultChecked />
                    <Checkbox label="WhatsApp" />
                  </div>
                  <button className="bg-[#4a4458] text-white px-5 py-2.5 rounded-full text-[13px] font-semibold flex items-center gap-2 hover:bg-[#322f3b] transition-colors">
                    Send Broadcast
                    <Send className="w-4 h-4" />
                  </button>
               </div>
            </div>
          </section>

          {/* Timeline */}
          <section className="bg-surface-container-low rounded-[28px] p-6 flex-1">
             <h2 className="text-[18px] font-bold text-on-surface mb-8 flex items-center gap-3">
                <History className="w-6 h-6 text-[#21005d]" />
                Live Timeline
             </h2>
             <div className="relative border-l-2 border-[#e6e0e9] ml-4 space-y-8 pb-4">
                <TimelineItem time="14:40:12" text="Cmdr. Jenkins assumed Incident Command" icon={CheckCircle2} color="primary" />
                <TimelineItem time="14:35:00" text="Fire Alarm Triggered (Zone 4)" sub="Smoke detected in Corridor B. Auto-dispatch initiated." icon={FireExtinguisher} color="error" />
                <TimelineItem time="14:32:15" text="Guest report: Burning smell" icon={Clock} color="on-surface-variant" />
             </div>
          </section>
        </div>
      </div>
    </div>
  );
}

function ActionButton({ icon: Icon, label, isWarning }: any) {
  return (
    <button className={cn(
      "px-5 py-2.5 rounded-full font-semibold text-[14px] flex items-center gap-2 transition-colors shadow-sm",
      isWarning ? "bg-[#f9dedc] text-[#410e0b] hover:bg-[#f2b8b5]" : "bg-white text-on-surface hover:bg-[#e6e0e9]"
    )}>
      <Icon className="w-4.5 h-4.5" />
      {label}
    </button>
  );
}

function BentoStat({ label, value, badge, badgeColor, isError, custom, hideLabel }: any) {
  return (
    <div className="bg-white p-5 rounded-[20px] flex flex-col gap-1.5 min-w-[140px] flex-1 shadow-sm">
       {!hideLabel && <span className="text-[11px] font-medium text-on-surface-variant">{label}</span>}
       {custom ? custom : (
         <div className="flex items-center gap-3 mt-1">
            <span className={cn("text-[28px] font-bold font-sans leading-none", isError ? "text-error" : "text-on-surface")}>{value}</span>
            {badge && <span className={cn("text-[10px] font-bold px-2.5 py-1 rounded-full uppercase tracking-wide", badgeColor)}>{badge}</span>}
         </div>
       )}
    </div>
  );
}

function TableHead({ items, cols }: any) {
  return (
    <div className={cn("grid gap-4 px-4 py-3 text-[11px] font-medium text-on-surface-variant border-b border-[#e6e0e9]", cols)}>
      {items.map(it => <div key={it}>{it}</div>)}
    </div>
  );
}

function ResponderRow({ name, role, status, eta, active }: any) {
  return (
    <div className="grid grid-cols-[5fr_3fr_2fr_1fr] gap-4 px-4 py-4 items-center hover:bg-[#f5f3f7] rounded-2xl transition-all cursor-pointer group">
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-full bg-[#f5f3f7] flex items-center justify-center">
           <Users className="w-5 h-5 text-on-surface-variant" />
        </div>
        <div>
          <p className="text-[14px] font-bold text-on-surface leading-none">{name}</p>
          <p className="text-[12px] font-medium text-on-surface-variant mt-1.5">{role}</p>
        </div>
      </div>
      <div>
        <span className={cn(
          "px-3 py-1 rounded-full text-[11px] font-bold",
          active ? "bg-[#e8def8] text-[#21005d]" : "bg-[#e6e0e9] text-on-surface-variant"
        )}>{status}</span>
      </div>
      <div className="text-[14px] font-bold text-on-surface">{eta}</div>
      <div className="flex justify-end pr-2">
         <MoreVertical className="w-5 h-5 text-on-surface-variant opacity-0 group-hover:opacity-100 transition-opacity" />
      </div>
    </div>
  );
}

function GuestRow({ room, name, status, isError, isSuccess }: any) {
  return (
    <div className="grid grid-cols-[2fr_5fr_3fr_2fr] gap-4 px-4 py-4 items-center hover:bg-[#f5f3f7] rounded-2xl transition-all cursor-pointer group">
      <div className="text-[14px] font-bold text-on-surface">{room}</div>
      <div className="text-[14px] font-bold text-on-surface">{name}</div>
      <div>
        <div className={cn(
          "flex items-center gap-2 text-[12px] font-bold",
          isError ? "text-error" : isSuccess ? "text-[#21005d]" : "text-on-surface-variant"
        )}>
          {isError ? <HelpCircle className="w-4 h-4 fill-error text-white" /> : <CheckCircle2 className="w-4 h-4 fill-[#21005d] text-white" />}
          {status}
        </div>
      </div>
      <div className="flex justify-end gap-3 pr-2 opacity-0 group-hover:opacity-100 transition-opacity">
         <button className="p-1 hover:text-[#21005d] transition-colors"><Phone className="w-4 h-4" /></button>
         <button className="p-1 hover:text-[#21005d] transition-colors"><CheckCircle2 className="w-4 h-4" /></button>
      </div>
    </div>
  );
}

function ServiceItem({ icon: Icon, label, status, color, iconColor, badgeColor }: any) {
  return (
    <div className={cn("p-4 bg-white flex justify-between items-center rounded-[20px] border-l-[6px] shadow-sm", color)}>
       <div className="flex items-center gap-4">
          <div className="w-10 h-10 rounded-full flex items-center justify-center bg-[#f5f3f7]">
             <Icon className={cn("w-5 h-5", iconColor)} />
          </div>
          <span className="text-[15px] font-semibold text-on-surface">{label}</span>
       </div>
       <span className={cn("px-3 py-1.5 rounded-full text-[11px] font-bold", badgeColor)}>{status}</span>
    </div>
  );
}

function Checkbox({ label, defaultChecked }: any) {
  return (
    <label className="flex items-center gap-2 cursor-pointer group">
       <div className={cn(
         "w-[18px] h-[18px] rounded-[4px] flex items-center justify-center transition-all",
         defaultChecked ? "bg-[#21005d] text-white" : "border-2 border-on-surface-variant group-hover:border-[#21005d]"
       )}>
         {defaultChecked && <CheckCircle2 className="w-3.5 h-3.5" />}
       </div>
       <span className="text-[13px] font-medium text-on-surface">{label}</span>
    </label>
  );
}

function TimelineItem({ time, text, sub, icon: Icon, color }: any) {
  return (
     <div className="relative pl-8">
        <div className={cn(
          "absolute -left-[11px] top-0.5 w-[22px] h-[22px] rounded-full bg-white border-[3px] flex items-center justify-center z-10",
          color === 'error' ? 'border-error' : color === 'primary' ? 'border-[#21005d]' : 'border-[#e6e0e9]'
        )}>
          {color === 'primary' ? (
             <div className="w-2.5 h-2.5 rounded-full bg-[#21005d]" />
          ) : color === 'error' ? (
             <div className="w-2.5 h-2.5 rounded-full bg-error" />
          ) : null}
        </div>
        <div className="flex flex-col gap-1">
           <span className="text-[12px] font-medium text-on-surface-variant">{time}</span>
           <h4 className="text-[14px] font-semibold text-on-surface leading-tight mt-1">{text}</h4>
           {sub && <p className="text-[13px] font-medium text-on-surface-variant mt-2 bg-white px-4 py-3 rounded-[16px] shadow-sm">{sub}</p>}
        </div>
     </div>
  );
}
