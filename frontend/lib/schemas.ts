import { z } from "zod";

export const authSchema = z.object({
  email: z.string().email("Please enter a valid email address"),
  password: z.string().min(1, "Password must be at least 1 characters"),
});

export const taskSchema = z.object({
  task: z.string().min(1, "Task text is required"),
});
