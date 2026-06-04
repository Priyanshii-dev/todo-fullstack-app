"use client";

import { useEffect, useRef, useState } from "react";
import { useForm } from "react-hook-form";
import { Plus, Save, Trash2, Upload, X } from "lucide-react";
import { GlobalButton } from "@/global/button";
import { GlobalDialog } from "@/global/dialog";
import { GlobalForm, GlobalFormActions, GlobalFormMessage } from "@/global/form";
import { GlobalCheckbox, GlobalInput } from "@/global/input";
import { TaskFormProps, TaskFormValues } from "./types/tasks.types";

const modeCopy = {
  create: { title: "Create task", submitLabel: "Create", loadingLabel: "Creating", icon: Plus },
  edit:   { title: "Edit task",   submitLabel: "Save",   loadingLabel: "Saving",   icon: Save },
  delete: { title: "Delete task", submitLabel: "Delete", loadingLabel: "Deleting", icon: Trash2 },
} as const;

export default function TaskForm({
  mode,
  task,
  isCompleted,
  logo,              
  loading = false,
  submitting = false,
  message = "",
  onBack,
  onSubmit,
  onDelete,
}: TaskFormProps) {
  const copy = modeCopy[mode];
  const ActionIcon = copy.icon;
  const isDeleteMode = mode === "delete";

  const fileInputRef = useRef<HTMLInputElement>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(logo ?? null);
  const [selectedFile, setSelectedFile] = useState<File | undefined>(undefined);

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<TaskFormValues>({
    defaultValues: { task, isCompleted },
  });

  useEffect(() => {
    reset({ task, isCompleted });
    setPreviewUrl(logo ?? null);
    setSelectedFile(undefined);
  }, [isCompleted, reset, task, logo]);

function handleFileChange(e: React.ChangeEvent<HTMLInputElement>) {
  const file = e.target.files?.[0];

  console.log("FILE PICKED:", file);

  if (!file) return;

  setSelectedFile(file);
  setPreviewUrl(URL.createObjectURL(file));
}

  function clearLogo() {
    setSelectedFile(undefined);
    setPreviewUrl(null);
    if (fileInputRef.current) fileInputRef.current.value = "";
  }

  function submitForm(values: TaskFormValues) {
     console.log("selectedFile at submit:", selectedFile);
    if (isDeleteMode) {
      onDelete?.();
      return;
    }
    onSubmit?.({ ...values, logo: selectedFile });  // ← pass File to hook
  }

  return (
    <GlobalDialog title={copy.title} onClose={onBack}>
      {message && (
        <GlobalFormMessage className="mb-4">
          {message}
        </GlobalFormMessage>
      )}

      {loading ? (
        <p className="text-sm text-app-muted dark:text-app-muted-dark">Loading task...</p>
      ) : (
        <GlobalForm onSubmit={handleSubmit(submitForm)}>
          {isDeleteMode ? (
            <p className="text-sm text-app-muted dark:text-app-muted-dark">
              Are you sure you want to delete{" "}
              <span className="font-semibold text-app-text dark:text-app-text-dark">
                {task || "this task"}
              </span>
              ?
            </p>
          ) : (
            <>
              <GlobalInput
                label="Task name"
                autoFocus
                error={errors.task?.message}
                {...register("task", { required: "Task text is required" })}
              />

              <GlobalCheckbox
                label="Task completed"
                {...register("isCompleted")}
              />

              {/* Logo upload */}
              <div className="flex flex-col gap-2">
                <label className="text-sm font-medium text-app-text dark:text-app-text-dark">
                  Logo <span className="text-app-muted dark:text-app-muted-dark font-normal">(optional)</span>
                </label>

                {/* Preview */}
                {previewUrl && (
                  <div className="relative w-16 h-16">
                    {/* eslint-disable-next-line @next/next/no-img-element */}
                    <img
                      src={previewUrl}
                      alt="Task logo preview"
                      className="size-full object-cover rounded-lg border border-app-border dark:border-app-border-dark"
                    />
                    <button
                      type="button"
                      onClick={clearLogo}
                      className="absolute -top-1.5 -right-1.5 bg-red-500 text-white rounded-full p-0.5 hover:bg-red-600"
                    >
                      <X className="size-3" />
                    </button>
                  </div>
                )}

                {/* Hidden native file input */}
                <input
                  ref={fileInputRef}
                  type="file"
                  accept="image/*"
                  className="hidden"
                  onChange={handleFileChange}
                />

                {/* Styled trigger button */}
                <button
                  type="button"
                  onClick={() => fileInputRef.current?.click()}
                  className="flex items-center gap-2 w-fit text-sm px-3 py-1.5 rounded-md border border-dashed border-app-border dark:border-app-border-dark text-app-muted dark:text-app-muted-dark hover:text-app-text dark:hover:text-app-text-dark hover:border-app-text dark:hover:border-app-text-dark transition-colors"
                >
                  <Upload className="size-4" />
                  {previewUrl ? "Change logo" : "Upload logo"}
                </button>
              </div>
            </>
          )}

          <GlobalFormActions>
            <GlobalButton
              type="button"
              variant="outline"
              onClick={onBack}
              className="w-full sm:w-auto"
            >
              Cancel
            </GlobalButton>

            <GlobalButton
              type="submit"
              disabled={submitting}
              variant={isDeleteMode ? "danger" : "primary"}
              className="w-full sm:w-auto"
            >
              <ActionIcon className="size-4" />
              {submitting ? copy.loadingLabel : copy.submitLabel}
            </GlobalButton>
          </GlobalFormActions>
        </GlobalForm>
      )}
    </GlobalDialog>
  );
}
