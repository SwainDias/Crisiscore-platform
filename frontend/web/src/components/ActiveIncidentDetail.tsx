import React from 'react';
import { motion } from 'motion/react';
import { 
  ArrowLeft, Clock, MapPin, Users, FireExtinguisher, BadgeAlert, 
  MessageSquare, ShieldAlert, CheckCircle2, MoreVertical, 
  Fullscreen, MonitorPlay, Send, History, Phone,
  Activity, Siren, HelpCircle, Megaphone
} from 'lucide-react';
import { cn } from '../lib/utils';

export default function ActiveIncidentDetail({ onBack }: { onBack?: () => void }) {
  return (
    <div className="space-y-6">
      {/* Contextual Header */}
      <div className="flex items-center justify-between pb-4 border-b border-secondary/5">
        <div className="flex items-center gap-4">
          <button 
            onClick={onBack}
            className="flex items-center gap-2 text-on-surface-variant hover:text-on-surface hover:bg-surface-container py-1.5 px-3 rounded-xl transition-all font-bold text-sm tracking-tight"
          >
            <ArrowLeft className="w-4 h-4" />
            Active Incidents
          </button>
          <div className="h-4 w-[1px] bg-secondary/10" />
          <span className="font-bold text-sm text-on-surface-variant tracking-tight uppercase">Incident ID: #INC-2023-8842</span>
        </div>
        <div className="flex items-center gap-2 text-on-surface font-bold text-sm">
          <Clock className="w-4 h-4 text-on-surface-variant" />
          14:42:05 Local Time
        </div>
      </div>

      {/* Hero Header Card */}
      <section className="bg-surface-container-lowest rounded-3xl relative shadow-sm overflow-hidden border border-secondary/5">
        <div className="absolute top-0 left-0 right-0 h-1.5 bg-error" />
        <div className="p-8">
          <div className="flex flex-col lg:flex-row lg:items-start justify-between gap-8">
            <div className="space-y-3">
              <div className="flex items-center gap-3">
                <div className="bg-error text-on-error px-2.5 py-1 rounded-lg font-bold text-[10px] tracking-widest flex items-center gap-1.5 uppercase">
                  <ShieldAlert className="w-3.5 h-3.5 fill-current" />
                  P1 Severity
                </div>
                <div className="flex items-center gap-2 bg-error/10 text-error px-2.5 py-1 rounded-lg font-bold text-[10px] tracking-widest uppercase">
                  <div className="relative flex h-2 w-2">
                    <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-error opacity-75" />
                    <span className="relative inline-flex rounded-full h-2 w-2 bg-error" />
                  </div>
                  Active
                </div>
              </div>
              <h1 className="font-sans text-4xl font-extrabold tracking-tight text-on-surface uppercase">Fire - Floor 3, Wing B</h1>
              <p className="font-medium text-sm text-on-surface-variant flex items-center gap-2">
                <MapPin className="w-4 h-4" />
                Main Property, North Tower, Zone 4
              </p>
            </div>

            <div className="flex items-center gap-3">
              <ActionButton icon={MessageSquare} label="Log Update" />
              <ActionButton icon={ShieldAlert} label="Escalate" isWarning />
              <button className="bg-gradient-to-br from-primary to-primary-container text-on-primary font-bold text-sm px-6 py-3 rounded-2xl flex items-center gap-2 shadow-lg hover:shadow-primary/20 transition-all active:scale-95">
                <CheckCircle2 className="w-5 h-5" />
                Resolve Incident
              </button>
            </div>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mt-10">
             <BentoStat label="Elapsed Time" value="00:14:32" />
             <BentoStat label="Responders" value="8" badge="On-Scene" badgeColor="bg-secondary-container text-on-secondary-container" />
             <BentoStat label="Guests" value="12" isError badge="Unaccounted" badgeColor="bg-error/10 text-error" />
             <BentoStat label="Services Notified" custom={
               <div className="flex items-center gap-2 mt-1">
                 <FireExtinguisher className="w-5 h-5 text-error" />
                 <BadgeAlert className="w-5 h-5 text-secondary opacity-40" />
                 <Activity className="w-5 h-5 text-on-surface-variant opacity-40" />
               </div>
             } />
             <BentoStat label="SOP Progress" custom={
                <div className="space-y-2 mt-2 w-full">
                  <div className="flex justify-between items-center text-[10px] font-bold">
                    <span className="text-on-surface">45%</span>
                  </div>
                  <div className="w-full h-1.5 bg-surface-container-high rounded-full overflow-hidden">
                    <div className="h-full bg-primary rounded-full transition-all duration-1000" style={{ width: '45%' }} />
                  </div>
                </div>
             } />
          </div>
        </div>
      </section>

      {/* Main Grid Content */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column */}
        <div className="lg:col-span-7 flex flex-col gap-6">
          {/* Live Tactical Map */}
          <section className="bg-surface-container-lowest rounded-3xl shadow-sm overflow-hidden flex flex-col border border-secondary/5 h-[450px]">
            <div className="p-5 flex justify-between items-center border-b border-secondary/5 relative z-10 glass">
              <h2 className="text-base font-bold text-on-surface flex items-center gap-2">
                <MapPin className="w-5 h-5 text-primary" />
                Live Tactical Map
              </h2>
              <div className="flex items-center gap-2">
                <span className="text-[10px] font-bold bg-surface-container-high text-on-surface px-2.5 py-1 rounded-lg uppercase tracking-widest">Floor 3</span>
                <button className="text-on-surface-variant hover:text-on-surface transition-all p-1">
                  <Fullscreen className="w-4 h-4" />
                </button>
              </div>
            </div>
            <div className="relative flex-1 bg-surface-container-low overflow-hidden">
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
                 <div className="absolute top-[45%] left-[45%] bg-secondary text-on-secondary h-7 w-7 rounded-lg flex items-center justify-center text-[10px] font-black shadow-xl ring-2 ring-white">R1</div>
                 <div className="absolute top-[35%] left-[25%] bg-secondary text-on-secondary h-7 w-7 rounded-lg flex items-center justify-center text-[10px] font-black shadow-xl ring-2 ring-white">R2</div>
                 {/* Sweep Zone */}
                 <div className="absolute top-[55%] right-[20%] w-40 h-40 border-2 border-dashed border-primary/40 bg-primary/5 rounded-2xl flex items-center justify-center">
                    <span className="text-[10px] font-bold text-primary tracking-widest bg-surface-container-lowest/80 px-3 py-1.5 rounded-lg backdrop-blur uppercase">Zone B - Sweep Req.</span>
                 </div>
               </div>
            </div>
          </section>

          {/* Responder Assignments */}
          <section className="bg-surface-container-lowest rounded-3xl shadow-sm p-6 border border-secondary/5">
             <h2 className="text-base font-bold text-on-surface mb-6 flex items-center gap-2">
                <Users className="w-5 h-5 text-primary" />
                Responder Assignments
             </h2>
             <div className="space-y-1">
               <TableHead items={['Personnel', 'Status', 'ETA', 'Action']} cols="grid-cols-[5fr_3fr_2fr_1fr]" />
               <ResponderRow name="Cmdr. Sarah Jenkins" role="Incident Commander" status="On Scene" eta="-" active />
               <ResponderRow name="Team Alpha" role="Fire Suppression" status="En Route" eta="2 min" />
             </div>
          </section>

          {/* Guest Accountability */}
          <section className="bg-surface-container-lowest rounded-3xl shadow-sm p-6 border border-secondary/5">
             <div className="flex justify-between items-center mb-6">
                <h2 className="text-base font-bold text-on-surface flex items-center gap-2">
                  <BadgeAlert className="w-5 h-5 text-primary" />
                  Guest Accountability
                </h2>
                <span className="text-[10px] font-bold text-error bg-error/10 px-3 py-1 rounded-full uppercase tracking-widest">12 Unaccounted</span>
             </div>
             <div className="space-y-1">
               <TableHead items={['Room', 'Guest Name', 'Status', 'Actions']} cols="grid-cols-[2fr_5fr_3fr_2fr]" />
               <GuestRow room="312" name="Robert & Mary Higgins" status="Unknown" isError />
               <GuestRow room="314" name="David Chen" status="Evacuated" isSuccess />
             </div>
          </section>
        </div>

        {/* Right Column */}
        <div className="lg:col-span-5 flex flex-col gap-6">
          {/* External Services */}
          <section className="bg-surface-container-lowest rounded-3xl shadow-sm p-6 border border-secondary/5">
            <h2 className="text-base font-bold text-on-surface mb-6 flex items-center gap-2">
               <ShieldAlert className="w-5 h-5 text-primary" />
               External Services
            </h2>
            <div className="space-y-3">
               <ServiceItem icon={FireExtinguisher} label="Fire Department" status="On Scene" color="border-error" iconColor="text-error" badgeColor="bg-error/10 text-error" />
               <ServiceItem icon={Police} label="Police" status="En Route (5m)" color="border-secondary" iconColor="text-secondary" badgeColor="bg-secondary/10 text-secondary" />
               <ServiceItem icon={MedicalServices} label="Medical" status="Standby" color="border-on-surface-variant/30" iconColor="text-on-surface-variant" badgeColor="bg-surface-container text-on-surface-variant opacity-60" />
            </div>
          </section>

          {/* Broadcast Communication */}
          <section className="bg-surface-container-lowest rounded-3xl shadow-sm p-6 flex flex-col h-[400px] border border-secondary/5">
            <h2 className="text-base font-bold text-on-surface mb-6 flex items-center gap-2">
               <Megaphone className="w-5 h-5 text-primary" />
               Broadcast Communication
            </h2>
            <div className="bg-surface-container-low rounded-2xl p-6 flex flex-col gap-6 flex-1 shadow-inner">
               <div className="space-y-3">
                 <p className="text-[10px] font-bold text-on-surface-variant uppercase tracking-widest">Audience</p>
                 <div className="flex gap-2">
                   {['All Guests', 'Affected Floor', 'Specific Room'].map(a => (
                     <button key={a} className={cn(
                       "px-4 py-2 rounded-xl text-[11px] font-bold transition-all border",
                       a === 'Affected Floor' ? "bg-primary/10 text-primary border-primary" : "bg-white text-on-surface-variant border-secondary/10 hover:border-primary/40"
                     )}>{a}</button>
                   ))}
                 </div>
               </div>

               <div className="flex-1 flex flex-col space-y-2">
                  <div className="flex justify-between items-center">
                    <p className="text-[10px] font-bold text-on-surface-variant uppercase tracking-widest">Message</p>
                    <button className="text-[10px] font-bold text-primary hover:underline underline-offset-4">USE TEMPLATE</button>
                  </div>
                  <textarea 
                    className="flex-1 w-full bg-white border border-secondary/5 focus:ring-2 focus:ring-primary/20 rounded-2xl p-4 text-sm font-medium text-on-surface resize-none focus:outline-none placeholder:text-on-surface-variant/40" 
                    placeholder="Type emergency broadcast message..."
                  />
               </div>

               <div className="flex justify-between items-center pt-2 border-t border-secondary/5">
                  <div className="flex items-center gap-4">
                    <Checkbox label="App Push" defaultChecked />
                    <Checkbox label="WhatsApp" />
                  </div>
                  <button className="signature-gradient text-on-primary px-5 py-2.5 rounded-xl text-xs font-bold shadow-lg flex items-center gap-2 active:scale-95 transition-all">
                    Send Broadcast
                    <Send className="w-4 h-4" />
                  </button>
               </div>
            </div>
          </section>

          {/* Timeline */}
          <section className="bg-surface-container-lowest rounded-3xl shadow-sm p-6 border border-secondary/5 flex-1">
             <h2 className="text-base font-bold text-on-surface mb-8 flex items-center gap-2">
                <History className="w-5 h-5 text-primary" />
                Live Timeline
             </h2>
             <div className="relative border-l-2 border-secondary/5 ml-4 space-y-8 pb-4">
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
      "px-5 py-3 rounded-2xl font-bold text-sm tracking-tight flex items-center gap-2 transition-all active:scale-95",
      isWarning ? "bg-surface-container-high text-error hover:bg-error-container hover:text-on-error-container" : "bg-surface-container-high text-on-surface hover:bg-surface-container-highest"
    )}>
      <Icon className="w-4.5 h-4.5" />
      {label}
    </button>
  );
}

function BentoStat({ label, value, badge, badgeColor, isError, custom }: any) {
  return (
    <div className="bg-surface-container-low/50 p-5 rounded-2xl flex flex-col gap-1.5 border border-secondary/5">
       <span className="text-[10px] font-bold text-on-surface-variant uppercase tracking-widest">{label}</span>
       {custom ? custom : (
         <div className="flex items-center gap-2">
            <span className={cn("text-2xl font-extrabold font-sans", isError ? "text-error" : "text-on-surface")}>{value}</span>
            {badge && <span className={cn("text-[9px] font-black px-2 py-0.5 rounded-full uppercase tracking-tighter", badgeColor)}>{badge}</span>}
         </div>
       )}
    </div>
  );
}

function TableHead({ items, cols }: any) {
  return (
    <div className={cn("grid gap-4 px-4 py-2 text-[10px] font-black text-on-surface-variant uppercase tracking-widest border-b border-secondary/5", cols)}>
      {items.map(it => <div key={it}>{it}</div>)}
    </div>
  );
}

function ResponderRow({ name, role, status, eta, active }: any) {
  return (
    <div className="grid grid-cols-[5fr_3fr_2fr_1fr] gap-4 px-4 py-4 items-center hover:bg-surface-container/50 rounded-2xl transition-all cursor-pointer group">
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-2xl bg-surface-container-high flex items-center justify-center shadow-sm">
           <Users className="w-5 h-5 text-on-surface-variant" />
        </div>
        <div>
          <p className="text-sm font-bold text-on-surface leading-none">{name}</p>
          <p className="text-xs font-medium text-on-surface-variant mt-1.5">{role}</p>
        </div>
      </div>
      <div>
        <span className={cn(
          "px-2.5 py-1 rounded-lg text-[10px] font-black uppercase tracking-widest",
          active ? "bg-secondary/10 text-secondary" : "bg-primary/10 text-primary"
        )}>{status}</span>
      </div>
      <div className="text-sm font-bold text-on-surface">{eta}</div>
      <div className="flex justify-end pr-2">
         <MoreVertical className="w-5 h-5 text-on-surface-variant opacity-0 group-hover:opacity-100 transition-opacity" />
      </div>
    </div>
  );
}

function GuestRow({ room, name, status, isError, isSuccess }: any) {
  return (
    <div className="grid grid-cols-[2fr_5fr_3fr_2fr] gap-4 px-4 py-4 items-center hover:bg-surface-container/50 rounded-2xl transition-all cursor-pointer group">
      <div className="text-sm font-black text-on-surface font-sans">{room}</div>
      <div className="text-sm font-bold text-on-surface">{name}</div>
      <div>
        <div className={cn(
          "flex items-center gap-2 text-xs font-black uppercase tracking-widest",
          isError ? "text-error" : isSuccess ? "text-primary" : "text-on-surface-variant"
        )}>
          {isError ? <HelpCircle className="w-4 h-4" /> : <CheckCircle2 className="w-4 h-4" />}
          {status}
        </div>
      </div>
      <div className="flex justify-end gap-3 pr-2 opacity-0 group-hover:opacity-100 transition-opacity">
         <button className="p-1 hover:text-primary transition-colors"><Phone className="w-4 h-4" /></button>
         <button className="p-1 hover:text-primary transition-colors"><CheckCircle2 className="w-4 h-4" /></button>
      </div>
    </div>
  );
}

function ServiceItem({ icon: Icon, label, status, color, iconColor, badgeColor }: any) {
  return (
    <div className={cn("p-4 bg-surface-container-low flex justify-between items-center rounded-2xl border-l-[6px] shadow-sm", color)}>
       <div className="flex items-center gap-3">
          <div className={cn("w-10 h-10 rounded-full flex items-center justify-center bg-white shadow-sm", iconColor)}>
             <Icon className="w-5 h-5 fill-current opacity-80" />
          </div>
          <span className="text-sm font-bold text-on-surface">{label}</span>
       </div>
       <span className={cn("px-3 py-1.5 rounded-lg text-[10px] font-black uppercase tracking-widest shadow-sm", badgeColor)}>{status}</span>
    </div>
  );
}

function Checkbox({ label, defaultChecked }: any) {
  return (
    <label className="flex items-center gap-2 cursor-pointer group">
       <div className={cn(
         "w-4 h-4 rounded-md border border-secondary/20 flex items-center justify-center transition-all",
         defaultChecked ? "bg-primary border-primary" : "bg-white group-hover:border-primary/40"
       )}>
         {defaultChecked && <CheckCircle2 className="w-3 h-3 text-white" />}
       </div>
       <span className="text-xs font-bold text-on-surface-variant group-hover:text-on-surface">{label}</span>
    </label>
  );
}

function TimelineItem({ time, text, sub, icon: Icon, color }: any) {
  return (
     <div className="relative pl-8">
        <div className={cn(
          "absolute -left-[11px] top-1 w-5 h-5 rounded-full bg-white border-2 flex items-center justify-center z-10 shadow-sm",
          `border-${color}`,
          color === 'error' ? 'border-error' : color === 'primary' ? 'border-primary' : 'border-on-surface-variant'
        )}>
          <div className={cn("w-2 h-2 rounded-full", `bg-${color}`, color === 'error' ? 'bg-error' : color === 'primary' ? 'bg-primary' : 'bg-on-surface-variant')} />
        </div>
        <div className="flex flex-col gap-1">
           <span className="text-[10px] font-black text-on-surface-variant tracking-widest">{time}</span>
           <h4 className="text-sm font-bold text-on-surface leading-tight">{text}</h4>
           {sub && <p className="text-xs font-medium text-on-surface-variant mt-2 bg-surface-container p-3 rounded-2xl border border-secondary/5">{sub}</p>}
        </div>
     </div>
  );
}
