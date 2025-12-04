export function Card({ children, className }) {
  return (
    <div
      className={`glass rounded-2xl border border-white/10 shadow-lg p-6 ${className}`}
    >
      {children}
    </div>
  );
}
