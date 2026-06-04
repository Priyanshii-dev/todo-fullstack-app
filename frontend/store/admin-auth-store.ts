import { create } from "zustand";
import { persist } from "zustand/middleware";

interface AdminUser {
  id: number;
  email: string;
  role: string;
  status: string;
}

interface AdminAuthState {
  accessToken: string | null;
  admin: AdminUser | null;
  isBusy: boolean;
  message: string;
  setMessage: (msg: string) => void;
  login: (email: string, password: string) => Promise<boolean>;
  logout: () => void;
}

const API = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";

export const useAdminAuthStore = create<AdminAuthState>()(
  persist(
    (set) => ({
      accessToken: null,
      admin: null,
      isBusy: false,
      message: "",

      setMessage: (msg) => set({ message: msg }),

      login: async (email, password) => {
        set({ isBusy: true, message: "" });
        try {
          const res = await fetch(`${API}/api/auth/login/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password }),
          });
          const data = await res.json();

          if (!res.ok) {
            const msg =
              data?.non_field_errors?.[0] ||
              data?.message ||
              "Invalid credentials.";
            set({ message: msg, isBusy: false });
            return false;
          }

          const user: AdminUser = data.data.user;

          if (user.role !== "admin") {
            set({ message: "Access denied. Admins only.", isBusy: false });
            return false;
          }

          set({
            accessToken: data.data.token,
            admin: user,
            isBusy: false,
          });

          // set cookie for middleware
          document.cookie = `adminToken=${data.data.token}; path=/`;
          return true;
        } catch {
          set({ message: "Could not reach server.", isBusy: false });
          return false;
        }
      },

      logout: () => {
        document.cookie = "adminToken=; path=/; max-age=0";
        set({ accessToken: null, admin: null });
      },
    }),
    { name: "admin-auth" }
  )
);