import { Button } from "./components/ui/button";
import { Separator } from "./components/ui/separator";
import { Tabs, TabsList, TabsTrigger } from "./components/ui/tabs";
import { useState } from "react";
import { RiCloseLine, RiAddLine } from "@remixicon/react";

function App() {
  const [tabs, setTabs] = useState([]);
  const addTab = () => {
    const id = crypto.randomUUID();
    const newTab = {
      id,
      tabName: `New Tab`,
    };
    setTabs((prev) => [...prev, newTab]);
  };
  const removeTab = (id) => {
    setTabs((prev) => prev.filter((tab) => tab.id !== id));
  };
  return (
    <>
      <div className="flex">
        <Tabs defaultValue="tab1">
          <TabsList>
            {tabs.map((tab) => (
              <div className="flex items-center">
                <TabsTrigger value={tab.id}>{tab.tabName}</TabsTrigger>
                <Button
                  variant="ghost"
                  className="w-6 h-6 p-1"
                  onClick={() => removeTab(tab.id)}
                >
                  <RiCloseLine className="size-3" />
                </Button>
              </div>
            ))}
          </TabsList>
        </Tabs>
        <Button variant="ghost" onClick={addTab}>
          <RiAddLine className="size-3" />
        </Button>
      </div>
      <Separator />
    </>
  );
}

export default App;
