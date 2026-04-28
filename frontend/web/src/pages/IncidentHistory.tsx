import React from 'react';
import { motion } from 'motion/react';
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, 
} from 'recharts';
import { 
  TrendingDown, TrendingUp, AlertTriangle, Timer, ShieldCheck, 
  Calendar, MoreHorizontal, Lightbulb, ArrowRight, FileText
} from 'lucide-react';
import { cn } from '../lib/utils';

const VOLUME_DATA = [
  { name: 'Jan', fire: 40, security: 20, medical: 10 },
  { name: 'Feb', fire: 30, security: 45, medical: 15 },
  { name: 'Mar', fire: 20, security: 30, medical: 40 },
  { name: 'Apr', fire: 60, security: 15, medical: 5 },
  { name: 'May', fire: 25, security: 25, medical: 10 },
  { name: 'Jun', fire: 15, security: 65, medical: 5 },
];

const HISTOGRAM_DATA = [
  { time: '< 1m', count: 10, fill: '#dad8dc' },
  { time: '1-2m', count: 25, fill: '#dad8dc' },
  { time: '2-3m', count: 60, fill: '#e8def8' },
  { time: '3-4m', count: 85, fill: '#6750a4' },
  { time: '4-5m', count: 45, fill: '#e8def8' },
  { time: '5-6m', count: 20, fill: '#dad8dc' },
  { time: '6m+', count: 5, fill: '#b3261e' },
];

export default function IncidentHistory() {
  return (
    <div className="space-y-6 font-sans pb-12">
      {/* Page Header */}
      <div className="flex justify-between items-center px-1">
        <div>
          <h2 className="text-[32px] font-bold tracking-tight text-on-surface">Incident History & Analytics</h2>
          <p className="text-on-surface-variant text-[15px] mt-1">Review historical response data, compliance metrics, and operational trends.</p>
        </div>
        
        <div className="bg-surface-container-low rounded-full p-1.5 flex gap-1 items-center shadow-sm border border-secondary/5">
          {['7D', '30D', '90D', 'YTD'].map((range) => (
            <button key={range} className={cn(
              "px-4 py-2 text-[13px] font-semibold rounded-full transition-all",
              range === '90D' 
                ? "bg-[#e8def8] text-on-surface" 
                : "text-on-surface-variant hover:bg-black/5"
            )}>
              {range}
            </button>
          ))}
          <div className="w-[1px] h-5 bg-black/10 mx-1" />
          <button className="px-4 py-2 text-[13px] font-semibold text-on-surface-variant hover:bg-black/5 rounded-full flex items-center gap-1.5">
            <Calendar className="w-4 h-4" />
            Custom
          </button>
        </div>
      </div>

      {/* Stats Row */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard 
          icon={AlertTriangle} 
          label="Total Incidents" 
          value="142" 
          trend="-12%" 
          trendUp={false} 
        />
        <StatCard 
          icon={Timer} 
          label="Avg Response Time" 
          value="2m 45s" 
          trend="+8s" 
          trendUp={true} 
          isWarning
        />
        <StatCard 
          icon={ShieldCheck} 
          label="SOP Compliance" 
          value="96.4%" 
          trend="+2.1%" 
          trendUp={true} 
        />
        <StatCard 
          icon={Calendar} 
          label="Drills Conducted" 
          value="12" 
          subValue="/ 15 target" 
        />
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-12 gap-6">
        {/* Main Volume Chart */}
        <div className="col-span-12 lg:col-span-8 bg-surface-container-low rounded-[28px] p-7 flex flex-col h-[400px]">
          <div className="flex justify-between items-center mb-6">
            <h3 className="text-[20px] font-bold text-on-surface tracking-tight">Incident Volume</h3>
            <button className="text-on-surface-variant hover:text-on-surface p-2 rounded-full hover:bg-black/5 transition-colors">
              <MoreHorizontal className="w-5 h-5" />
            </button>
          </div>
          
          <div className="flex-1 min-h-0">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={VOLUME_DATA}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#dad8dc" />
                <XAxis 
                  dataKey="name" 
                  axisLine={false} 
                  tickLine={false} 
                  tick={{ fontSize: 12, fontWeight: 500, fill: '#49454f' }}
                  dy={10}
                />
                <YAxis 
                  axisLine={false} 
                  tickLine={false} 
                  tick={{ fontSize: 12, fontWeight: 500, fill: '#49454f' }}
                />
                <Tooltip 
                  cursor={{ fill: 'rgba(0,0,0,0.05)' }}
                  contentStyle={{ borderRadius: '16px', border: 'none', backgroundColor: '#fdfdfd', boxShadow: '0 4px 12px rgba(0,0,0,0.1)' }}
                />
                <Bar dataKey="fire" stackId="a" fill="#b3261e" radius={[2, 2, 0, 0]} barSize={40} />
                <Bar dataKey="security" stackId="a" fill="#625b71" radius={[0, 0, 0, 0]} barSize={40} />
                <Bar dataKey="medical" stackId="a" fill="#7d5260" radius={[4, 4, 0, 0]} barSize={40} />
              </BarChart>
            </ResponsiveContainer>
          </div>

          <div className="flex justify-center gap-8 mt-6 pt-5 border-t border-black/5">
             <LegendItem color="bg-error" label="Fire / Critical" />
             <LegendItem color="bg-secondary" label="Security" />
             <LegendItem color="bg-tertiary" label="Medical" />
          </div>
        </div>

        {/* Sidebar Analytics */}
        <div className="col-span-12 lg:col-span-4 flex flex-col gap-6">
          {/* Histogram */}
          <div className="bg-surface-container-low rounded-[28px] p-6 h-[180px] flex flex-col">
            <h3 className="text-[16px] font-bold text-on-surface tracking-tight mb-4">Response Time Dist.</h3>
            <div className="flex-1 flex items-end justify-between px-1 gap-1.5 border-b border-black/5 pb-1">
              {HISTOGRAM_DATA.map((item, i) => (
                <div 
                  key={i} 
                  className="w-full rounded-t-[4px] transition-all hover:opacity-80"
                  style={{ height: `${item.count}%`, backgroundColor: item.fill }}
                />
              ))}
            </div>
            <div className="flex justify-between text-[11px] font-semibold text-on-surface-variant mt-2 px-1">
              <span>&lt; 1m</span>
              <span>3m</span>
              <span>&gt; 5m</span>
            </div>
          </div>

          {/* Top Responders */}
          <div className="bg-surface-container-low rounded-[28px] p-6 flex-1">
            <h3 className="text-[16px] font-bold text-on-surface tracking-tight mb-5">Top Responders</h3>
            <div className="space-y-3">
               <ResponderItem init="JD" name="John Davies" role="Security Lead" count={42} color="bg-secondary-container" text="text-on-surface" />
               <ResponderItem init="SL" name="Sarah Lin" role="Medical Officer" count={38} color="bg-primary-container" text="text-on-surface" />
               <ResponderItem init="MR" name="Marcus Reed" role="Floor Warden" count={24} color="bg-surface-container-highest" text="text-on-surface" />
            </div>
          </div>
        </div>
      </div>

      {/* Bottom Insights Row */}
      <div className="grid grid-cols-12 gap-6">
        {/* Type Breakdown */}
        <div className="col-span-12 lg:col-span-4 bg-surface-container-low rounded-[28px] p-7">
          <h3 className="text-[20px] font-bold text-on-surface tracking-tight mb-6">Type Breakdown</h3>
          <div className="space-y-5">
             <BreakdownItem label="Unattended Baggage" value={42} color="bg-secondary" total={50} />
             <BreakdownItem label="Medical Emergency" value={28} color="bg-primary" total={50} />
             <BreakdownItem label="Access Control Breach" value={19} color="bg-secondary" total={50} />
             <BreakdownItem label="Fire Alarm (False)" value={14} color="bg-error" total={50} />
          </div>
        </div>

        {/* Heatmap Simulation */}
        <div className="col-span-12 lg:col-span-4 bg-surface-container-low rounded-[28px] p-7 flex flex-col relative overflow-hidden group">
          <div className="relative z-10">
            <h3 className="text-[20px] font-bold text-on-surface tracking-tight mb-1">Incident Heatmap</h3>
            <p className="text-[13px] text-on-surface-variant mb-6">Concentration by level</p>
          </div>
          
          <div className="flex-1 flex flex-col justify-center items-center">
            <div className="w-full max-w-[200px] flex flex-col gap-1.5">
               {['L5 - Roof', 'L4 - Exec', 'L3 - Office', 'L2 - Retail', 'L1 - Lobby', 'B1 - Parking'].map((floor, i) => {
                 const intensity = [5, 15, 30, 80, 100, 40][i];
                 return (
                   <div key={floor} className="h-8 bg-surface-container border border-black/5 flex items-center justify-between px-3 rounded-[8px] relative overflow-hidden group/floor cursor-pointer">
                      <span className="text-[12px] font-semibold text-on-surface-variant relative z-20">{floor}</span>
                      <div className="absolute left-0 top-0 bottom-0 bg-primary/20 transition-all duration-500 group-hover/floor:opacity-80" style={{ width: `${intensity}%` }} />
                      {intensity > 70 && <div className="absolute inset-0 bg-error/10 opacity-40 mix-blend-multiply" />}
                   </div>
                 );
               })}
            </div>
          </div>
          
          <div className="absolute -right-12 -bottom-12 w-48 h-48 bg-primary/5 rounded-full blur-3xl" />
        </div>

        {/* Recommendations */}
        <div className="col-span-12 lg:col-span-4 bg-surface-container-low rounded-[28px] p-7 flex flex-col relative overflow-hidden">
           <div className="flex items-center gap-3 mb-4">
             <div className="w-12 h-12 rounded-2xl bg-primary/10 flex items-center justify-center">
               <Lightbulb className="w-6 h-6 text-primary" />
             </div>
             <h3 className="text-[20px] font-bold text-on-surface tracking-tight">System Recommendations</h3>
           </div>
           
           <p className="text-[14px] text-on-surface-variant leading-[1.6] mb-6">
             Analysis of recent incident data indicates a recurring bottleneck in response times for Lobby-level security alerts during peak hours (08:00 - 10:00).
           </p>

           <div className="space-y-4 flex-1">
              <RecItem text="Deploy additional static guard at East Entrance during morning rush." />
              <RecItem text="Review false-alarm triggers on L2 Retail smoke detectors." />
           </div>

           <button className="mt-8 w-full py-3 bg-surface-container text-on-surface text-[14px] font-semibold rounded-full transition-all hover:bg-black/5 flex items-center justify-center gap-2 group">
              <FileText className="w-[18px] h-[18px] text-on-surface-variant" />
              Generate Full Report
              <ArrowRight className="w-[18px] h-[18px] translate-x-0 group-hover:translate-x-1 transition-transform" />
           </button>
        </div>
      </div>
    </div>
  );
}

function StatCard({ icon: Icon, label, value, trend, trendUp, isWarning, subValue }: any) {
  return (
    <div className="bg-surface-container-low rounded-[28px] p-6 flex flex-col gap-5">
      <div className="flex items-start justify-between">
        <div className={cn(
          "w-12 h-12 rounded-[16px] flex items-center justify-center",
          isWarning ? "bg-error-container text-on-error-container" : "bg-primary-container text-on-primary-container"
        )}>
          <Icon className="w-6 h-6" />
        </div>
        {trend && (
          <div className={cn(
            "px-2.5 py-1 rounded-full text-[12px] font-semibold flex items-center gap-1",
            trendUp ? "bg-[#c4eed0] text-[#0f5223]" : "bg-error-container text-on-error-container"
          )}>
            {trendUp ? <TrendingUp className="w-3.5 h-3.5" /> : <TrendingDown className="w-3.5 h-3.5" />}
            {trend}
          </div>
        )}
      </div>
      <div>
        <h3 className="text-[14px] font-medium text-on-surface-variant mb-1">{label}</h3>
        <div className="flex items-baseline gap-2">
          <span className="text-[32px] font-bold text-on-surface leading-none">{value}</span>
          {subValue && <span className="text-[13px] font-medium text-on-surface-variant">{subValue}</span>}
        </div>
      </div>
    </div>
  );
}

function LegendItem({ color, label }: any) {
  return (
    <div className="flex items-center gap-2">
      <div className={cn("w-3 h-3 rounded-[4px]", color)} />
      <span className="text-[13px] font-medium text-on-surface-variant">{label}</span>
    </div>
  );
}

function ResponderItem({ init, name, role, count, color, text }: any) {
  return (
    <div className="flex items-center gap-4 group p-2 hover:bg-black/5 rounded-[20px] transition-all cursor-pointer">
      <div className={cn("w-11 h-11 rounded-[16px] flex items-center justify-center text-[14px] font-bold", color, text)}>
        {init}
      </div>
      <div className="flex-1 min-w-0">
        <h4 className="text-[14px] font-bold text-on-surface truncate leading-tight">{name}</h4>
        <p className="text-[12px] text-on-surface-variant mt-0.5">{role}</p>
      </div>
      <div className="text-right">
        <div className="text-[15px] font-bold text-on-surface leading-tight">{count}</div>
        <div className="text-[10px] font-semibold text-on-surface-variant uppercase tracking-wider">incidents</div>
      </div>
    </div>
  );
}

function BreakdownItem({ label, value, color, total }: any) {
  return (
    <div className="space-y-2">
      <div className="flex justify-between text-[13px] font-semibold">
        <span className="text-on-surface">{label}</span>
        <span className="text-on-surface-variant">{value}</span>
      </div>
      <div className="w-full h-2.5 bg-surface-container-highest rounded-full overflow-hidden">
        <motion.div 
          initial={{ width: 0 }}
          animate={{ width: `${(value / total) * 100}%` }}
          className={cn("h-full rounded-full", color)} 
        />
      </div>
    </div>
  );
}

function RecItem({ text }: any) {
  return (
    <div className="flex gap-3 items-start group">
      <div className="w-6 h-6 rounded-full bg-primary/10 flex items-center justify-center mt-0.5 group-hover:scale-110 transition-transform shrink-0">
        <ArrowRight className="w-3.5 h-3.5 text-primary" />
      </div>
      <span className="text-[14px] text-on-surface font-medium leading-[1.6]">{text}</span>
    </div>
  );
}
