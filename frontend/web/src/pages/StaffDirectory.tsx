import React from 'react';
import { 
  Users, Search, Upload, Download, Megaphone, 
  ChevronDown, MessageCircle, MapPin, MoreHorizontal,
  TriangleAlert, Info, UserCircle, Phone, CheckCircle2
} from 'lucide-react';
import { cn } from '../lib/utils';

export default function StaffDirectory() {
  return (
    <div className="space-y-6 font-sans pb-12">
      {/* Alert Banner */}
      <div className="bg-[#f9dedc] rounded-[28px] p-6 flex flex-col md:flex-row items-center gap-6 shadow-sm border border-[#b3261e]/10">
        <div className="w-14 h-14 rounded-2xl bg-[#b3261e] flex items-center justify-center shrink-0">
          <TriangleAlert className="w-8 h-8 text-white" />
        </div>
        <div className="flex-1 text-left">
          <h3 className="text-[20px] font-bold text-[#410e0b] tracking-tight uppercase">Unresponsive Staff Alert</h3>
          <p className="text-[14px] font-medium text-[#8c1d18] mt-1">3 staff members have missed their routine check-in during the current active scenario. Immediate communication requested.</p>
        </div>
        <button className="px-6 py-2.5 bg-white text-[#b3261e] font-bold text-[13px] rounded-full shadow-sm hover:bg-[#f2b8b5] transition-all uppercase tracking-wider">
           View Details
        </button>
      </div>

      {/* Page Header */}
      <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-6 px-1">
        <div>
          <h2 className="text-[32px] font-bold tracking-tight text-on-surface">Staff Directory</h2>
          <div className="flex flex-wrap gap-2 mt-3">
            <Badge label="TOTAL: 142" color="bg-surface-container-high text-on-surface-variant" />
            <Badge label="ON SHIFT: 89" color="bg-[#e8def8] text-[#21005d]" />
            <Badge label="UNRESPONSIVE: 3" color="bg-[#f9dedc] text-[#b3261e]" />
          </div>
        </div>

        <div className="flex items-center gap-3">
           <HeaderAction icon={Upload} label="Import Staff" />
           <HeaderAction icon={Download} label="Export CSV" />
           <button className="bg-[#4a4458] text-white px-6 py-3 rounded-full font-bold text-[13px] flex items-center gap-2 hover:bg-[#322f3b] transition-all active:scale-95 uppercase tracking-wider">
             <Megaphone className="w-4 h-4" />
             Send Broadcast
           </button>
        </div>
      </div>

      <div className="flex flex-col lg:flex-row gap-6 items-start">
        {/* Filters Sidebar */}
        <aside className="w-full lg:w-72 shrink-0 bg-surface-container-low p-6 rounded-[28px] space-y-8 sticky top-24 self-start shadow-sm border border-secondary/5">
           <div className="flex items-center justify-between">
              <h3 className="text-[11px] font-bold uppercase tracking-widest text-on-surface-variant">Filters</h3>
              <button className="text-[11px] font-bold uppercase text-[#6750a4] hover:underline underline-offset-4">Clear All</button>
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
              <Checkbox label="Unresponsive" checked color="bg-[#b3261e] border-[#b3261e]" />
           </FilterSection>

           <FilterSection title="Floor">
              <div className="relative group">
                <select className="w-full bg-white text-on-surface font-bold text-[14px] px-4 py-3 rounded-[16px] border-none focus:ring-2 focus:ring-primary/20 appearance-none transition-all shadow-sm">
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
        <div className="flex-1 bg-surface-container-low rounded-[28px] shadow-sm overflow-hidden border border-secondary/5">
           {/* Table Header */}
           <div className="grid grid-cols-[3fr_2fr_2fr_2fr_1.5fr_1fr] gap-4 px-6 py-4 bg-surface-container-low border-b border-[#e6e0e9] font-bold text-[11px] uppercase tracking-widest text-on-surface-variant">
             <div>Staff Member</div>
             <div>Role / ID</div>
             <div>Assignment</div>
             <div>Last Seen</div>
             <div>Status</div>
             <div className="text-right pr-4">Actions</div>
           </div>

           {/* Table Content */}
           <div className="p-2 space-y-1 bg-white">
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
                avatar="https://api.dicebear.com/7.x/avataaars/svg?seed=Michael"
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
                color="bg-[#e8def8] text-[#21005d]"
                avatar="https://api.dicebear.com/7.x/avataaars/svg?seed=Sarah"
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
                avatar="https://api.dicebear.com/7.x/avataaars/svg?seed=David"
              />
           </div>
        </div>
      </div>
    </div>
  );
}

function Badge({ label, color }: any) {
  return (
    <span className={cn("px-4 py-1.5 rounded-full text-[10px] font-bold uppercase tracking-wider", color)}>
      {label}
    </span>
  );
}

function HeaderAction({ icon: Icon, label }: any) {
  return (
    <button className="flex items-center gap-2 px-5 py-2.5 rounded-full bg-white text-on-surface hover:bg-[#f5f3f7] transition-all font-bold text-[13px] shadow-sm active:scale-95 border border-secondary/10">
      <Icon className="w-4 h-4 text-on-surface-variant" />
      {label}
    </button>
  );
}

function FilterSection({ title, children }: any) {
  return (
    <div className="space-y-4">
       <p className="text-[11px] font-bold uppercase tracking-widest text-on-surface-variant">{title}</p>
       <div className="flex flex-col gap-3">
         {children}
       </div>
    </div>
  );
}

function Checkbox({ label, checked, color = "bg-[#6750a4] border-[#6750a4]" }: any) {
  return (
    <label className="flex items-center gap-3 group cursor-pointer">
       <div className={cn(
         "w-5 h-5 rounded-md border-2 transition-all flex items-center justify-center",
         checked ? color : "border-[#dad8dc] bg-white group-hover:border-[#6750a4]/40"
       )}>
         {checked && <CheckCircle2 className="w-3.5 h-3.5 text-white" />}
       </div>
       <span className={cn("text-[14px] transition-colors", checked ? "text-on-surface font-bold" : "text-on-surface-variant font-medium group-hover:text-on-surface")}>
         {label}
       </span>
    </label>
  );
}

function StaffRow({ name, phone, role, id, assignment, lastSeen, location, status, responseTime, avatar, color, isUnresponsive }: any) {
  return (
    <div className={cn(
      "grid grid-cols-[3fr_2fr_2fr_2fr_1.5fr_1fr] gap-4 px-4 py-4 items-center hover:bg-[#f5f3f7] rounded-2xl transition-all cursor-pointer group relative",
      isUnresponsive && "bg-[#f9dedc]/30"
    )}>
       <div className="flex items-center gap-4">
          <div className="w-12 h-12 rounded-full bg-[#f5f3f7] overflow-hidden shadow-sm shrink-0 border border-secondary/5">
             <img src={avatar} alt={name} className="w-full h-full object-cover" />
          </div>
          <div>
            <h4 className="text-[15px] font-bold text-on-surface leading-none">{name}</h4>
            <p className="text-[12px] font-medium text-on-surface-variant mt-2">Ph: {phone}</p>
          </div>
       </div>

       <div>
         <p className="text-[14px] font-bold text-on-surface leading-none">{role}</p>
         <p className="text-[10px] font-bold text-on-surface-variant mt-2 uppercase tracking-widest bg-[#f5f3f7] w-fit px-1.5 py-0.5 rounded-lg border border-secondary/5">{id}</p>
       </div>

       <div className="text-[14px] font-bold text-on-surface leading-tight text-left pr-4">
         {assignment}
       </div>

       <div>
          <p className="text-[14px] font-bold text-on-surface leading-none">{lastSeen}</p>
          <p className="text-[10px] font-bold text-on-surface-variant mt-2 uppercase tracking-widest">{location}</p>
       </div>

       <div>
          <span className={cn(
            "px-3 py-1.5 rounded-full text-[10px] font-bold uppercase tracking-widest",
            isUnresponsive ? "bg-[#b3261e] text-white shadow-sm" : (color || "bg-[#dad8dc] text-on-surface-variant")
          )}>{status}</span>
       </div>

       <div className="flex justify-end gap-2 opacity-0 group-hover:opacity-100 transition-opacity pr-2">
          <button className="p-2 hover:bg-white rounded-full text-on-surface-variant hover:text-[#6750a4] shadow-sm"><MessageCircle className="w-4 h-4" /></button>
          <button className="p-2 hover:bg-white rounded-full text-on-surface-variant hover:text-[#6750a4] shadow-sm"><MapPin className="w-4 h-4" /></button>
          <button className="p-2 hover:bg-white rounded-full text-on-surface-variant hover:text-[#6750a4] shadow-sm"><MoreHorizontal className="w-4 h-4" /></button>
       </div>
    </div>
  );
}
