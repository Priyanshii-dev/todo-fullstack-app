"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useAdminAuthStore } from "@/store/admin-auth-store";

import { toast } from "sonner";
import { GlobalTable, GlobalTableColumn } from "@/global/global-table";
import { CustomPagination } from "@/global/global-pagination";

interface Employee {
  id: number;
  email: string;
  role: string;
  status: string;
}

type StatusFilter = "all" | "pending" | "approved" | "rejected";

const API = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";
const PAGE_SIZE = 10;

export default function AdminUsersPage() {
  const router = useRouter();
  const { accessToken, admin, logout } = useAdminAuthStore();

  const [users, setUsers]           = useState<Employee[]>([]);
  const [loading, setLoading]       = useState(true);
  const [filter, setFilter]         = useState<StatusFilter>("all");
  const [currentPage, setCurrentPage] = useState(1);
  const [busy, setBusy]             = useState<number | null>(null);

  useEffect(() => {
    if (!accessToken) { router.replace("/admin/login"); return; }
    fetchUsers();
  }, [accessToken]);

  async function fetchUsers() {
    setLoading(true);
    try {
      const url = filter === "all"
        ? `${API}/api/admin/users/`
        : `${API}/api/admin/users/?status=${filter}`;

      const res  = await fetch(url, {
        headers: { Authorization: `Bearer ${accessToken}` },
      });
      const data = await res.json();
      setUsers(data.data ?? []);
      setCurrentPage(1);
    } catch {
      toast.error("Failed to load users.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => { fetchUsers(); }, [filter]);

  async function updateStatus(id: number, status: "approved" | "rejected") {
    setBusy(id);
    try {
      const res = await fetch(`${API}/api/admin/users/${id}/`, {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${accessToken}`,
        },
        body: JSON.stringify({ status }),
      });

      if (!res.ok) { toast.error("Failed to update user."); return; }

      setUsers((prev) =>
        prev.map((u) => (u.id === id ? { ...u, status } : u))
      );
      toast.success(`User ${status} successfully.`);
    } catch {
      toast.error("Could not reach server.");
    } finally {
      setBusy(null);
    }
  }

  // paginate client-side
  const paginated = users.slice(
    (currentPage - 1) * PAGE_SIZE,
    currentPage * PAGE_SIZE
  );
  const totalPages = Math.ceil(users.length / PAGE_SIZE);

  const columns: GlobalTableColumn<Employee>[] = [
    {
      key: "email",
      header: "Email",
      render: (row) => (
        <span className="font-medium text-app-text dark:text-app-text-dark">
          {row.email}
        </span>
      ),
    },
    {
      key: "role",
      header: "Role",
      render: (row) => (
        <span className="text-app-muted dark:text-app-muted-dark capitalize">
          {row.role}
        </span>
      ),
    },
    {
      key: "status",
      header: "Status",
      render: (row) => <StatusBadge status={row.status} />,
    },
    {
      key: "actions",
      header: "Actions",
      render: (row) => (
        <div className="flex gap-2">
          <button
            onClick={() => updateStatus(row.id, "approved")}
            disabled={row.status === "approved" || busy === row.id}
            className="rounded-md bg-green-50 px-3 py-1.5 text-xs font-semibold text-green-700 transition hover:bg-green-100 disabled:cursor-not-allowed disabled:opacity-40 dark:bg-green-900/20 dark:text-green-400"
          >
            {busy === row.id ? "…" : "Approve"}
          </button>
          <button
            onClick={() => updateStatus(row.id, "rejected")}
            disabled={row.status === "approved" || busy === row.id}
            className="rounded-md bg-red-50 px-3 py-1.5 text-xs font-semibold text-red-700 transition hover:bg-red-100 disabled:cursor-not-allowed disabled:opacity-40 dark:bg-red-900/20 dark:text-red-400"
          >
            Reject
          </button>
        </div>
      ),
    },
  ];

  return (
    <div className="min-h-screen bg-app-bg dark:bg-app-bg-dark">
      <header className="border-b border-app-border bg-app-surface px-6 py-4 dark:border-app-border-dark dark:bg-app-surface-dark">
        <div className="mx-auto flex max-w-6xl items-center justify-between">
          <div>
            <p className="text-xs font-semibold uppercase tracking-widest text-app-muted dark:text-app-muted-dark">
              Master Admin
            </p>
            <h1 className="text-lg font-semibold text-app-text dark:text-app-text-dark">
              Employee Approvals
            </h1>
          </div>
          <div className="flex items-center gap-4">
            <span className="text-sm text-app-muted dark:text-app-muted-dark">
              {admin?.email}
            </span>
            <button
              onClick={() => { logout(); router.replace("/admin/login"); }}
              className="text-sm font-medium text-app-muted hover:text-app-text dark:text-app-muted-dark dark:hover:text-app-text-dark"
            >
              Sign out
            </button>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-6xl px-6 py-8">
        {/* stats */}
        <div className="mb-6 grid grid-cols-3 gap-4">
          {(["pending", "approved", "rejected"] as const).map((s) => (
            <div
              key={s}
              className="rounded-lg border border-app-border bg-app-surface p-4 dark:border-app-border-dark dark:bg-app-surface-dark"
            >
              <p className="text-xs font-semibold uppercase tracking-wide text-app-muted dark:text-app-muted-dark">
                {s}
              </p>
              <p className="mt-1 text-2xl font-semibold text-app-text dark:text-app-text-dark">
                {users.filter((u) => u.status === s).length}
              </p>
            </div>
          ))}
        </div>

        {/* filter tabs */}
        <div className="mb-4 flex gap-2">
          {(["all", "pending", "approved", "rejected"] as const).map((s) => (
            <button
              key={s}
              onClick={() => setFilter(s)}
              className={`rounded-md px-4 py-1.5 text-sm font-medium transition capitalize ${
                filter === s
                  ? "bg-app-primary text-app-on-primary"
                  : "bg-app-hover text-app-muted hover:text-app-text dark:bg-app-hover-dark dark:text-app-muted-dark"
              }`}
            >
              {s}
            </button>
          ))}
        </div>

        <GlobalTable
          data={paginated}
          columns={columns}
          getRowKey={(row) => row.id}
          loading={loading}
          emptyMessage="No users found."
        />

        {totalPages > 1 && (
          <CustomPagination
            currentPage={currentPage}
            totalPages={totalPages}
            onPageChange={setCurrentPage}
            itemsPerPage={PAGE_SIZE}
            totalItems={users.length}
          />
        )}
      </main>
    </div>
  );
}

function StatusBadge({ status }: { status: string }) {
  const styles: Record<string, string> = {
    pending:  "bg-yellow-50 text-yellow-700 dark:bg-yellow-900/20 dark:text-yellow-400",
    approved: "bg-green-50 text-green-700 dark:bg-green-900/20 dark:text-green-400",
    rejected: "bg-red-50 text-red-700 dark:bg-red-900/20 dark:text-red-400",
  };
  return (
    <span className={`rounded-full px-2.5 py-1 text-xs font-semibold capitalize ${styles[status] ?? ""}`}>
      {status}
    </span>
  );
}