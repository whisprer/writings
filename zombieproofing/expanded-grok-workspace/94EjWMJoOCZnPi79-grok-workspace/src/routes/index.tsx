import { createFileRoute } from "@tanstack/react-router";
import { Manual } from "@/components/Manual";

export const Route = createFileRoute("/")({ component: Home });

function Home() {
  return <Manual />;
}
