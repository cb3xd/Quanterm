import { Button } from "./components/ui/button";
import {
  Card,
  CardDescription,
  CardFooter,
  CardTitle,
} from "./components/ui/card";

function HomePage() {
  return (
    <Card>
      <CardTitle>Macro View</CardTitle>
      <CardDescription>
        Welcome to Quanterm! This is the Macro View page, select a view to
        expand.
      </CardDescription>
      <CardFooter className="flex gap-1">
        <Button variant="outline" size="sm" className="w-1/3">
          View 1
        </Button>
        <Button variant="outline" size="sm" className="w-1/3">
          View 2
        </Button>
        <Button variant="outline" size="sm" className="w-1/3">
          View 3
        </Button>
      </CardFooter>
    </Card>
  );
}

export default HomePage;
