import { Button } from "./components/ui/button";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "./components/ui/tabs";
import { useState } from "react";
import { RiCloseLine, RiAddLine } from "@remixicon/react";
import HomePage from "./Home";

function App() {
  const [tabs, setTabs] = useState([{ id: "1", tabName: "Tab 1" }]);
  const [activeTab, setActiveTab] = useState("1");

  const addTab = () => {
    const id = crypto.randomUUID();
    const newTab = { id, tabName: `Tab ${tabs.length + 1}` };
    setTabs((prev) => [...prev, newTab]);
    setActiveTab(id);
  };

  const removeTab = (id) => {
    setTabs((prev) => prev.filter((tab) => tab.id !== id));
    if (activeTab === id) {
      setActiveTab(tabs[0]?.id || null);
    }
  };

  return (
    <>
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <div className="flex items-center">
          <TabsList className="flex gap-1">
            {tabs.map((tab) => (
              <div key={tab.id} className="flex items-center gap-1">
                <TabsTrigger value={tab.id}>{tab.tabName}</TabsTrigger>
                <Button
                  variant="ghost"
                  size="sm"
                  className="w-5 h-5"
                  onClick={() => removeTab(tab.id)}
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

        {/* Content INSIDE Tabs */}
        {tabs.map((tab) => (
          <TabsContent key={tab.id} value={tab.id}>
            <HomePage />
          </TabsContent>
        ))}
      </Tabs>
    </>
  );
}
export default App;
