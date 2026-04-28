/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState } from 'react';
import Layout from './components/Layout';
import Overview from './components/Overview';
import LiveMap from './components/LiveMap';
import IncidentHistory from './components/IncidentHistory';
import ActiveIncidentDetail from './components/ActiveIncidentDetail';
import StaffDirectory from './components/StaffDirectory';
import SystemSettings from './components/SystemSettings';
import DrillManagement from './components/DrillManagement';

export default function App() {
  const [activeId, setActiveId] = useState('live-map');

  const renderContent = () => {
    switch (activeId) {
      case 'overview':
        return <Overview />;
      case 'live-map':
        return <LiveMap />;
      case 'incident-history':
        return <IncidentHistory />;
      case 'active-incidents':
        return <ActiveIncidentDetail onBack={() => setActiveId('overview')} />;
      case 'staff-directory':
        return <StaffDirectory />;
      case 'settings':
        return <SystemSettings />;
      case 'drill-management':
        return <DrillManagement />;
      default:
        return (
          <div className="flex flex-col items-center justify-center min-h-[60vh] space-y-4">
             <div className="w-20 h-20 rounded-full bg-surface-container flex items-center justify-center">
               <span className="text-4xl text-on-surface-variant font-bold opacity-20">?</span>
             </div>
             <div className="text-center">
                <h3 className="text-xl font-bold text-on-surface">Module Under Construction</h3>
                <p className="text-on-surface-variant font-medium">This section of the ResQ Admin command center is currently being synchronized.</p>
             </div>
          </div>
        );
    }
  };

  return (
    <Layout activeId={activeId} onNavigate={setActiveId}>
      {renderContent()}
    </Layout>
  );
}
