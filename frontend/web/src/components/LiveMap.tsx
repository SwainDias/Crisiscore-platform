import React, { useState } from 'react';
import { motion } from 'motion/react';
import { MapPin, ShieldAlert, Users, Video, Filter, FireExtinguisher, Crosshair, Phone } from 'lucide-react';
import { cn } from '../lib/utils';
import { MapContainer, TileLayer, CircleMarker } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

export default function LiveMap() {
  const [activeFloor, setActiveFloor] = useState('Floor 1');
  const [layers, setLayers] = useState({
    staff: true,
    heatmap: false,
    incidents: true,
    cctv: false
  });

  return (
    <div className="h-[calc(100vh-4rem)] w-full relative bg-[#1d192b] overflow-hidden">
      {/* Map Background using React Leaflet */}
      <div className="absolute inset-0 z-0">
        <MapContainer center={[51.505, -0.09]} zoom={18} zoomControl={false} className="w-full h-full" style={{ background: '#1d192b' }}>
           <TileLayer
             url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
             attribution='&copy; OpenStreetMap contributors &copy; CARTO'
           />
           {/* Markers for Staff */}
           <CircleMarker center={[51.504, -0.091]} radius={6} color="#6750a4" fillColor="#6750a4" fillOpacity={1} stroke={true} weight={2} />
           <CircleMarker center={[51.506, -0.088]} radius={6} color="#6750a4" fillColor="#6750a4" fillOpacity={1} stroke={true} weight={2} />
           <CircleMarker center={[51.5055, -0.092]} radius={6} color="#6750a4" fillColor="#6750a4" fillOpacity={1} stroke={true} weight={2} />
           
           {/* Incident Marker */}
           <CircleMarker center={[51.505, -0.089]} radius={20} color="#b3261e" fillColor="#b3261e" fillOpacity={0.2} stroke={false} />
           <CircleMarker center={[51.505, -0.089]} radius={10} color="#b3261e" fillColor="#b3261e" fillOpacity={1} stroke={false} />

           {/* Guest Cluster */}
           <CircleMarker center={[51.5045, -0.093]} radius={12} color="#e8def8" fillColor="#e8def8" fillOpacity={1} stroke={true} weight={2} />
        </MapContainer>
      </div>

      {/* Floating UI Overlay */}
      <div className="absolute top-6 left-6 w-[300px] space-y-4 z-[400] pointer-events-none">
        {/* Floor Selector */}
        <div className="bg-[#f5f3f7] rounded-full p-1.5 shadow-lg flex pointer-events-auto">
          {['Floor 1', 'Floor 2', 'Floor 3', 'Roof'].map((floor) => (
            <button
              key={floor}
              onClick={() => setActiveFloor(floor)}
              className={cn(
                "flex-1 py-2 text-xs font-bold transition-all rounded-full",
                activeFloor === floor 
                  ? "bg-white text-[#1d192b] shadow-sm" 
                  : "text-on-surface-variant hover:text-[#1d192b]"
              )}
            >
              {floor}
            </button>
          ))}
        </div>

        {/* Layers & Filters */}
        <div className="bg-[#f5f3f7] rounded-[28px] p-6 shadow-xl space-y-6 pointer-events-auto">
          <div>
            <h3 className="text-[11px] font-black tracking-widest text-on-surface-variant uppercase mb-4">Map Layers</h3>
            <div className="space-y-4">
              <LayerToggle label="Staff Location" icon={MapPin} active={layers.staff} onChange={(val: boolean) => setLayers({...layers, staff: val})} color="text-[#6750a4]" />
              <LayerToggle label="Guest Heatmap" icon={Users} active={layers.heatmap} onChange={(val: boolean) => setLayers({...layers, heatmap: val})} />
              <LayerToggle label="Active Incidents" icon={ShieldAlert} active={layers.incidents} onChange={(val: boolean) => setLayers({...layers, incidents: val})} color="text-[#6750a4]" />
              <LayerToggle label="CCTV Cameras" icon={Video} active={layers.cctv} onChange={(val: boolean) => setLayers({...layers, cctv: val})} />
            </div>
          </div>
          
          <div className="pt-6 border-t border-secondary/10">
            <h3 className="text-[11px] font-black tracking-widest text-on-surface-variant uppercase mb-4">Incident Filters</h3>
            <div className="flex flex-wrap gap-2">
              <button className="px-4 py-2 bg-[#f9dedc] text-[#410e0b] text-[12px] font-bold rounded-xl flex items-center gap-1.5 transition-all">
                Fire (1)
              </button>
              <button className="px-4 py-2 bg-white text-on-surface-variant text-[12px] font-bold rounded-xl hover:bg-[#e7e5e8] transition-all">
                Medical
              </button>
              <button className="px-4 py-2 bg-white text-on-surface-variant text-[12px] font-bold rounded-xl hover:bg-[#e7e5e8] transition-all">
                Security
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Active Incident Details Floating */}
      <div className="absolute top-6 right-6 w-[340px] space-y-4 z-[400] pointer-events-none">
         <motion.div 
           initial={{ x: 50, opacity: 0 }}
           animate={{ x: 0, opacity: 1 }}
           className="bg-white rounded-[28px] shadow-xl overflow-hidden pointer-events-auto"
         >
           <div className="bg-[#f9dedc] p-6 relative">
              <div className="flex justify-between items-start mb-4">
                <div className="bg-[#b3261e] text-white px-2.5 py-1 rounded-md text-[10px] font-bold tracking-widest uppercase flex items-center gap-1">
                  <FireExtinguisher className="w-3.5 h-3.5 fill-current" />
                  Critical Alarm
                </div>
                <span className="text-[12px] font-bold text-[#b3261e]">00:04:12</span>
              </div>
              <h2 className="text-[20px] font-bold text-[#410e0b] leading-tight">Smoke Detected: Sector 4 Storage</h2>
              <p className="text-[11px] text-[#b3261e] mt-1.5 uppercase font-medium tracking-wide">Incident #4029 • Auto-Triggered</p>
           </div>
           
           <div className="p-6 space-y-5">
             <div className="grid grid-cols-2 gap-y-5 gap-x-4">
               <InfoItem label="Location" value="Floor 2, Room 24B" />
               <InfoItem label="Sensor Status" value="Active" isError />
               <InfoItem label="Proximity Risk" value="14 Guests nearby" />
               <InfoItem label="Closest Staff" value="J. Doe (Security)" />
             </div>

             <div className="pt-5 border-t border-secondary/10">
               <h4 className="text-[10px] font-bold uppercase tracking-widest text-on-surface-variant mb-3">Dispatched Units</h4>
               <div className="flex items-center gap-3 bg-[#f5f3f7] p-3 rounded-2xl">
                 <div className="w-10 h-10 rounded-full overflow-hidden">
                   <img src="https://i.pravatar.cc/150?u=security" alt="Security" className="w-full h-full object-cover" />
                 </div>
                 <div className="flex-1">
                   <p className="text-[13px] font-bold text-[#1d192b]">Unit Alpha-1</p>
                   <p className="text-[11px] text-[#6750a4] font-semibold">En route • ETA 2m</p>
                 </div>
                 <button className="w-8 h-8 rounded-full bg-white flex items-center justify-center shadow-sm hover:bg-[#e7e5e8] transition-colors">
                   <Phone className="w-4 h-4 text-on-surface-variant" />
                 </button>
               </div>
             </div>
           </div>
         </motion.div>

         <div className="bg-white rounded-[28px] p-5 shadow-xl space-y-3 pointer-events-auto">
           <button className="w-full bg-[#6750a4] text-white py-3.5 rounded-[20px] font-bold text-[14px] shadow-sm hover:bg-[#5a4691] active:scale-[0.98] transition-all flex justify-center items-center gap-2">
             <Crosshair className="w-4.5 h-4.5" />
             Assign Responder
           </button>
           <div className="grid grid-cols-2 gap-3">
             <button className="py-3 rounded-[20px] bg-[#f9dedc] text-[#410e0b] font-bold text-[13px] hover:bg-[#f2b8b5] transition-all flex items-center justify-center gap-2">
                <ShieldAlert className="w-4 h-4 text-[#b3261e]" />
                Escalate
             </button>
             <button className="py-3 rounded-[20px] bg-[#f5f3f7] text-[#1d192b] font-bold text-[13px] hover:bg-[#e7e5e8] transition-all flex items-center justify-center gap-2">
                <Users className="w-4 h-4 text-on-surface-variant" />
                Broadcast
             </button>
           </div>
         </div>
      </div>

      {/* Global Stats Footer */}
      <div className="absolute bottom-6 left-1/2 -translate-x-1/2 h-[60px] bg-[#f5f3f7] rounded-full shadow-xl flex items-center px-8 justify-between z-[400] pointer-events-auto w-max gap-12">
        <div className="flex items-center gap-8">
          <StatMini dotColor="bg-[#6750a4]" label="Staff Online" value="142" />
          <StatMini dotColor="bg-[#6750a4]" label="Guests Present" value="890" />
          <div className="flex items-center gap-2 bg-[#f9dedc] px-4 py-1.5 rounded-full">
             <div className="w-2 h-2 rounded-full bg-[#b3261e] animate-pulse" />
             <span className="text-[12px] font-bold text-[#b3261e]">Active Incidents: 1</span>
          </div>
        </div>
        <div className="flex items-center gap-2 text-[10px] font-bold uppercase tracking-widest text-on-surface-variant border-l border-secondary/10 pl-6">
           <motion.div animate={{ rotate: 360 }} transition={{ repeat: Infinity, duration: 4, ease: "linear" }}>
             <Filter className="w-3.5 h-3.5" />
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
        <span className={cn("text-[13px] transition-colors", active ? "text-[#1d192b] font-bold" : "text-on-surface-variant font-medium")}>{label}</span>
      </div>
      <div className={cn("w-10 h-6 rounded-full relative transition-colors", active ? "bg-[#6750a4]" : "bg-[#dad8dc]")}>
        <motion.div 
          animate={{ x: active ? 18 : 2 }}
          className={cn("absolute top-[2px] w-5 h-5 rounded-full shadow-sm", active ? "bg-white" : "bg-[#49454f]")} 
        />
      </div>
    </div>
  );
}

function InfoItem({ label, value, isError }: any) {
  return (
    <div className="space-y-1 text-left">
      <p className="text-[9px] font-bold uppercase tracking-widest text-on-surface-variant">{label}</p>
      <div className={cn("text-[13px] font-bold", isError ? "text-[#b3261e] flex items-center gap-1.5" : "text-[#1d192b]")}>
        {isError && <div className="w-1.5 h-1.5 rounded-full bg-[#b3261e]" />}
        {value}
      </div>
    </div>
  );
}

function StatMini({ dotColor, label, value }: any) {
  return (
    <div className="flex items-center gap-2">
      <div className={cn("w-2 h-2 rounded-full", dotColor)} />
      <span className="text-[12px] font-medium text-on-surface-variant">
        {label}: <span className="text-[#1d192b] font-bold ml-1">{value}</span>
      </span>
    </div>
  );
}
