import React from 'react';
import { motion } from 'motion/react';
import { 
  AlertTriangle, Phone, MapPin, AlertCircle, ShieldAlert
} from 'lucide-react';
import { cn } from '../lib/utils';
import { MapContainer, TileLayer, CircleMarker, Polyline } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

export default function Overview() {
  return (
    <div className="font-sans">
      <div className="grid grid-cols-12 gap-12">
        {/* Main Left Column */}
        <div className="col-span-12 xl:col-span-8 flex flex-col">
           {/* Header Area */}
           <div className="flex justify-between items-start mb-6">
              <div>
                 <h2 className="text-[56px] font-black tracking-tighter text-[#1d192b] leading-none mb-3 uppercase">Command</h2>
                 <div className="flex items-center gap-2">
                    <div className="w-2 h-2 rounded-full bg-[#6750a4]" />
                    <p className="text-[11px] font-black text-[#6750a4] tracking-[0.3em] uppercase">Precision Control System v4.2</p>
                 </div>
              </div>
              <div className="flex items-center gap-6">
                 <div className="text-right">
                    <p className="text-[10px] font-bold tracking-[0.1em] text-on-surface-variant uppercase">Property<br/>Time</p>
                    <p className="text-[28px] font-bold text-[#1d192b] leading-none mt-1">14:30</p>
                 </div>
                 <button className="bg-[#4a4458] text-white px-6 py-3 rounded-l-full rounded-r-full font-bold text-[13px] tracking-wide flex items-center gap-2 hover:bg-[#322f3b] transition-colors uppercase shadow-sm">
                    <AlertTriangle className="w-4 h-4" />
                    Raise System Alert
                 </button>
              </div>
           </div>

           {/* Map Container */}
           <div className="relative flex-1 min-h-[600px] bg-[#e7e5e8]/50 rounded-[32px] overflow-hidden shadow-sm border border-secondary/5">
              <MapContainer center={[51.505, -0.09]} zoom={18} zoomControl={false} className="w-full h-full" style={{ background: '#f0f0f0' }}>
                <TileLayer
                  url="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png"
                  attribution='&copy; OpenStreetMap contributors &copy; CARTO'
                />
                <CircleMarker center={[51.505, -0.09]} radius={80} color="#b3261e" fillColor="#b3261e" fillOpacity={0.1} stroke={false} />
                <CircleMarker center={[51.505, -0.09]} radius={16} color="#b3261e" fillColor="#b3261e" fillOpacity={1} stroke={false} />
                <Polyline positions={[[51.505, -0.09], [51.504, -0.09], [51.504, -0.088], [51.503, -0.088]]} color="#f59e0b" weight={3} dashArray="5, 10" />
              </MapContainer>
              
              {/* Ping Marker UI Overlay for Icon */}
              <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 z-[400] pointer-events-none">
                <AlertCircle className="w-6 h-6 text-white absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2" />
              </div>

              {/* Floating Alert Panel at bottom of map */}
              <div className="absolute bottom-6 left-6 right-6 z-[400]">
                <div className="bg-[#f9dedc] rounded-[24px] p-6 flex flex-col md:flex-row items-start md:items-center justify-between shadow-sm border border-[#b3261e]/10">
                   <div className="flex items-center gap-5">
                     <div className="w-14 h-14 bg-[#b3261e] rounded-[16px] flex items-center justify-center text-white">
                        <AlertCircle className="w-8 h-8" />
                     </div>
                     <div className="space-y-1">
                        <h2 className="text-[20px] font-bold text-[#410e0b] uppercase leading-tight tracking-tight">Active Incident: Fire - Floor 3, Wing B</h2>
                        <p className="text-[11px] font-bold text-[#b3261e] uppercase tracking-wider">12 Responders Deployed • 45 Guests in Danger Zone</p>
                     </div>
                   </div>
                   <button className="mt-4 md:mt-0 bg-[#e8def8] text-[#21005d] px-6 py-3 rounded-full uppercase tracking-wider font-bold text-[12px] hover:bg-[#d0c4e8] transition-colors">
                      View Full Incident
                   </button>
                </div>
              </div>
           </div>
        </div>

        {/* Analytics Aside */}
        <aside className="col-span-12 xl:col-span-4 flex flex-col">
           <div className="mb-10">
              <h3 className="text-[11px] font-black text-[#21005d] tracking-[0.2em] uppercase mb-6">System Analytics</h3>
              <div className="grid grid-cols-1 gap-4">
                 <AnalyticsMetric label="Staff On-Duty" value="142" />
                 <AnalyticsMetric label="Active Incidents" value="01" isError />
                 <AnalyticsMetric label="Guests Tracked" value="856" />
                 <AnalyticsMetric label="Avg Response" value="2" sub="m" value2="14" sub2="s" />
              </div>
           </div>

           <div className="mb-10">
              <div className="flex items-center justify-between mb-6">
                <h3 className="text-[11px] font-black text-on-surface-variant tracking-[0.2em] uppercase">Live Responders</h3>
                <div className="w-2 h-2 rounded-full bg-secondary/20" />
              </div>
              <div className="space-y-3">
                 <ResponderMini init="JD" name="John Doe" role="Security Lead" status="En Route" />
                 <ResponderMini init="AS" name="Alice Smith" role="Medical" status="On Scene" />
              </div>
           </div>

           <div>
              <h3 className="text-[11px] font-black text-on-surface-variant tracking-[0.2em] uppercase mb-6">Historical Queue</h3>
              <div className="space-y-6 ml-2 border-l-2 border-secondary/10 pr-4 relative pb-4">
                 <HistoryItem title="Medical Assist" time="10M AGO" location="Pool Deck • Resolved" />
                 <HistoryItem title="Noise Complaint" time="1H AGO" location="Room 402 • Closed" />
              </div>
           </div>
        </aside>
      </div>
    </div>
  );
}

function AnalyticsMetric({ label, value, sub, value2, sub2, isError }: any) {
  return (
    <div className={cn(
      "p-6 rounded-[24px] cursor-default flex flex-col justify-center h-[120px]",
      isError ? "bg-[#f9dedc]" : "bg-[#f5f3f7]"
    )}>
       <div className={cn("text-[10px] font-bold uppercase tracking-widest mb-1", isError ? "text-[#b3261e]" : "text-on-surface-variant")}>{label}</div>
       <div className="flex items-baseline gap-0.5">
          <span className={cn("text-[48px] font-bold font-sans leading-none tracking-tighter", isError ? "text-[#b3261e]" : "text-[#1d192b]")}>{value}</span>
          {sub && <span className="text-[20px] font-bold text-on-surface-variant lowercase ml-1">{sub}</span>}
          {value2 && <span className="text-[48px] font-bold font-sans leading-none tracking-tighter text-[#1d192b] ml-3">{value2}</span>}
          {sub2 && <span className="text-[20px] font-bold text-on-surface-variant lowercase ml-1">{sub2}</span>}
       </div>
    </div>
  );
}

function ResponderMini({ init, name, role, status }: any) {
  return (
    <div className="bg-[#f5f3f7] p-4 rounded-[20px] flex items-center justify-between">
       <div className="flex items-center gap-4">
          <div className="w-10 h-10 bg-[#e6e0e9] text-[#49454f] rounded-full flex items-center justify-center font-bold text-sm">{init}</div>
          <div>
            <div className="text-[13px] font-bold text-[#1d192b] leading-tight">{name}</div>
            <div className="text-[10px] font-semibold text-on-surface-variant uppercase tracking-wide mt-0.5">{role}</div>
          </div>
       </div>
       <span className={cn("text-[9px] font-bold px-3 py-1.5 rounded-full uppercase tracking-wider", status === 'En Route' ? "bg-[#e6e0e9] text-on-surface-variant" : "bg-[#dad8dc] text-on-surface-variant")}>{status}</span>
    </div>
  );
}

function HistoryItem({ title, time, location }: any) {
  return (
    <div className="relative pl-6">
       <div className="absolute -left-[5px] top-1.5 w-2 h-2 rounded-full bg-[#49454f] ring-4 ring-surface" />
       <div className="flex justify-between items-center mb-0.5">
          <span className="text-[11px] font-bold uppercase text-[#1d192b] tracking-wider">{title}</span>
          <span className="text-[9px] font-bold text-on-surface-variant uppercase tracking-widest">{time}</span>
       </div>
       <p className="text-[9px] font-bold text-on-surface-variant uppercase tracking-widest">{location}</p>
    </div>
  );
}
