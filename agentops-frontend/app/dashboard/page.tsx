export default function DashboardPage() {
    return (
      <div className="p-10">
        <h1 className="text-3xl font-bold">Dashboard</h1>
        <p className="text-muted-foreground">Your GitLab Code Review Activity</p>
  
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-6">
          <div className="p-6 border rounded-xl shadow-sm">
            <h2 className="text-xl font-semibold">Repositories</h2>
            <p className="text-sm text-muted-foreground">Coming soon…</p>
          </div>
          <div className="p-6 border rounded-xl shadow-sm">
            <h2 className="text-xl font-semibold">Recent Reviews</h2>
            <p className="text-sm text-muted-foreground">Coming soon…</p>
          </div>
        </div>
      </div>
    );
  }
  