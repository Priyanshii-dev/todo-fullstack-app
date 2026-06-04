export type TaskStatusFilter = "all" | "completed" | "pending";

export type Task = {
  id: number;
  task_number: number;
  task: string;
  is_completed: boolean;
  user_id: number;
  email: string;
  logo?: string;
};

export type TaskTableParams = {
  page: number;
  limit: number;
  search: string;
  status: TaskStatusFilter;
};

export type TaskTableResponse = {
  results: Task[];
  page: number;
  limit: number;
  total: number;
  totalPages: number;
  totalTasks: number;
  completedTasks: number;
};

export type TaskStatsProps = {
  total: number;
  completed: number;
};

export type TaskListProps = {
  tasks: Task[];
  onToggle: (task: Task) => void;
  onDelete: (id: number) => void;
};

export type TaskNavbarProps = {
  onLogout: () => void;
};

export type TaskItemProps = {
  task: Task;
  onToggle: () => void;
  onDelete: () => void;
};

export type TaskFormMode = "create" | "edit" | "delete";

export type TaskFormValues = {
  task: string;
  isCompleted: boolean;
  logo?: File;         
};

export type TaskFormProps = {
  mode: TaskFormMode;
  task: string;
  isCompleted: boolean;
  logo?: string;      
  loading?: boolean;
  submitting?: boolean;
  message?: string;
  onBack: () => void;
  onSubmit?: (values: TaskFormValues) => void | Promise<void>;
  onDelete?: () => void | Promise<void>;
};