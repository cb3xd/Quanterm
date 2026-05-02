import { useState } from "react";
import Home from "./Home";

function TabSwitcher() {
  const [activeTab, setActiveTab] = useState(0);
  const tabs = [{ id: 0, label: "Home", content: <Home /> }];
  const addTab () => {
    
  }
  return (
    <div>
      <ul role="tablist" className="flex gap-4">
        {tabs.map((tab) => (
          <li key={tab.id}>
            <button
              onClick={() => setActiveTab(tab.id)}
              style={{ fontWeight: activeTab === tab.id ? "bold" : "normal" }}
            >
              {tab.label}
            </button>
          </li>
        ))}
        <button>+</button>
      </ul>
      <div className="tab-content">
        {tabs.find((t) => t.id === activeTab)?.content}
      </div>
    </div>
  );
}

export default TabSwitcher;
