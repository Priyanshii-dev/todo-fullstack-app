export type AuthTabsProps = {
  mode: AuthMode;
  onModeChange: (mode: AuthMode) => void;
};

export type AuthFormValues = {
  email: string;
  password: string;
};

export type AuthFormProps = {
  mode: AuthMode;
  onModeChange?: (mode: AuthMode) => void;

  defaultValues?: Partial<AuthFormValues>;
  onSubmit: (values: AuthFormValues) => void | Promise<void>;

  isBusy: boolean;
  message: string;
};

export type AuthStates = {
  total: number;
  completed: number;
};

export type AuthMode = "login" | "register";

export type AuthPageProps = {
  mode: AuthMode;
};
