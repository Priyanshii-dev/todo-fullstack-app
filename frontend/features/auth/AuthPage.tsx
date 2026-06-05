"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { AuthFormValues, AuthMode, AuthPageProps } from "./types/auth.types";
import { useAuthStore } from "@/store/auth-store";
import { authSchema } from "@/lib/schemas";
import AuthForm from "@/components/auth/AuthForm";
import { toast } from "sonner";
import { requestNotificationPermission } from "@/lib/notification";

const LOGIN_ROUTE = "/login";
const REGISTER_ROUTE = "/register";
const TASKS_ROUTE = "/tasks";

export default function AuthPage({ mode }: AuthPageProps) {
  const router = useRouter();
  const {
    email,
    login,
    register,
    isBusy,
    message,
    setMessage,
    accessToken,
    clearAuth,
  } = useAuthStore();

  useEffect(() => {
    if (!accessToken) {
      return;
    }

    const hasAuthCookie = document.cookie
      .split("; ")
      .some((cookie) => cookie.startsWith("accessToken="));

    if (hasAuthCookie) {
      router.replace(TASKS_ROUTE);
      return;
    }

    clearAuth();
  }, [accessToken, clearAuth, router]);

  function handleModeChange(nextMode: AuthMode) {
    router.push(nextMode === "login" ? LOGIN_ROUTE : REGISTER_ROUTE);
  }

  async function handleSubmit(values: AuthFormValues) {
    setMessage("");

    const validation = authSchema.safeParse(values);

    if (!validation.success) {
      const message = validation.error.issues
        .map((issue) => issue.message)
        .join(" ");

      setMessage(message);
      toast.error(message);
      return;
    }

    const success =
      mode === "login"
        ? await login(validation.data)
        : await register(validation.data);

    if (success) {
  try {
    const fcmToken =
      await requestNotificationPermission();

    console.log("FCM Token:", fcmToken);

    // Later we'll send this token to Django
  } catch (error) {
    console.error(error);
  }

  router.push(TASKS_ROUTE);
}
  }

  return (
    <div className="mx-auto w-full max-w-md">
      <AuthForm
        mode={mode}
        onModeChange={handleModeChange}
        defaultValues={{ email }}
        onSubmit={handleSubmit}
        isBusy={isBusy}
        message={message}
      />
    </div>
  );
}
