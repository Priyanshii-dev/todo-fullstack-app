import { Task } from "@/features/tasks/types/tasks.types";
import { AuthResponse, TokenPair } from "@/types";


export function mapTokenPair(payload: AuthResponse): TokenPair {
  if (!payload.token) {
    throw new Error("Authentication response did not include a token.");
  }

  return {
    access: payload.token,
  };
}

export function mapTask(payload: Task): Task {
  return {
    id: payload.id,
    task_number: payload.task_number ?? payload.id,
    task: payload.task,
    is_completed: payload.is_completed,
    user_id: payload.user_id,
    email: payload.email ?? "",
  };
}
