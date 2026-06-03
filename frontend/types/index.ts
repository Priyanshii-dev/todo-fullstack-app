export type TokenPair = {
  access: string;
  refresh?: string;
}

export type AuthUser = {
  id: number;
  username: string;
  email: string;
}

export type AuthResponse = {
  token: string;
  user: AuthUser;
}
