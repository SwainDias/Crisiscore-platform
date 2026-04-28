import React from 'react';
import { motion } from 'motion/react';
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, 
  LineChart, Line, Cell, PieChart, Pie
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
  { time: '< 1m', count: 10, fill: '#ebe7e9' },
  { time: '1-2m', count: 25, fill: '#ebe7e9' },
  { time: '2-3m', count: 60, fill: '#cbbeff' },
  { time: '3-4m', count: 85, fill: '#4c22bd' },
  { time: '4-5m', count: 45, fill: '#cbbeff' },
  { time: '5-6m', count: 20, fill: '#ebe7e9' },
  { time: '6m+', count: 5, fill: '#ba1a1a' },
];

export default function IncidentHistory() {
  return (
    <div className="space-y-8 pb-12">
      {/* Page Header */}
      <div className="flex justify-between items-end">
        <div>
          <h2 className="text-4xl font-sans font-bold tracking-tight text-on-surface mb-2">Incident History & Analytics</h2>
          <p className="text-on-surface-variant font-medium">Review historical response data, compliance metrics, and operational trends.</p>
        </div>
        
        <div className="glass rounded-full p-1.5 flex gap-2 border border-secondary/10 shadow-lg">
          {['7D', '30D', '90D', 'YTD'].map((range) => (
            <button key={range} className={cn(
              "px-4 py-1.5 text-xs font-bold rounded-full transition-all",
              range === '90D' 
                ? "bg-surface-container-highest text-on-surface shadow-sm" 
                : "text-on-surface-variant hover:text-on-surface"
            )}>
              {range}
            </button>
          ))}
          <div className="w-[1px] h-4 bg-secondary/10 mx-1 mt-1.5" />
          <button className="px-3 py-1.5 text-xs font-bold text-on-surface-variant hover:text-on-surface flex items-center gap-1.5">
            <Calendar className="w-3.5 h-3.5" />
            Custom
          </button>
        </div>
      </div>

      {/* Stats Row */}
      <div className="grid grid-cols-4 gap-6">
        <StatCard 
          icon={AlertTriangle} 
          label="Total Incidents" 
          value="142" 
          trend="-12%" 
          trendUp={false} 
          bgIcon="list"
        />
        <StatCard 
          icon={Timer} 
          label="Avg Response Time" 
          value="2m 45s" 
          trend="+8s" 
          trendUp={true} 
          bgIcon="timer"
          isWarning
        />
        <StatCard 
          icon={ShieldCheck} 
          label="SOP Compliance" 
          value="96.4%" 
          trend="+2.1%" 
          trendUp={true} 
          bgIcon="award"
        />
        <StatCard 
          icon={Calendar} 
          label="Drills Conducted" 
          value="12" 
          subValue="/ 15 target" 
          bgIcon="calendar"
        />
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-12 gap-6">
        {/* Main Volume Chart */}
        <div className="col-span-8 bg-surface-container-lowest rounded-3xl p-8 shadow-sm border border-secondary/5 flex flex-col h-[400px]">
          <div className="flex justify-between items-center mb-8">
            <h3 className="text-lg font-bold text-on-surface tracking-tight">Incident Volume</h3>
            <button className="text-on-surface-variant hover:text-on-surface p-1.5 rounded-full hover:bg-surface-container transition-colors">
              <MoreHorizontal className="w-5 h-5" />
            </button>
          </div>
          
          <div className="flex-1 min-h-0">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={VOLUME_DATA}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1edef" />
                <XAxis 
                  dataKey="name" 
                  axisLine={false} 
                  tickLine={false} 
                  tick={{ fontSize: 11, fontWeight: 700, fill: '#484554' }}
                  dy={10}
                />
                <YAxis 
                  axisLine={false} 
                  tickLine={false} 
                  tick={{ fontSize: 11, fontWeight: 700, fill: '#484554' }}
                />
                <Tooltip 
                  cursor={{ fill: 'transparent' }}
                  contentStyle={{ borderRadius: '16px', border: 'none', boxShadow: '0 10px 40px rgba(0,0,0,0.1)' }}
                />
                <Bar dataKey="fire" stackId="a" fill="#ba1a1a" radius={[2, 2, 0, 0]} barSize={40} />
                <Bar dataKey="security" stackId="a" fill="#5d5c73" radius={[0, 0, 0, 0]} barSize={40} />
                <Bar dataKey="medical" stackId="a" fill="#4a464b" radius={[4, 4, 0, 0]} barSize={40} />
              </BarChart>
            </ResponsiveContainer>
          </div>

          <div className="flex justify-center gap-8 mt-6 pt-4 border-t border-secondary/5">
             <LegendItem color="bg-error" label="Fire / Critical" />
             <LegendItem color="bg-secondary" label="Security" />
             <LegendItem color="bg-tertiary" label="Medical" />
          </div>
        </div>

        {/* Sidebar Analytics */}
        <div className="col-span-4 flex flex-col gap-6">
          {/* Histogram */}
          <div className="bg-surface-container-lowest rounded-3xl p-6 shadow-sm border border-secondary/5 h-[180px]">
            <h3 className="text-sm font-bold text-on-surface tracking-tight mb-4">Response Time Dist.</h3>
            <div className="h-24 flex items-end justify-between px-1 gap-1.5 border-b border-surface-container-high pb-1">
              {HISTOGRAM_DATA.map((item, i) => (
                <div 
                  key={i} 
                  className="w-full rounded-t-sm transition-all hover:opacity-80"
                  style={{ height: `${item.count}%`, backgroundColor: item.fill }}
                />
              ))}
            </div>
            <div className="flex justify-between text-[10px] font-bold text-on-surface-variant mt-1.5 px-0.5">
              <span>&lt; 1m</span>
              <span>3m</span>
              <span>&gt; 5m</span>
            </div>
          </div>

          {/* Top Responders */}
          <div className="bg-surface-container-lowest rounded-3xl p-6 shadow-sm border border-secondary/5 flex-1">
            <h3 className="text-sm font-bold text-on-surface tracking-tight mb-5">Top Responders</h3>
            <div className="space-y-4">
               <ResponderItem init="JD" name="John Davies" role="Security Lead" count={42} color="bg-secondary-container" text="text-on-secondary-container" />
               <ResponderItem init="SL" name="Sarah Lin" role="Medical Officer" count={38} color="bg-primary-container" text="text-on-primary-container" />
               <ResponderItem init="MR" name="Marcus Reed" role="Floor Warden" count={24} color="bg-surface-container-highest" text="text-on-surface" />
            </div>
          </div>
        </div>
      </div>

      {/* Bottom Insights Row */}
      <div className="grid grid-cols-12 gap-6">
        {/* Type Breakdown */}
        <div className="col-span-4 bg-surface-container-lowest rounded-3xl p-8 shadow-sm border border-secondary/5">
          <h3 className="text-lg font-bold text-on-surface tracking-tight mb-6">Type Breakdown</h3>
          <div className="space-y-5">
             <BreakdownItem label="Unattended Baggage" value={42} count={42} color="bg-secondary" total={50} />
             <BreakdownItem label="Medical Emergency" value={28} count={28} color="bg-primary" total={50} />
             <BreakdownItem label="Access Control Breach" value={19} count={19} color="bg-secondary" total={50} />
             <BreakdownItem label="Fire Alarm (False)" value={14} count={14} color="bg-error" total={50} />
          </div>
        </div>

        {/* Heatmap Simulation */}
        <div className="col-span-4 bg-surface-container-lowest rounded-3xl p-8 shadow-sm border border-secondary/5 flex flex-col relative overflow-hidden group">
          <div className="relative z-10">
            <h3 className="text-lg font-bold text-on-surface tracking-tight mb-1">Incident Heatmap</h3>
            <p className="text-xs text-on-surface-variant font-medium mb-8">Concentration by level</p>
          </div>
          
          <div className="flex-1 flex flex-col justify-center items-center">
            <div className="w-48 flex flex-col gap-1.5">
               {['L5 - Roof', 'L4 - Exec', 'L3 - Office', 'L2 - Retail', 'L1 - Lobby', 'B1 - Parking'].map((floor, i) => {
                 const intensity = [5, 15, 30, 80, 100, 40][i];
                 return (
                   <div key={floor} className="h-8 bg-surface-container-low border border-secondary/5 flex items-center justify-between px-3 relative group/floor cursor-pointer">
                      <span className="text-[10px] font-bold text-on-surface-variant relative z-20">{floor}</span>
                      <div className="absolute right-0 top-0 bottom-0 bg-primary/20 transition-all duration-500 group-hover/floor:opacity-80" style={{ width: `${intensity}%` }} />
                      {intensity > 70 && <div className="absolute inset-0 bg-error/10 opacity-40 mix-blend-multiply" />}
                   </div>
                 );
               })}
            </div>
          </div>
          
          <div className="absolute -right-12 -bottom-12 w-48 h-48 bg-primary/5 rounded-full blur-3xl" />
        </div>

        {/* Recommendations */}
        <div className="col-span-4 bg-surface-container-lowest rounded-3xl p-8 shadow-sm border-l-8 border-primary flex flex-col relative overflow-hidden">
           <div className="flex items-center gap-3 mb-4">
             <div className="w-10 h-10 rounded-2xl bg-primary/10 flex items-center justify-center">
               <Lightbulb className="w-5 h-5 text-primary" />
             </div>
             <h3 className="text-lg font-bold text-on-surface tracking-tight">System Recommendations</h3>
           </div>
           
           <p className="text-sm text-on-surface-variant leading-relaxed mb-6 font-medium">
             Analysis of recent incident data indicates a recurring bottleneck in response times for Lobby-level security alerts during peak hours (08:00 - 10:00).
           </p>

           <div className="space-y-4 flex-1">
              <RecItem text="Deploy additional static guard at East Entrance during morning rush." />
              <RecItem text="Review false-alarm triggers on L2 Retail smoke detectors." />
           </div>

           <button className="mt-8 w-full py-3 bg-surface-container text-on-surface text-xs font-bold rounded-2xl transition-all hover:bg-surface-container-high flex items-center justify-center gap-2 group">
              <FileText className="w-4 h-4 text-on-surface-variant" />
              Generate Full Report
              <ArrowRight className="w-4 h-4 translate-x-0 group-hover:translate-x-1 transition-transform" />
           </button>
        </div>
      </div>
    </div>
  );
}

function StatCard({ icon: Icon, label, value, trend, trendUp, isWarning, subValue, bgIcon }: any) {
  return (
    <div className="bg-surface-container-lowest p-6 rounded-3xl shadow-sm border border-secondary/5 relative overflow-hidden group">
      <div className="absolute top-0 right-0 p-4 opacity-5 group-hover:opacity-10 transition-opacity">
        <Icon className="w-16 h-16" />
      </div>
      <div className="flex items-center gap-3 mb-4">
        <div className={cn(
          "w-8 h-8 rounded-xl bg-surface-container-low flex items-center justify-center",
          isWarning ? "text-error" : "text-primary"
        )}>
          <Icon className="w-4.5 h-4.5" />
        </div>
        <h3 className="text-[11px] font-bold text-on-surface-variant uppercase tracking-widest">{label}</h3>
      </div>
      <div className="flex items-baseline gap-2">
        <span className="text-3xl font-bold text-on-surface font-sans">{value}</span>
        {trend && (
          <span className={cn(
            "text-[10px] font-bold flex items-center",
            trendUp ? "text-primary" : "text-secondary"
          )}>
            {trendUp ? <TrendingUp className="w-3 h-3 mr-0.5" /> : <TrendingDown className="w-3 h-3 mr-0.5" />}
            {trend}
          </span>
        )}
        {subValue && <span className="text-[10px] font-bold text-on-surface-variant">{subValue}</span>}
      </div>
    </div>
  );
}

function LegendItem({ color, label }: any) {
  return (
    <div className="flex items-center gap-2">
      <div className={cn("w-2.5 h-2.5 rounded-sm", color)} />
      <span className="text-[11px] font-bold text-on-surface-variant">{label}</span>
    </div>
  );
}

function ResponderItem({ init, name, role, count, color, text }: any) {
  return (
    <div className="flex items-center gap-4 group p-1.5 hover:bg-surface-container/50 rounded-2xl transition-all cursor-pointer">
      <div className={cn("w-10 h-10 rounded-2xl flex items-center justify-center text-xs font-black shadow-sm", color, text)}>
        {init}
      </div>
      <div className="flex-1 min-w-0">
        <h4 className="text-xs font-bold text-on-surface truncate">{name}</h4>
        <p className="text-[10px] font-medium text-on-surface-variant">{role}</p>
      </div>
      <div className="text-right">
        <div className="text-xs font-bold text-on-surface">{count}</div>
        <div className="text-[9px] font-bold text-on-surface-variant uppercase tracking-tighter">incidents</div>
      </div>
    </div>
  );
}

function BreakdownItem({ label, value, color, total }: any) {
  return (
    <div className="space-y-2">
      <div className="flex justify-between text-xs font-bold">
        <span className="text-on-surface">{label}</span>
        <span className="text-on-surface-variant">{value}</span>
      </div>
      <div className="w-full h-2 bg-surface-container rounded-full overflow-hidden">
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
      <div className="w-5 h-5 rounded-full bg-primary/5 flex items-center justify-center mt-0.5 group-hover:scale-110 transition-transform">
        <ArrowRight className="w-3 h-3 text-primary" />
      </div>
      <span className="text-xs text-on-surface font-semibold leading-relaxed">{text}</span>
    </div>
  );
}
