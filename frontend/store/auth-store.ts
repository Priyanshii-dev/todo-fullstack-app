"use client";

import { create } from "zustand";
import { persist } from "zustand/middleware";
import { toast } from "sonner";
import { API_ENDPOINTS } from "../api/endpoints";
import { mapTokenPair } from "../api/mappers";
import { request } from "../lib/api";
import { clearTokens, saveTokens } from "../lib/auth";
import { AuthResponse } from "../types";

type AuthCredentials = {
  email: string;
  password: string;
};

interface AuthState {
  email: string;
  password: string;

  accessToken: string | null;
  refreshToken: string | null;

  isBusy: boolean;
  message: string;

  setEmail: (value: string) => void;
  setPassword: (value: string) => void;
  setMessage: (message: string) => void;

  login: (credentials?: AuthCredentials) => Promise<boolean>;
  register: (credentials?: AuthCredentials) => Promise<boolean>;
  verifyOtp: (email: string, code: string) => Promise<boolean>;
  resendOtp: (email: string) => Promise<boolean>;

  logout: () => void;
  clearAuth: () => void;

  clearMessage: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      email: "",
      password: "",
      accessToken: null,
      refreshToken: null,

      isBusy: false,
      message: "",

      setEmail: (value) => set({ email: value }),

      setPassword: (value) => set({ password: value }),

      setMessage: (message) => set({ message }),

      login: async (credentials) => {
        set({
          isBusy: true,
          message: "",
        });

        try {
          const payload = credentials ?? {
            email: get().email,
            password: get().password,
          };

          const response = await request<AuthResponse>(
            API_ENDPOINTS.auth.login,
            {
              method: "POST",
              body: JSON.stringify(payload),
            },
          );

          const tokens = mapTokenPair(response);
          const actualEmail = response.user?.email ?? payload.email;
          saveTokens(tokens.access, tokens.refresh);

          set({
            accessToken: tokens.access,
            refreshToken: tokens.refresh,
            password: "",
            email: actualEmail,
            message: "Login successful",
          });
          toast.success("Login successful");

          return true;
        } catch (error) {
          const message =
            error instanceof Error
              ? error.message
              : "Unable to login";

          set({
            message,
          });
          toast.error(message);

          return false;
        } finally {
          set({ isBusy: false });
        }
      },

      register: async (credentials) => {
        set({
          isBusy: true,
          message: "",
        });

        try {
          const payload = credentials ?? {
            email: get().email,
            password: get().password,
          };

          await request<null>(
            API_ENDPOINTS.auth.register,
            {
              method: "POST",
              body: JSON.stringify(payload),
            },
          );

          set({
            email: payload.email,
            message: "Registration successful. Please check your email for the OTP.",
            password: "",
          });
          toast.success("Registration successful! Check your email for the verification code.");

          return true;
        } catch (error) {
          const message =
            error instanceof Error
              ? error.message
              : "Unable to register";

          set({
            message,
          });
          toast.error(message);

          return false;
        } finally {
          set({ isBusy: false });
        }
      },

      verifyOtp: async (email, code) => {
        set({ isBusy: true, message: "" });

        try {
          await request<null>(
            API_ENDPOINTS.auth.verifyOtp,
            {
              method: "POST",
              body: JSON.stringify({ email, code }),
            },
          );

          set({ message: "Email verified successfully." });
          toast.success("Email verified! You can now log in.");

          return true;
        } catch (error) {
          const message =
            error instanceof Error
              ? error.message
              : "Unable to verify OTP";

          set({ message });
          toast.error(message);

          return false;
        } finally {
          set({ isBusy: false });
        }
      },

      resendOtp: async (email) => {
        set({ isBusy: true, message: "" });

        try {
          await request<null>(
            API_ENDPOINTS.auth.resendOtp,
            {
              method: "POST",
              body: JSON.stringify({ email }),
            },
          );

          set({ message: "A new OTP has been sent to your email." });
          toast.success("New OTP sent! Check your email.");

          return true;
        } catch (error) {
          const message =
            error instanceof Error
              ? error.message
              : "Unable to resend OTP";

          set({ message });
          toast.error(message);

          return false;
        } finally {
          set({ isBusy: false });
        }
      },

      logout: () => {
        clearTokens();

        set({
          accessToken: null,
          refreshToken: null,
          email: "",
          password: "",

          message: "Logged out successfully",
        });
        toast.success("Logged out successfully");
      },

      clearAuth: () => {
        clearTokens();

        set({
          accessToken: null,
          refreshToken: null,
          email: "",
          password: "",
          message: "",
        });
      },

      clearMessage: () => {
        set({ message: "" });
      },
    }),
    {
      name: "auth-storage",
      version: 3,

      partialize: (state) => ({
        accessToken: state.accessToken,
        refreshToken: state.refreshToken,
        email: state.email,
      }),
      migrate: (persistedState) => {
        const state = persistedState as
          | (Partial<AuthState> & { username?: string; loggedInUsername?: string })
          | undefined;

        return {
          accessToken: state?.accessToken ?? null,
          refreshToken: state?.refreshToken ?? null,
          email: state?.email ?? state?.username ?? state?.loggedInUsername ?? "",
          password: "",
          isBusy: false,
          message: "",
        };
      },
    },
  ),
);
