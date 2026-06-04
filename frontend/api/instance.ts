import axios, { AxiosError } from "axios";
import { useAuthStore } from "../store/auth-store";
import { ApiErrorPayload } from "./hooks/types";

export const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000";

function getErrorMessage(data: ApiErrorPayload | null) {
  if (data?.detail && typeof data.detail === "string") {
    return data.detail;
  }

  const fieldErrors = Object.values(data ?? {})
    .flat()
    .filter(Boolean)
    .join(" ");

  return fieldErrors || "Request failed";
}

const instance = axios.create({
  baseURL: API_BASE_URL,
});

export async function apiRequest<T>(
  url: string,
  options: RequestInit = {},
): Promise<T> {
  const body = options.body;
  const isFormData = body instanceof FormData;
  const hasContentType = !!(options.headers as Record<string, string>)?.["Content-Type"];

  const response = await instance.request<T>({
    url,
    method: options.method ?? "GET",
    data: body,
    headers: {
      ...(!isFormData && !hasContentType && body != null
        ? { "Content-Type": "application/json" }
        : {}),
      ...(options.headers as Record<string, string> | undefined),
    },
  });

 if (
    response.data &&
    typeof response.data === "object" &&
    "statusCode" in response.data &&
    "data" in response.data
  ) {
    return response.data.data as T;
  }

  return response.data as T;

}

instance.interceptors.request.use(
  (config) => {
    const token = useAuthStore.getState().accessToken;

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => Promise.reject(error),
);

instance.interceptors.response.use(
  (response) => response,
  (error: AxiosError<ApiErrorPayload>) => {
    const status = error.response?.status;
    const data = error.response?.data ?? null;

    // Auto logout on unauthorized
    if (status === 401 || status === 440) {
      useAuthStore.getState().clearAuth();

      if (typeof window !== "undefined") {
        window.location.href = "/";
      }
    }

    // Create clean error message
    const message = getErrorMessage(data);

    return Promise.reject(new Error(message));
  },
);

export default instance;
