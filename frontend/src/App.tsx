import { Button } from "./components/ui/button";
import { Separator } from "./components/ui/separator";
import { Tabs, TabsList, TabsTrigger } from "./components/ui/tabs";

function App() {
  return (
    <>
      <div className="flex">
        <Tabs defaultValue="tab1">
          <TabsList>
            <TabsTrigger value="tab1">New Tab 1</TabsTrigger>
            <TabsTrigger value="tab2">New Tab 2</TabsTrigger>
            <TabsTrigger value="tab3">New Tab 3</TabsTrigger>
            <TabsTrigger value="tab4">New Tab 4</TabsTrigger>
            <TabsTrigger value="tab5">New Tab 5</TabsTrigger>
          </TabsList>
        </Tabs>
        <Button variant="ghost">+</Button>
      </div>
      <Separator />
    </>
  );
}

export default App;
