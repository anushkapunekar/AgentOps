import { cn } from "@/lib/utils";

export function Button({ children, className, ...props }) {
  return (
    <button
      className={cn(
        "px-5 py-2.5 rounded-xl bg-white/10 backdrop-blur-xl border border-white/20 text-white hover:bg-white/20 transition font-medium shadow-sm",
        className
      )}
      {...props}
    >
      {children}
    </button>
  );
}
