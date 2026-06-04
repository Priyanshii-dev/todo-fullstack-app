"use client";

import { useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useParams, useRouter } from "next/navigation";

import { useTodoStore } from "@/store/todo-store";
import { useFetchData } from "@/api/hooks/useFetch";

import { API_ENDPOINTS } from "@/api/endpoints";
import { mapTask } from "@/api/mappers";
import usePostData from "@/api/hooks/usePost";
import usePutData from "@/api/hooks/use-put";
import useDeleteData from "@/api/hooks/use-delete";
import instance from "@/api/instance";
import { taskSchema } from "@/lib/schemas";
import { Task, TaskFormMode, TaskFormValues, TaskTableParams, TaskTableResponse } from "../types/tasks.types";
import { useAuthStore } from "@/store/auth-store";
import { toast } from "sonner";

const TASKS_ROUTE = "/tasks";

// Task Pannel
export function useTasksPanel(params: TaskTableParams) {
  const message  = useTodoStore((s) => s.message);
  const accessToken = useAuthStore((s) => s.accessToken);
  const isAuthenticated = Boolean(accessToken);

  const {
    isLoading: fetching,
    refetch,
    data,
  } = useQuery<TaskTableResponse>({
    queryKey: [API_ENDPOINTS.tasks.list, params],
    enabled: isAuthenticated,
    queryFn: async () => {
      const requestParams = {
        page: params.page,
        limit: params.limit,
        ...(params.search.trim() ? { search: params.search.trim() } : {}),
        ...(params.status !== "all" ? { status: params.status } : {}),
      };

      const response = await instance.get<{
        data: TaskTableResponse;
      }>(API_ENDPOINTS.tasks.list, {
        params: requestParams,
      });

      return response.data.data;
    },
    select: (raw) => ({
      ...raw,
      results: raw.results.map(mapTask),
    }),
    refetchOnWindowFocus: false,
  });

  return {
    tasks: data?.results ?? [],
    totalTasks: data?.totalTasks ?? 0,
    completedTasks: data?.completedTasks ?? 0,
    totalItems: data?.total ?? 0,
    totalPages: data?.totalPages ?? 1,
    currentPage: data?.page ?? params.page,
    isAuthenticated,
    fetching,
    message,
    refetch,
  };
}

export function useBulkToggleTasks() {
  const queryClient = useQueryClient();
  const [message, setMessage] = useState("");

  const { mutateAsync, isPending } = useMutation<void, Error, number>({
    mutationFn: async (taskId) => {
      await instance.post(API_ENDPOINTS.tasks.toggle(taskId));
    },
  });

  async function toggleTasks(taskIds: number[]) {
    if (!taskIds.length) return false;

    setMessage("");

    try {
      await Promise.all(taskIds.map((taskId) => mutateAsync(taskId)));
      await queryClient.invalidateQueries({ queryKey: [API_ENDPOINTS.tasks.list] });
      return true;
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "Unable to toggle selected tasks.");
      return false;
    }
  }

  return {
    bulkToggling: isPending,
    bulkMessage: message,
    clearBulkMessage: () => setMessage(""),
    toggleTasks,
  };
}

export function useTaskFormAction(mode: TaskFormMode) {
  const router = useRouter();
  const queryClient = useQueryClient();
  const params = useParams<{ id?: string }>();
  const taskId = params.id ?? "";

  const addTask    = useTodoStore((s) => s.addTask);
  const updateTask = useTodoStore((s) => s.updateTask);
  const removeTask = useTodoStore((s) => s.removeTask);

  const [message, setMessage] = useState("");

  const needsTask = mode === "edit" || mode === "delete";

  // Fetch
  const { data: rawTask, isLoading } = useFetchData<Task>({
    url: API_ENDPOINTS.tasks.detail(Number(taskId)),
    enabled: needsTask && !!taskId,
  });

  const fetchedTask = rawTask ? mapTask(rawTask) : null;

  //  Create
  const { mutateAsync: createTask, isPending: isCreating } =
  usePostData<Task, FormData>({
    url: API_ENDPOINTS.tasks.create,
    showToast: true,
    onSuccess: async (data) => {
      addTask(mapTask(data));
      await queryClient.invalidateQueries({ queryKey: [API_ENDPOINTS.tasks.list] });
      router.push(TASKS_ROUTE);
    },
  });

  // Edit 
  const { mutateAsync: editTask, isPending: isEditing } =
  usePutData<FormData, Task>({
    url: API_ENDPOINTS.tasks.edit(Number(taskId)),
    mutationOptions: {
      onSuccess: async (data) => {
        updateTask(mapTask(data));
        await queryClient.invalidateQueries({
          queryKey: [API_ENDPOINTS.tasks.list],
        });
        router.push(TASKS_ROUTE);
      },
    },
  });

  // Delete
  const { mutateAsync: destroyTask, isPending: isDeleting } = useDeleteData<Task>({
    url: API_ENDPOINTS.tasks.delete(Number(taskId)),
    mutationOptions: {
      onSuccess: async () => {
        removeTask(Number(taskId));
        await queryClient.invalidateQueries({ queryKey: [API_ENDPOINTS.tasks.list] });
        router.push(TASKS_ROUTE);
      },
    },
  });


  // Handlers
  async function submitTask(values: TaskFormValues) {
    setMessage("");

    const validation = taskSchema.safeParse({
      task: values.task,
    });

    if (!validation.success) {
      const message = validation.error.issues
        .map((i) => i.message)
        .join(" ");

      setMessage(message);
      toast.error(message);
      return;
    }

    try {
      const formData = new FormData();
      formData.append("task", validation.data.task);
      formData.append("is_completed", String(values.isCompleted));

      if (values.logo) {
        formData.append("logo_upload", values.logo);
      }

      if (mode === "create") {
        await createTask(formData);
      } else {
        await editTask({ payload: formData });
      }
    } catch (error) {
      const message =
        error instanceof Error
          ? error.message
          : `Unable to ${mode} task.`;

      setMessage(message);
      toast.error(message);
    }
  }

  async function deleteTask() {
    setMessage("");
    try {
      await destroyTask("");
    } catch (error) {
      const message = error instanceof Error ? error.message : "Unable to delete task.";
      setMessage(message);
      toast.error(message);
    }
  }

  return {
    task:         fetchedTask?.task        ?? "",
    isCompleted:  fetchedTask?.is_completed ?? false,
    isLoading:    needsTask && isLoading,
    isSubmitting: isCreating || isEditing || isDeleting,
    message,
    goBack:       () => router.push(TASKS_ROUTE),
    submitTask,
    deleteTask,
  };
}
