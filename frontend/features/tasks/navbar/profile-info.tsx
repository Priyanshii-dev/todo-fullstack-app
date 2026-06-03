"use client";

import { User } from "lucide-react";
import { useAuthStore } from "@/store/auth-store";

export function ProfileInfo() {
  const displayName = useAuthStore((state) => state.email || "User");
  const initial = displayName.charAt(0).toUpperCase();

  return (
    <div className="flex min-w-0 items-center gap-3">
      <div className="flex size-10 items-center justify-center rounded-full bg-app-inverse text-sm font-bold text-app-on-inverse dark:bg-app-surface dark:text-app-text">
        {initial || <User className="size-4" />}
      </div>
      <div className="hidden min-w-0 leading-tight sm:block">
        <p className="truncate text-sm font-semibold text-app-text dark:text-app-text-dark">
          {displayName}
        </p>
        <p className="text-xs text-app-muted dark:text-app-muted-dark">
          Task workspace
        </p>
      </div>
    </div>
  );
}
