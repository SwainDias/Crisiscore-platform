import React from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { Shield, Search, Clock, Bell, UserCircle, TriangleAlert } from 'lucide-react';
import { NAV_ITEMS } from '../types/constants';
import { cn } from '../lib/utils';

interface LayoutProps {
  children: React.ReactNode;
  activeId: string;
  onNavigate: (id: string) => void;
}

export default function Layout({ children, activeId, onNavigate }: LayoutProps) {
  return (
    <div className="flex min-h-screen bg-surface">
      {/* Sidebar */}
      <aside className="fixed left-0 top-0 h-screen w-64 bg-surface-container-low py-6 px-4 flex flex-col z-[60]">
        <div className="flex items-center gap-3 px-3 mb-8">
          <div className="w-10 h-10 rounded-xl bg-primary flex items-center justify-center text-on-primary">
            <Shield className="w-6 h-6 fill-current" />
          </div>
          <div>
            <h1 className="font-sans text-xl font-bold tracking-tighter text-on-surface leading-tight">CrisisCore Admin</h1>
            <p className="font-body text-[10px] uppercase font-bold tracking-widest text-on-surface-variant">Precision Command</p>
          </div>
        </div>

        <nav className="flex-1 space-y-1">
          {NAV_ITEMS.map((item) => {
            const Icon = item.icon;
            const isActive = activeId === item.id;
            return (
              <button
                key={item.id}
                onClick={() => onNavigate(item.id)}
                className={cn(
                  "w-full flex items-center gap-3 px-3 py-2 rounded-xl transition-all duration-200 group text-left",
                  isActive 
                    ? "bg-surface-container-lowest text-on-surface font-semibold shadow-sm"
                    : "text-on-surface-variant hover:bg-surface-container hover:text-on-surface font-medium"
                )}
              >
                <Icon className={cn("w-5 h-5", isActive ? "text-primary" : "group-hover:text-primary")} />
                <span className="text-sm tracking-tight">{item.label}</span>
              </button>
            );
          })}
        </nav>

        <div className="mt-auto border-t border-secondary/10 pt-4">
          <button className="w-full flex items-center gap-3 px-3 py-2 rounded-xl text-on-surface-variant hover:bg-surface-container hover:text-on-surface transition-all group text-left">
            <UserCircle className="w-5 h-5 group-hover:text-primary" />
            <span className="text-sm font-medium">Manager Profile</span>
          </button>
        </div>
      </aside>

      {/* Main Content Area */}
      <div className="flex-1 ml-64 flex flex-col">
        {/* Header */}
        <header className="fixed top-0 right-0 left-64 h-16 glass z-50 flex items-center justify-between px-8">
          <div className="flex items-center gap-6">
            <div className="relative w-64 hidden lg:block">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-on-surface-variant w-4 h-4" />
              <input 
                type="text" 
                placeholder="Search entities, staff..." 
                className="w-full bg-surface-container-high/50 text-on-surface text-sm rounded-xl pl-9 pr-4 py-1.5 focus:outline-none focus:ring-2 focus:ring-primary/20 transition-all font-body border-none"
              />
            </div>
            <div className="h-full items-center flex border-b-2 border-primary pt-1">
              <span className="text-on-surface font-semibold text-sm">Main Property</span>
            </div>
          </div>

          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2 px-3 py-1 bg-surface-container text-on-surface-variant rounded-full text-xs font-medium">
              <Clock className="w-3.5 h-3.5" />
              Property Time: 14:30
            </div>
            <button className="relative w-8 h-8 flex items-center justify-center rounded-full hover:bg-surface-container transition-colors">
              <Bell className="w-5 h-5 text-on-surface-variant" />
              <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-error rounded-full ring-2 ring-surface-container-lowest" />
            </button>
            <button className={cn(
              "signature-gradient text-on-primary px-4 py-1.5 rounded-full text-sm font-semibold flex items-center gap-2",
              "shadow-[0_4px_12px_rgba(76,34,189,0.3)] hover:shadow-[0_6px_20px_rgba(76,34,189,0.4)] active:scale-95 transition-all"
            )}>
              <TriangleAlert className="w-4 h-4" />
              Raise Alert
            </button>
            <div className="w-8 h-8 rounded-full bg-surface-container-high overflow-hidden border border-surface-variant ml-2">
               <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=Felix" alt="User" />
            </div>
          </div>
        </header>

        <main className={cn("flex-1 mt-16 min-h-[calc(100vh-4rem)] relative overflow-x-hidden", activeId === 'live-map' ? "p-0" : "p-8")}>
          <AnimatePresence mode="wait">
            <motion.div
              key={activeId}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              transition={{ duration: 0.3 }}
            >
              {children}
            </motion.div>
          </AnimatePresence>
        </main>
      </div>
    </div>
  );
}
