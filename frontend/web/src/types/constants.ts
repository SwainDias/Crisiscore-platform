import { Shield, LayoutDashboard, Map as MapIcon, Siren as Emergency, Users, IdCard, History, Footprints, BarChart3, Settings, UserCircle, Search, Bell, TriangleAlert, Clock, Plus, Phone, Mail, MoreVertical, MoreHorizontal, CheckCircle2, AlertTriangle, Info, BellRing as BellIcon, MoreHorizontalIcon, Fullscreen, CornerUpRight, Send, HelpCircle, ChevronRight, RotateCcw, Edit3, Archive, CheckSquare, Lightbulb, ArrowRight, FileText as SummarizeIcon, Upload, Download, Megaphone } from 'lucide-react';

export const NAV_ITEMS = [
  { id: 'overview', label: 'Overview', icon: LayoutDashboard },
  { id: 'live-map', label: 'Live Map', icon: MapIcon },
  { id: 'active-incidents', label: 'Active Incidents', icon: Emergency },
  { id: 'staff-directory', label: 'Staff Directory', icon: Users },
  { id: 'guest-registry', label: 'Guest Registry', icon: IdCard },
  { id: 'incident-history', label: 'Incident History', icon: History },
  { id: 'drill-management', label: 'Drill Management', icon: Footprints },
  { id: 'reports', label: 'Reports & Analytics', icon: BarChart3 },
  { id: 'settings', label: 'System Settings', icon: Settings },
];

export interface Incident {
  id: string;
  title: string;
  location: string;
  severity: 'P1' | 'P2' | 'P3';
  status: 'active' | 'resolved' | 'escalated';
  elapsedTime: string;
  responders: number;
  guestsUnaccounted: number;
}
