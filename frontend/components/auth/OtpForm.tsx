"use client";

import { useState } from "react";
import { Controller, useForm } from "react-hook-form";
import { GlobalButton } from "@/global/button";
import { GlobalForm, GlobalFormMessage } from "@/global/form";
import { GlobalInput } from "@/global/input";
import { OtpFormProps, OtpFormValues } from "@/features/auth/types/auth.types";

export default function OtpForm({
  email,
  onSubmit,
  onResend,
  onBack,
  isBusy,
  message,
}: OtpFormProps) {
  const [resendDisabled, setResendDisabled] = useState(false);
  const [countdown, setCountdown] = useState(0);

  const {
    control,
    handleSubmit,
    formState: { errors },
  } = useForm<OtpFormValues>({
    defaultValues: { code: "" },
  });

  async function handleResend() {
    setResendDisabled(true);
    setCountdown(30);

    await onResend();

    const timer = setInterval(() => {
      setCountdown((prev) => {
        if (prev <= 1) {
          clearInterval(timer);
          setResendDisabled(false);
          return 0;
        }
        return prev - 1;
      });
    }, 1000);
  }

  return (
    <GlobalForm
      onSubmit={handleSubmit(onSubmit)}
      className="rounded-lg border border-app-border bg-app-surface p-4 shadow-sm dark:border-app-border-dark dark:bg-app-surface-dark sm:p-6"
    >
      <div className="mb-5 text-center">
        <h2 className="text-lg font-bold text-app-text dark:text-app-text-dark">
          Verify Your Email
        </h2>
        <p className="mt-1 text-sm text-app-muted dark:text-app-muted-dark">
          We sent a 6-digit code to <span className="font-medium">{email}</span>
        </p>
      </div>

      <Controller
        name="code"
        control={control}
        rules={{
          required: "OTP code is required",
          pattern: {
            value: /^\d{6}$/,
            message: "Please enter a valid 6-digit code",
          },
        }}
        render={({ field }) => (
          <GlobalInput
            label="OTP Code"
            type="text"
            inputMode="numeric"
            maxLength={6}
            placeholder="Enter 6-digit code"
            className="h-11 text-center text-lg tracking-[0.5em] focus:ring-2 focus:ring-app-primary-ring/20"
            error={errors.code?.message}
            {...field}
          />
        )}
      />

      <GlobalButton
        type="submit"
        disabled={isBusy}
        className="h-11 w-full text-sm font-bold"
      >
        {isBusy ? "Verifying..." : "Verify OTP"}
      </GlobalButton>

      <div className="mt-4 flex items-center justify-between">
        <button
          type="button"
          onClick={onBack}
          className="text-sm text-app-muted hover:text-app-text dark:text-app-muted-dark dark:hover:text-app-text-dark"
        >
          &larr; Back to login
        </button>

        <button
          type="button"
          onClick={handleResend}
          disabled={resendDisabled || isBusy}
          className="text-sm font-medium text-app-primary hover:underline disabled:cursor-not-allowed disabled:opacity-50"
        >
          {countdown > 0 ? `Resend in ${countdown}s` : "Resend OTP"}
        </button>
      </div>

      {message && (
        <GlobalFormMessage tone="success" className="mt-4">
          {message}
        </GlobalFormMessage>
      )}
    </GlobalForm>
  );
}
