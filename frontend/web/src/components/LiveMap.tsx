import React, { useState } from 'react';
import { motion } from 'motion/react';
import { MapPin, ShieldAlert, Users, Video, Filter, FireExtinguisher, Crosshair, Phone } from 'lucide-react';
import { cn } from '../lib/utils';

export default function LiveMap() {
  const [activeFloor, setActiveFloor] = useState('Floor 1');
  const [layers, setLayers] = useState({
    staff: true,
    heatmap: false,
    incidents: true,
    cctv: false
  });

  return (
    <div className="h-[calc(100vh-10rem)] w-full relative bg-inverse-surface rounded-3xl overflow-hidden shadow-2xl border border-white/5">
      {/* Map Background Simulation */}
      <div className="absolute inset-0 w-full h-full opacity-60 flex items-center justify-center pointer-events-none">
         <img 
            src="https://images.unsplash.com/photo-1542661062-843818e98031?auto=format&fit=crop&q=80&w=2000" 
            className="w-full h-full object-cover mix-blend-screen opacity-40 grayscale contrast-150"
            alt="Schematic"
         />
         <div className="absolute inset-0 bg-gradient-to-tr from-primary/10 to-transparent" />
         <div className="grid grid-cols-12 grid-rows-12 absolute inset-0 opacity-10">
           {Array.from({ length: 144 }).map((_, i) => (
             <div key={i} className="border-[0.5px] border-on-surface-variant/20" />
           ))}
         </div>
      </div>

      {/* Map Content - Interactive Elements */}
      <div className="absolute inset-0">
        {/* Fire Incident */}
        <motion.div 
          initial={{ scale: 0.8, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          className="absolute top-[40%] left-[55%] -translate-x-1/2 -translate-y-1/2"
        >
          <div className="relative">
            <div className="absolute inset-0 bg-error/20 rounded-full animate-ping scale-150" />
            <div className="relative w-12 h-12 rounded-full bg-error/20 border border-error/50 flex items-center justify-center backdrop-blur-md shadow-[0_0_20px_rgba(186,26,26,0.4)]">
               <ShieldAlert className="w-6 h-6 text-error fill-current" />
            </div>
          </div>
        </motion.div>

        {/* Staff Markers */}
        <div className="absolute top-[35%] left-[48%] w-3 h-3 rounded-full bg-primary ring-2 ring-inverse-surface shadow-lg" />
        <div className="absolute top-[45%] left-[58%] w-3 h-3 rounded-full bg-primary ring-2 ring-inverse-surface shadow-lg" />
        <div className="absolute top-[42%] left-[42%] w-3 h-3 rounded-full bg-primary ring-2 ring-inverse-surface shadow-lg" />

        {/* Guest Cluster */}
        <div className="absolute top-[60%] left-[35%] w-8 h-8 rounded-full bg-secondary-container text-on-secondary-container flex items-center justify-center font-bold text-xs ring-2 ring-inverse-surface shadow-2xl">
          14
        </div>
      </div>

      {/* Floating UI Overlay */}
      <div className="absolute top-6 left-6 w-72 space-y-4">
        {/* Floor Selector */}
        <div className="glass rounded-2xl p-1.5 shadow-xl flex border border-white/10">
          {['Floor 1', 'Floor 2', 'Floor 3', 'Roof'].map((floor) => (
            <button
              key={floor}
              onClick={() => setActiveFloor(floor)}
              className={cn(
                "flex-1 py-2 text-xs font-bold transition-all rounded-xl",
                activeFloor === floor 
                  ? "bg-surface-container-high text-on-surface shadow-sm" 
                  : "text-on-surface-variant hover:text-on-surface"
              )}
            >
              {floor}
            </button>
          ))}
        </div>

        {/* Layers & Filters */}
        <div className="glass rounded-3xl p-5 shadow-2xl space-y-5 border border-white/10">
          <div>
            <h3 className="text-[11px] font-bold tracking-[0.05em] text-on-surface-variant uppercase mb-4">Map Layers</h3>
            <div className="space-y-4">
              <LayerToggle label="Staff Location" icon={MapPin} active={layers.staff} onChange={(val) => setLayers({...layers, staff: val})} color="text-primary" />
              <LayerToggle label="Guest Heatmap" icon={Users} active={layers.heatmap} onChange={(val) => setLayers({...layers, heatmap: val})} />
              <LayerToggle label="Active Incidents" icon={ShieldAlert} active={layers.incidents} onChange={(val) => setLayers({...layers, incidents: val})} color="text-primary" />
              <LayerToggle label="CCTV Cameras" icon={Video} active={layers.cctv} onChange={(val) => setLayers({...layers, cctv: val})} />
            </div>
          </div>
          
          <div className="pt-5 border-t border-secondary/10">
            <h3 className="text-[11px] font-bold tracking-[0.05em] text-on-surface-variant uppercase mb-4">Incident Filters</h3>
            <div className="flex flex-wrap gap-2">
              <button className="px-3 py-1.5 bg-error-container text-on-error-container text-[11px] font-bold rounded-xl flex items-center gap-1.5 active:scale-95 transition-all">
                Fire (1)
              </button>
              <button className="px-3 py-1.5 bg-surface-container-high text-on-surface-variant text-[11px] font-bold rounded-xl hover:bg-surface-container-highest active:scale-95 transition-all">
                Medical
              </button>
              <button className="px-3 py-1.5 bg-surface-container-high text-on-surface-variant text-[11px] font-bold rounded-xl hover:bg-surface-container-highest active:scale-95 transition-all">
                Security
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Active Incident Details Floating */}
      <div className="absolute top-6 right-6 w-80 space-y-4">
         <motion.div 
           initial={{ x: 50, opacity: 0 }}
           animate={{ x: 0, opacity: 1 }}
           className="glass rounded-3xl shadow-2xl overflow-hidden border border-white/10"
         >
           <div className="bg-error-container/80 p-5 relative">
              <div className="flex justify-between items-start mb-3">
                <div className="bg-error text-on-error px-2 py-0.5 rounded-full text-[10px] font-bold tracking-widest uppercase flex items-center gap-1">
                  <FireExtinguisher className="w-3 h-3 fill-current" />
                  Critical Alarm
                </div>
                <span className="text-xs font-bold text-on-error-container/80">00:04:12</span>
              </div>
              <h2 className="text-lg font-bold text-on-error-container leading-tight">Smoke Detected: Sector 4 Storage</h2>
              <p className="text-xs text-on-error-container opacity-90 mt-1 uppercase font-bold tracking-tighter italic">Incident #4029 • Auto-Triggered</p>
           </div>
           
           <div className="p-5 space-y-4 bg-surface-container-lowest/50">
             <div className="grid grid-cols-2 gap-4">
               <InfoItem label="Location" value="Floor 2, Room 24B" />
               <InfoItem label="Status" value="Active" isError />
               <InfoItem label="Risk" value="14 Guests nearby" />
               <InfoItem label="Closest Staff" value="J. Doe (Security)" />
             </div>

             <div className="pt-2">
               <h4 className="text-[10px] font-bold uppercase tracking-[0.05em] text-on-surface-variant mb-2 font-sans">Dispatched Units</h4>
               <div className="flex items-center gap-3 bg-surface-container/30 p-2.5 rounded-2xl border border-white/5">
                 <div className="w-10 h-10 rounded-full bg-surface-container-high overflow-hidden">
                   <img src="https://i.pravatar.cc/150?u=security" alt="Security" />
                 </div>
                 <div className="flex-1">
                   <p className="text-xs font-bold text-on-surface">Unit Alpha-1</p>
                   <p className="text-[10px] text-primary font-semibold">En route • ETA 2m</p>
                 </div>
                 <button className="w-8 h-8 rounded-xl bg-surface-container flex items-center justify-center hover:bg-surface-container-high transition-colors">
                   <Phone className="w-4 h-4 text-on-surface-variant" />
                 </button>
               </div>
             </div>
           </div>
         </motion.div>

         <div className="glass rounded-3xl p-4 shadow-2xl border border-white/10 space-y-2">
           <button className="w-full signature-gradient text-on-primary py-3 rounded-2xl font-bold text-sm shadow-lg hover:shadow-primary/20 active:scale-[0.98] transition-all flex justify-center items-center gap-2">
             <Crosshair className="w-4 h-4" />
             Assign Responder
           </button>
           <div className="grid grid-cols-2 gap-2">
             <button className="py-2.5 rounded-2xl bg-error/10 text-error font-bold text-xs hover:bg-error/20 active:scale-[0.98] transition-all">Escalate</button>
             <button className="py-2.5 rounded-2xl bg-surface-container-high text-on-surface-variant font-bold text-xs hover:bg-surface-container-highest active:scale-[0.98] transition-all">Broadcast</button>
           </div>
         </div>
      </div>

      {/* Global Stats Footer */}
      <div className="absolute bottom-6 left-6 right-6 h-14 glass rounded-2xl shadow-2xl border border-white/20 flex items-center px-6 justify-between backdrop-blur-3xl">
        <div className="flex items-center gap-8">
          <StatMini dotColor="bg-primary" label="Staff Online" value="142" />
          <StatMini dotColor="bg-primary-container" label="Guests Present" value="890" />
          <div className="flex items-center gap-2 bg-error/10 px-4 py-1.5 rounded-full border border-error/20">
             <div className="w-2 h-2 rounded-full bg-error animate-pulse" />
             <span className="text-xs font-bold text-error">Active Incidents: 1</span>
          </div>
        </div>
        <div className="flex items-center gap-3 text-[10px] font-bold uppercase tracking-[0.1em] text-on-surface-variant">
           <motion.div animate={{ rotate: 360 }} transition={{ repeat: Infinity, duration: 4, ease: "linear" }}>
             <Filter className="w-3 h-3" />
           </motion.div>
           Live Feed Syncing
        </div>
      </div>
    </div>
  );
}

function LayerToggle({ label, icon: Icon, active, onChange, color = "text-on-surface-variant" }: any) {
  return (
    <div 
      className="flex items-center justify-between group cursor-pointer"
      onClick={() => onChange(!active)}
    >
      <div className="flex items-center gap-3">
        <Icon className={cn("w-4 h-4", active ? color : "text-on-surface-variant/40")} />
        <span className={cn("text-xs transition-colors", active ? "text-on-surface font-bold" : "text-on-surface-variant font-medium")}>{label}</span>
      </div>
      <div className={cn("w-8 h-4 rounded-full relative transition-colors", active ? "bg-primary" : "bg-surface-container-highest")}>
        <motion.div 
          animate={{ x: active ? 16 : 2 }}
          className="absolute top-0.5 w-3 h-3 rounded-full bg-white shadow-sm" 
        />
      </div>
    </div>
  );
}

function InfoItem({ label, value, isError }: any) {
  return (
    <div className="space-y-0.5 text-left">
      <p className="text-[9px] font-bold uppercase tracking-[0.05em] text-on-surface-variant">{label}</p>
      <div className={cn("text-xs font-bold font-sans", isError ? "text-error flex items-center gap-1.5" : "text-on-surface")}>
        {isError && <div className="w-1.5 h-1.5 rounded-full bg-error" />}
        {value}
      </div>
    </div>
  );
}

function StatMini({ dotColor, label, value }: any) {
  return (
    <div className="flex items-center gap-2">
      <div className={cn("w-2 h-2 rounded-full", dotColor)} />
      <span className="text-xs font-bold text-on-surface-variant">
        {label}: <span className="text-on-surface ml-1">{value}</span>
      </span>
    </div>
  );
}
