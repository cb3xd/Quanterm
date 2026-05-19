import { useTabData } from "@/hooks/useTabData";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardTitle,
  CardDescription,
  CardFooter,
} from "@/components/ui/card";
function HomePage() {
  const [data, updateData] = useTabData();
  const activeView = data.view as number | undefined;

  const handleViewClick = (view: number) => {
    updateData({ ...data, view, tabName: `View ${view}` });
  };

  return (
    <Card>
      <CardTitle>Macro View</CardTitle>
      <CardDescription>
        Welcome to Quanterm! This is the Macro View page, select a view to
        expand.
      </CardDescription>
      <CardFooter className="flex gap-1">
        <Button
          variant={activeView === 1 ? "default" : "outline"}
          size="sm"
          className={`w-1/3 ${activeView === 1 ? "bg-green-500 hover:bg-green-600" : ""}`}
          onClick={() => handleViewClick(1)}
        >
          View 1
        </Button>
        <Button
          variant={activeView === 2 ? "default" : "outline"}
          size="sm"
          className={`w-1/3 ${activeView === 2 ? "bg-green-500 hover:bg-green-600" : ""}`}
          onClick={() => handleViewClick(2)}
        >
          View 2
        </Button>
        <Button
          variant={activeView === 3 ? "default" : "outline"}
          size="sm"
          className={`w-1/3 ${activeView === 3 ? "bg-green-500 hover:bg-green-600" : ""}`}
          onClick={() => handleViewClick(3)}
        >
          View 3
        </Button>
      </CardFooter>
    </Card>
  );
}
export default HomePage;
