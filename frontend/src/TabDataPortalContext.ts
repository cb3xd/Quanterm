import { createContext } from "react";

type TabPageState = {
  page: string;
  tabName: string;
  data: Record<string, unknown>;
};

export type TabContextValue = {
  tabs: Record<string, TabPageState>;
  activeTab: string;
  addTab: () => void;
  removeTab: (tabId: string) => void;
  setActiveTab: (tabId: string) => void;
  setTabData: (tabId: string, data: Record<string, unknown>) => void;
};

export const DataPortal = createContext<TabContextValue | undefined>(undefined);
