import { useContext } from "react";
import { Button } from "./ui/button";
import { RiCloseLine, RiAddLine } from "@remixicon/react";
import HomePage from "@/views/Home";
import { DataPortal } from "@/context/TabDataPortalContext";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "./ui/tabs";
export default function TabsUI() {
  const context = useContext(DataPortal);

  if (!context) {
    throw new Error("TabsUI must be used within TabContext");
  }

  const { tabs, activeTab, setActiveTab, addTab, removeTab } = context;
  const tabList = Object.entries(tabs);

  return (
    <Tabs value={activeTab} onValueChange={setActiveTab}>
      <div className="flex items-center">
        <TabsList className="flex gap-1">
          {tabList.map(([tabId, tab]) => (
            <div key={tabId} className="flex items-center gap-1">
              <TabsTrigger value={tabId}>{tab.tabName}</TabsTrigger>
              <Button
                variant="ghost"
                size="sm"
                className="w-5 h-5"
                onClick={() => removeTab(tabId)}
              >
                <RiCloseLine className="size-3" />
              </Button>
            </div>
          ))}
        </TabsList>
        <Button variant="ghost" size="sm" onClick={addTab}>
          <RiAddLine className="size-3" />
        </Button>
      </div>
      {tabList.map(([tabId]) => (
        <TabsContent key={tabId} value={tabId}>
          <HomePage />
        </TabsContent>
      ))}
    </Tabs>
  );
}
