import React from 'react';
import { 
  Settings as Cog, Puzzle as Extension, Users, ClipboardList as AssignmentIcon, 
  TriangleAlert, Search, Plus, ExternalLink, ChevronRight, RefreshCcw, 
  Database, ShieldCheck, Network, Key
} from 'lucide-react';
import { cn } from '../lib/utils';

export default function SystemSettings() {
  return (
    <div className="space-y-10">
      {/* Header */}
      <div className="max-w-2xl">
        <h2 className="text-5xl font-sans font-extrabold tracking-tight text-on-surface mb-4">System Settings</h2>
        <p className="text-on-surface-variant text-lg font-medium">Manage integrations, user access, and global protocol configurations.</p>
      </div>

      <div className="grid grid-cols-12 gap-10">
        {/* Sidebar Nav */}
        <aside className="col-span-12 lg:col-span-3 bg-surface-container-low rounded-[32px] p-4 flex flex-col gap-1.5 self-start border border-secondary/5 shadow-xl">
           <SettingsNavItem icon={Cog} label="General" />
           <SettingsNavItem icon={Network} label="Integrations" active />
           <SettingsNavItem icon={Users} label="Users & Roles" />
           <SettingsNavItem icon={AssignmentIcon} label="Incident Protocols" />
           <div className="h-px bg-secondary/5 my-3 mx-4" />
           <SettingsNavItem icon={TriangleAlert} label="Danger Zone" isDanger />
        </aside>

        {/* Content Area */}
        <div className="col-span-12 lg:col-span-9 space-y-10">
           {/* Section Header */}
           <div className="flex items-center justify-between glass rounded-[40px] p-8 border border-secondary/5 shadow-2xl">
              <div>
                <h3 className="text-2xl font-extrabold text-on-surface tracking-tight">Active Integrations</h3>
                <p className="text-on-surface-variant font-medium mt-1">Connect third-party systems for unified command response.</p>
              </div>
              <button className="bg-primary-container text-on-primary-container px-6 py-3 rounded-2xl font-black text-sm uppercase tracking-widest flex items-center gap-2 shadow-lg hover:shadow-primary-container/20 transition-all active:scale-95">
                <Plus className="w-5 h-5" />
                Browse Directory
              </button>
           </div>

           {/* Cards Grid */}
           <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <IntegrationCard 
                name="Salto Access"
                category="Physical Security"
                desc="Syncs live access logs and door statuses to the command map. Enables remote lockdown capabilities during active incidents."
                status="Connected"
                latency="22ms"
                lastSynced="Just now"
                syncType="Real-time (Webhook)"
                nodes="142 Active"
              />
              <IntegrationCard 
                name="Everbridge Mass Notification"
                category="Communication"
                desc="Automates multi-channel emergency broadcasting across push, SMS, and voice. Integrated with P1 alert triggers."
                status="Standby"
                latency="105ms"
                lastSynced="5m ago"
                syncType="Scheduled (5m)"
                nodes="Global"
              />
           </div>
        </div>
      </div>
    </div>
  );
}

function SettingsNavItem({ icon: Icon, label, active, isDanger }: any) {
  return (
    <button className={cn(
      "w-full flex items-center gap-4 px-6 py-4 rounded-[20px] transition-all duration-200 group text-left",
      active 
        ? "bg-secondary-container text-on-secondary-container font-black shadow-lg" 
        : isDanger 
          ? "text-error hover:bg-error/10 font-bold" 
          : "text-on-surface-variant hover:bg-surface-container font-bold"
    )}>
      <Icon className={cn("w-5 h-5", active ? "fill-current" : "group-hover:text-primary")} />
      <span className="text-sm tracking-tight">{label}</span>
    </button>
  );
}

function IntegrationCard({ name, category, desc, status, latency, lastSynced, syncType, nodes }: any) {
  return (
    <div className="bg-surface-container-high/50 rounded-[40px] p-8 space-y-6 border border-secondary/5 hover:bg-surface-container-high transition-all group relative overflow-hidden shadow-sm">
       <div className="flex items-start justify-between relative z-10">
          <div className="flex items-center gap-5">
             <div className="w-16 h-16 bg-surface-container-lowest rounded-3xl flex items-center justify-center p-3 shadow-sm border border-secondary/5">
                <Database className="w-full h-full text-primary" />
             </div>
             <div>
                <h4 className="text-xl font-extrabold text-on-surface leading-tight">{name}</h4>
                <p className="text-sm font-bold text-on-surface-variant mt-1.5 uppercase tracking-widest">{category}</p>
             </div>
          </div>
          <div className={cn(
            "px-4 py-2 rounded-full text-[10px] font-black uppercase tracking-widest flex items-center gap-2",
            status === 'Connected' ? "bg-primary/10 text-primary" : "bg-on-surface-variant/10 text-on-surface-variant"
          )}>
             <div className={cn("w-2 h-2 rounded-full", status === 'Connected' ? "bg-primary animate-pulse" : "bg-on-surface-variant")} />
             {status}
          </div>
       </div>

       <p className="text-base font-medium text-on-surface-variant leading-relaxed">
          {desc}
       </p>

       <div className="bg-surface-container-lowest/50 rounded-3xl p-6 space-y-4 border border-secondary/5">
          <div className="flex justify-between items-center text-[11px] font-black uppercase tracking-[0.2em] text-on-surface">
            <span>API Status</span>
            <span className="bg-surface-container px-2.5 py-1 rounded-lg text-on-surface-variant lowercase tracking-normal">{latency} latency</span>
          </div>
          <div className="space-y-3">
             <DetailItem label="Last Synced" value={lastSynced} />
             <DetailItem label="Sync Schedule" value={syncType} />
             <DetailItem label="Connected Nodes" value={nodes} />
          </div>
       </div>

       <div className="flex items-center justify-between pt-2">
          <div className="flex items-center gap-3 text-xs font-bold text-on-surface-variant">
             <RefreshCcw className="w-4 h-4" />
             Auto-sync active
          </div>
          <button className="text-sm font-black text-primary hover:text-primary-container transition-colors flex items-center gap-1 group/btn px-4 py-2 rounded-full hover:bg-primary/5">
             Configure
             <ChevronRight className="w-5 h-5 group-hover/btn:translate-x-1 transition-transform" />
          </button>
       </div>
       
       <div className="absolute -right-20 -top-20 w-48 h-48 bg-primary/5 rounded-full blur-3xl opacity-0 group-hover:opacity-100 transition-opacity" />
    </div>
  );
}

function DetailItem({ label, value }: any) {
  return (
    <div className="flex justify-between items-center text-sm font-medium">
       <span className="text-on-surface-variant">{label}</span>
       <span className="text-on-surface font-bold">{value}</span>
    </div>
  );
}
