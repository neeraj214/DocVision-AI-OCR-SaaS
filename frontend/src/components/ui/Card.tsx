import React from "react";
import { cn } from "./Button";

export const Card: React.FC<React.HTMLAttributes<HTMLDivElement>> = ({
  className,
  ...props
}) => {
  return (
    <div
      className={cn(
        "bg-white/5 backdrop-blur-xl border border-white/10 rounded-xl shadow-2xl",
        className
      )}
      {...props}
    />
  );
};
