import React from 'react';
import { 
  SlidersHorizontal, Puzzle, UserPlus, ClipboardList, 
  TriangleAlert, Plus, RefreshCcw, ChevronRight
} from 'lucide-react';
import { cn } from '../lib/utils';

export default function SystemSettings() {
  return (
    <div className="space-y-8 font-sans">
      {/* Header */}
      <div className="max-w-2xl mt-4">
        <h2 className="text-[36px] font-bold tracking-tight text-[#1d192b] mb-1">System Settings</h2>
        <p className="text-[#49454f] text-[15px]">Manage integrations, user access, and global protocol configurations.</p>
      </div>

      <div className="grid grid-cols-12 gap-8">
        {/* Sidebar Nav */}
        <aside className="col-span-12 lg:col-span-4 xl:col-span-3 bg-[#f5f3f7] rounded-[28px] p-4 flex flex-col gap-2 self-start">
           <SettingsNavItem icon={SlidersHorizontal} label="General" />
           <SettingsNavItem icon={Puzzle} label="Integrations" active />
           <SettingsNavItem icon={UserPlus} label="Users & Roles" />
           <SettingsNavItem icon={ClipboardList} label="Incident Protocols" />
           <div className="h-[1px] bg-black/5 my-2 mx-4" />
           <SettingsNavItem icon={TriangleAlert} label="Danger Zone" isDanger />
        </aside>

        {/* Content Area */}
        <div className="col-span-12 lg:col-span-8 xl:col-span-9 space-y-6">
           {/* Section Header */}
           <div className="flex items-center justify-between bg-[#f5f3f7] rounded-[24px] p-6 py-5">
              <div>
                <h3 className="text-[20px] font-bold text-[#1d192b]">Active Integrations</h3>
                <p className="text-[#49454f] text-[14px] mt-0.5">Connect third-party systems for unified command response.</p>
              </div>
              <button className="bg-[#6750a4] text-white px-5 py-2.5 rounded-full font-medium text-[14px] flex items-center gap-2 hover:bg-[#5a4691] transition-colors shadow-sm">
                <Plus className="w-4 h-4" />
                Browse Directory
              </button>
           </div>

           {/* Cards Grid */}
           <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <IntegrationCard 
                name="Salto Access"
                category="Physical Security"
                desc="Syncs live access logs and door statuses to the command map. Enables remote lockdown capabilities during active incidents."
                status="Connected"
                latency="22ms latency"
                lastSynced="Just now"
                syncType={
                  <div className="text-right">
                    <div>Real-time</div>
                    <div className="text-gray-500 font-normal leading-tight">(Webhook)</div>
                  </div>
                }
                nodes="142 Active"
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
      "w-full flex items-center gap-4 px-5 py-3.5 rounded-full transition-all duration-200 group text-left",
      active 
        ? "bg-[#e8def8] text-[#1d192b] font-semibold" 
        : isDanger 
          ? "text-[#b3261e] hover:bg-[#b3261e]/10 font-medium" 
          : "text-[#49454f] hover:bg-black/5 font-medium"
    )}>
      <Icon className={cn("w-[22px] h-[22px]", active ? "text-[#1d192b] fill-current" : isDanger ? "text-[#b3261e]" : "text-[#49454f]")} />
      <span className="text-[14px]">{label}</span>
    </button>
  );
}

function IntegrationCard({ name, category, desc, status, latency, lastSynced, syncType, nodes }: any) {
  return (
    <div className="bg-[#f3f1f4] rounded-[28px] p-6 space-y-5 flex flex-col">
       <div className="flex items-start justify-between">
          <div className="flex items-center gap-4">
             {/* Icon Placeholder representing the Salto device */}
             <div className="w-11 h-11 bg-[#233543] rounded-lg flex items-center justify-center relative overflow-hidden shadow-sm">
                <div className="w-[22px] h-[28px] bg-[#3a4f60] border border-[#5d7386] rounded-[4px] flex flex-col items-center p-[2px] gap-[2px]">
                  <div className="w-full h-2.5 bg-[#4fd1c5] rounded-sm opacity-80"></div>
                  <div className="w-full flex-1 flex flex-wrap gap-[1px] pt-[1px]">
                     {[...Array(9)].map((_, i) => (
                       <div key={i} className="w-[4px] h-[4px] bg-[#758e9f] rounded-[1px]"></div>
                     ))}
                  </div>
                </div>
             </div>
             <div>
                <h4 className="text-[18px] font-bold text-[#1d192b] leading-tight">{name}</h4>
                <p className="text-[#49454f] text-[13px] mt-0.5">{category}</p>
             </div>
          </div>
          <div className={cn(
            "px-2.5 py-1 rounded-full text-[11px] font-semibold flex items-center gap-1.5",
            status === 'Connected' ? "bg-[#c4eed0] text-[#0f5223]" : "bg-black/10 text-gray-700"
          )}>
             <div className={cn("w-1.5 h-1.5 rounded-full", status === 'Connected' ? "bg-[#188038]" : "bg-gray-500")} />
             {status}
          </div>
       </div>

       <p className="text-[14px] text-[#49454f] leading-[1.6]">
          {desc}
       </p>

       <div className="bg-[#e7e5e8] rounded-[20px] p-5 space-y-4">
          <div className="flex justify-between items-center text-[11px] font-bold text-[#1d192b]">
            <span className="uppercase tracking-widest">API Status</span>
            <span className="bg-[#dad8dc] px-2 py-1 rounded-md text-[#49454f] font-normal">{latency}</span>
          </div>
          <div className="space-y-3 pt-1">
             <DetailItem label="Last Synced" value={lastSynced} />
             <DetailItem label="Sync Schedule" value={syncType} />
             <DetailItem label="Door Nodes" value={nodes} />
          </div>
       </div>

       <div className="flex items-center justify-between pt-1">
          <div className="flex items-center gap-2 text-[13px] font-medium text-[#49454f]">
             <RefreshCcw className="w-[14px] h-[14px]" />
             Auto-sync active
          </div>
          <button className="text-[14px] font-semibold text-[#6750a4] flex items-center gap-0.5 hover:underline pr-1">
             Configure
             <ChevronRight className="w-4 h-4" />
          </button>
       </div>
    </div>
  );
}

function DetailItem({ label, value }: any) {
  return (
    <div className="flex justify-between items-start text-[14px]">
       <span className="text-[#49454f]">{label}</span>
       <span className="text-[#1d192b] font-semibold text-right">{value}</span>
    </div>
  );
}

