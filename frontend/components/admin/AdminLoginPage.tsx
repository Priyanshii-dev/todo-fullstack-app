"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useAdminAuthStore } from "@/store/admin-auth-store";

export default function AdminLoginPage() {
  const router = useRouter();
  const { login, isBusy, message, setMessage } = useAdminAuthStore();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setMessage("");
    const success = await login(email, password);
    if (success) router.replace("/admin/users");
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-app-bg dark:bg-app-bg-dark px-4">
      <div className="w-full max-w-sm rounded-xl border border-app-border bg-app-surface p-8 shadow-sm dark:border-app-border-dark dark:bg-app-surface-dark">

        <div className="mb-8">
          <p className="text-xs font-semibold uppercase tracking-widest text-app-muted dark:text-app-muted-dark">
            Master Admin
          </p>
          <h1 className="mt-1 text-2xl font-semibold text-app-text dark:text-app-text-dark">
            Sign in
          </h1>
        </div>

        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <div className="flex flex-col gap-1.5">
            <label className="text-sm font-medium text-app-text dark:text-app-text-dark">
              Email
            </label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="admin@example.com"
              required
              className="h-10 rounded-lg border border-app-border bg-app-hover px-3 text-sm text-app-text outline-none focus:border-app-primary dark:border-app-border-dark dark:bg-app-hover-dark dark:text-app-text-dark"
            />
          </div>

          <div className="flex flex-col gap-1.5">
            <label className="text-sm font-medium text-app-text dark:text-app-text-dark">
              Password
            </label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              required
              className="h-10 rounded-lg border border-app-border bg-app-hover px-3 text-sm text-app-text outline-none focus:border-app-primary dark:border-app-border-dark dark:bg-app-hover-dark dark:text-app-text-dark"
            />
          </div>

          {message && (
            <p className="text-sm text-red-500">{message}</p>
          )}

          <button
            type="submit"
            disabled={isBusy}
            className="mt-2 h-10 rounded-lg bg-app-primary text-sm font-semibold text-app-on-primary transition hover:opacity-90 disabled:opacity-50"
          >
            {isBusy ? "Signing in…" : "Sign in"}
          </button>
        </form>
      </div>
    </div>
  );
}