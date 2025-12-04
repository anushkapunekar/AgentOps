import "./globals.css";
import { Inter } from "next/font/google";

const inter = Inter({ subsets: ["latin"] });

export const metadata = {
  title: "AgentOps - AI Code Reviewer",
  description: "Automated AI-driven code review for GitLab",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className="dark">
  <body
    className={`${inter.className} bg-gradient min-h-screen text-white`}
  >
    <div className="fixed inset-0 bg-gradient"></div>

    <div className="relative z-10">
      {children}
    </div>
  </body>
</html>

  );
}
