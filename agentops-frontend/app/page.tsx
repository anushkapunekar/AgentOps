import { Button } from "@/components/ui/button";

export default function HomePage() {
  return (
    <main className="flex flex-col items-center justify-center h-screen text-center px-4">
      <h1 className="text-5xl font-bold mb-4">AgentOps — GitLab Code Reviewer</h1>
      <p className="text-lg text-muted-foreground max-w-xl">
        Automate your GitLab Merge Request reviews with AI-powered pipelines.
      </p>
      <Button className="mt-6" asChild>
        <a href="/connect">Get Started</a>
      </Button>
    </main>
  );
}
