import { useState } from "react";
import { DataPortal } from "./TabDataPortalContext.ts";
import type { TabContextValue } from "./TabDataPortalContext.ts";
import TabsUI from "./TabsUI.tsx";
type TabPageState = {
  page: string;
  tabName: string;
  data: Record<string, unknown>;
};

export default function TabContext() {
  const defaultTabId = crypto.randomUUID();
  const defaultPage: TabPageState = { page: "home", tabName: "Home", data: {} };

  const [activeTab, setActiveTab] = useState<string>(defaultTabId);
  const [tabs, setTabs] = useState<Record<string, TabPageState>>({
    [defaultTabId]: defaultPage,
  });

  const addTab = () => {
    const newTabId = crypto.randomUUID();
    setTabs((prev) => ({ ...prev, [newTabId]: defaultPage }));
    setActiveTab(newTabId);
  };

  const removeTab = (tabId: string) => {
    setTabs((prevTabs) => {
      const { [tabId]: _, ...rest } = prevTabs;
      console.log(_);
      return rest;
    });

    if (activeTab === tabId) {
      const remaining = Object.keys(tabs).filter((id) => id !== tabId);
      if (remaining.length > 0) {
        setActiveTab(remaining[0]);
      }
    }
  };

  const setTabData = (tabId: string, data: Record<string, unknown>) => {
    setTabs((prev) => ({
      ...prev,
      [tabId]: {
        ...prev[tabId],
        data,
        tabName: (data.tabName as string) || prev[tabId].tabName,
      },
    }));
  };

  const value: TabContextValue = {
    tabs,
    activeTab,
    addTab,
    removeTab,
    setActiveTab,
    setTabData,
  };

  return (
    <DataPortal.Provider value={value}>
      <TabsUI />
    </DataPortal.Provider>
  );
}
