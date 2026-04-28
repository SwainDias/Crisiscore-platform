import React from 'react';
import { 
  Users, Search, Upload, Download, Megaphone, 
  ChevronDown, MessageCircle, MapPin, MoreHorizontal,
  TriangleAlert, Info, UserCircle
} from 'lucide-react';
import { cn } from '../lib/utils';

export default function StaffDirectory() {
  return (
    <div className="space-y-8">
      {/* Alert Banner */}
      <div className="bg-error-container/20 border-l-8 border-error rounded-3xl p-6 flex flex-col md:flex-row items-center gap-6 shadow-xl shadow-error/5 border border-error/10">
        <div className="w-14 h-14 rounded-2xl bg-error flex items-center justify-center shrink-0">
          <TriangleAlert className="w-8 h-8 text-on-error" />
        </div>
        <div className="flex-1 text-left">
          <h3 className="text-xl font-bold text-on-error-container tracking-tight">Unresponsive Staff Alert</h3>
          <p className="text-sm font-semibold text-on-error-container/80 mt-1">3 staff members have missed their routine check-in during the current active scenario. Immediate communication requested.</p>
        </div>
        <button className="px-6 py-2.5 bg-white text-error font-extrabold text-sm rounded-2xl shadow-sm hover:bg-error/5 transition-all border border-error/10 uppercase tracking-widest">
           View Details
        </button>
      </div>

      {/* Page Header */}
      <div className="flex flex-col lg:flex-row lg:items-end justify-between gap-6">
        <div>
          <h2 className="text-4xl font-sans font-extrabold tracking-tight text-on-surface mb-3">Staff Directory</h2>
          <div className="flex flex-wrap gap-2">
            <Badge label="TOTAL: 142" color="bg-surface-container-high text-on-surface-variant border-secondary/10" />
            <Badge label="ON SHIFT: 89" color="bg-primary/10 text-primary border-primary/20" />
            <Badge label="UNRESPONSIVE: 3" color="bg-error/10 text-error border-error/20" />
          </div>
        </div>

        <div className="flex items-center gap-3">
           <HeaderAction icon={Upload} label="Import Staff" />
           <HeaderAction icon={Download} label="Export CSV" />
           <button className="signature-gradient text-on-primary px-6 py-3 rounded-2xl font-extrabold text-sm flex items-center gap-2 shadow-lg hover:shadow-primary/30 transition-all active:scale-95 uppercase tracking-widest">
             <Megaphone className="w-5 h-5 flex-shrink-0" />
             Send Broadcast
           </button>
        </div>
      </div>

      <div className="flex flex-col lg:flex-row gap-8 items-start">
        {/* Filters Sidebar */}
        <aside className="w-full lg:w-72 shrink-0 glass p-8 rounded-3xl space-y-8 border border-secondary/5 sticky top-24 self-start shadow-xl">
           <div className="flex items-center justify-between">
              <h3 className="text-[10px] font-black uppercase tracking-[0.2em] text-on-surface-variant">Filters</h3>
              <button className="text-[10px] font-black uppercase text-primary hover:underline underline-offset-4">Clear All</button>
           </div>

           <FilterSection title="Role">
              <Checkbox label="Security (24)" checked />
              <Checkbox label="Medical (12)" checked />
              <Checkbox label="Maintenance (45)" />
              <Checkbox label="Management (18)" />
           </FilterSection>

           <FilterSection title="Status">
              <Checkbox label="Available" />
              <Checkbox label="Responding" />
              <Checkbox label="Unresponsive" checked color="bg-error border-error" />
           </FilterSection>

           <FilterSection title="Floor">
              <div className="relative group">
                <select className="w-full bg-surface-container-high text-on-surface font-bold text-sm px-4 py-3 rounded-2xl border-none focus:ring-2 focus:ring-primary/20 appearance-none transition-all">
                  <option>All Floors</option>
                  <option>Lobby</option>
                  <option>Floor 1 - 10</option>
                  <option>Roof</option>
                </select>
                <ChevronDown className="absolute right-4 top-1/2 -translate-y-1/2 w-5 h-5 text-on-surface-variant pointer-events-none group-hover:text-on-surface" />
              </div>
           </FilterSection>
        </aside>

        {/* Data Area */}
        <div className="flex-1 bg-surface-container-lowest rounded-3xl shadow-sm overflow-hidden border border-secondary/5">
           {/* Table Header */}
           <div className="grid grid-cols-[3fr_2fr_2fr_2fr_1.5fr_1.5fr_0.5fr] gap-4 px-8 py-5 bg-surface-container-low border-b border-secondary/5 font-black text-[10px] uppercase tracking-[0.2em] text-on-surface-variant">
             <div>Staff Member</div>
             <div>Role / ID</div>
             <div>Assignment</div>
             <div>Last Seen</div>
             <div>Status</div>
             <div>Response</div>
             <div className="text-right">Actions</div>
           </div>

           {/* Table Content */}
           <div className="divide-y divide-secondary/5">
              <StaffRow 
                name="Michael Chen"
                phone="+1 (555) 0192"
                role="Security Officer"
                id="SEC-882"
                assignment="Floor 4, West"
                lastSeen="14:15 (15m ago)"
                location="Stairwell B"
                status="UNRESPONSIVE"
                isUnresponsive
                avatar="https://i.pravatar.cc/150?u=michael"
              />
              <StaffRow 
                name="Sarah Jenkins"
                phone="+1 (555) 0184"
                role="Lead Medic"
                id="MED-042"
                assignment="Lobby Clinic"
                lastSeen="14:28 (2m ago)"
                location="Elevator Bank A"
                status="RESPONDING"
                responseTime="Est. 2 mins"
                color="bg-primary/20 text-primary"
                avatar="https://i.pravatar.cc/150?u=sarah"
              />
              <StaffRow 
                name="David Jones"
                phone="+1 (555) 0211"
                role="Maintenance"
                id="MNT-119"
                assignment="Basement L2"
                lastSeen="14:20 (10m ago)"
                location="Boiler Room"
                status="AVAILABLE"
                avatar="https://i.pravatar.cc/150?u=david"
              />
           </div>
        </div>
      </div>
    </div>
  );
}

function Badge({ label, color }: any) {
  return (
    <span className={cn("px-4 py-1.5 rounded-xl text-[11px] font-extrabold uppercase tracking-widest border shadow-sm", color)}>
      {label}
    </span>
  );
}

function HeaderAction({ icon: Icon, label }: any) {
  return (
    <button className="flex items-center gap-3 px-5 py-3 rounded-2xl bg-surface-container-high text-on-surface hover:bg-surface-container-highest transition-all font-bold text-sm shadow-sm active:scale-95">
      <Icon className="w-5 h-5 text-on-surface-variant" />
      {label}
    </button>
  );
}

function FilterSection({ title, children }: any) {
  return (
    <div className="space-y-4">
       <p className="text-[10px] font-black uppercase tracking-[0.1em] text-on-surface-variant mb-2">{title}</p>
       <div className="flex flex-col gap-3">
         {children}
       </div>
    </div>
  );
}

function Checkbox({ label, checked, color = "bg-primary border-primary" }: any) {
  return (
    <label className="flex items-center gap-4 group cursor-pointer">
       <div className={cn(
         "w-6 h-6 rounded-lg border-2 transition-all flex items-center justify-center",
         checked ? color : "border-secondary/20 bg-white group-hover:border-primary/40"
       )}>
         {checked && <div className="w-2.5 h-2.5 rounded-sm bg-white" />}
       </div>
       <span className={cn("text-sm transition-colors", checked ? "text-on-surface font-black" : "text-on-surface-variant font-bold group-hover:text-on-surface")}>
         {label}
       </span>
    </label>
  );
}

function StaffRow({ name, phone, role, id, assignment, lastSeen, location, status, responseTime, avatar, color, isUnresponsive }: any) {
  return (
    <div className={cn(
      "grid grid-cols-[3fr_2fr_2fr_2fr_1.5fr_1.5fr_0.5fr] gap-4 px-8 py-5 items-center hover:bg-surface-container/30 transition-all cursor-pointer group relative",
      isUnresponsive && "bg-error-container/5"
    )}>
       {isUnresponsive && <div className="absolute left-0 top-0 bottom-0 w-1.5 bg-error" />}
       
       <div className="flex items-center gap-4">
          <div className="w-12 h-12 rounded-2xl bg-surface-container-high overflow-hidden shadow-sm border border-secondary/5 shrink-0">
             <img src={avatar} alt={name} className="w-full h-full object-cover" />
          </div>
          <div>
            <h4 className="text-sm font-extrabold text-on-surface leading-none">{name}</h4>
            <p className="text-xs font-semibold text-on-surface-variant mt-2 tracking-tight">Ph: {phone}</p>
          </div>
       </div>

       <div>
         <p className="text-sm font-bold text-on-surface leading-none">{role}</p>
         <p className="text-[10px] font-black text-on-surface-variant mt-2 uppercase tracking-widest bg-surface-container-high w-fit px-1.5 py-0.5 rounded-lg border border-secondary/5 font-mono">{id}</p>
       </div>

       <div className="text-sm font-bold text-on-surface leading-tight text-left pr-4">
         {assignment}
       </div>

       <div>
          <p className="text-sm font-bold text-on-surface leading-none">{lastSeen}</p>
          <p className="text-[10px] font-black text-on-surface-variant mt-2 uppercase tracking-widest">{location}</p>
       </div>

       <div>
          <span className={cn(
            "px-3 py-1.5 rounded-xl text-[10px] font-black uppercase tracking-widest",
            isUnresponsive ? "bg-error text-on-error shadow-lg shadow-error/10" : (color || "bg-surface-container-highest text-on-surface-variant")
          )}>{status}</span>
       </div>

       <div className="text-sm font-black text-primary italic">
         {responseTime || "--"}
       </div>

       <div className="flex justify-end gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
          <button className="p-2 hover:bg-surface-container rounded-xl text-on-surface-variant hover:text-primary"><MessageCircle className="w-5 h-5" /></button>
          <button className="p-2 hover:bg-surface-container rounded-xl text-on-surface-variant hover:text-primary"><MapPin className="w-5 h-5" /></button>
          <button className="p-2 hover:bg-surface-container rounded-xl text-on-surface-variant hover:text-primary"><MoreHorizontal className="w-5 h-5" /></button>
       </div>
    </div>
  );
}
