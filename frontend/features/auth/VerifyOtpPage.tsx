"use client";

import { useRouter, useSearchParams } from "next/navigation";
import { useAuthStore } from "@/store/auth-store";
import { OtpFormValues } from "./types/auth.types";
import OtpForm from "@/components/auth/OtpForm";


const LOGIN_ROUTE = "/login";

export default function VerifyOtpPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const emailFromQuery = searchParams.get("email") ?? "";

  const { email: storeEmail, verifyOtp, resendOtp, isBusy, message } =
    useAuthStore();

  const email = emailFromQuery || storeEmail;

  async function handleVerify(values: OtpFormValues) {
    const success = await verifyOtp(email, values.code);
    if (success) {
      router.push(LOGIN_ROUTE);
    }
  }

  async function handleResend() {
    await resendOtp(email);
  }

  function handleBack() {
    router.push(LOGIN_ROUTE);
  }

  return (
    <OtpForm
      email={email}
      onSubmit={handleVerify}
      onResend={handleResend}
      onBack={handleBack}
      isBusy={isBusy}
      message={message}
    />
  );
}
