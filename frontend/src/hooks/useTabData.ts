import { useContext } from "react";
import { DataPortal } from "@/context/TabDataPortalContext";
export function useTabData() {
  const context = useContext(DataPortal);

  if (!context) {
    throw new Error("useTabData must be used within TabContext");
  }

  const { tabs, activeTab, setTabData } = context;
  const currentTabData = tabs[activeTab].data;

  const updateTabData = (newData: Record<string, unknown>) => {
    setTabData(activeTab, newData);
  };

  return [currentTabData, updateTabData] as const;
}
