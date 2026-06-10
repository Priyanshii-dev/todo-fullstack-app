export const API_ENDPOINTS = {
  auth: {
    login: "/api/auth/login/",
    register: "/api/auth/register/",
    verifyOtp: "/api/auth/verify-otp/",
    resendOtp: "/api/auth/resend-otp/",
  },
  tasks: {
    list: "/api/tasks/",
    create: "/api/tasks/create/",
    detail: (id: number) => `/api/tasks/${id}/`,
    edit:   (id: number) => `/api/tasks/edit/${id}`,
    delete: (id: number) => `/api/tasks/delete/${id}`,
    toggle: (id: number) => `/api/tasks/toggle/${id}`,
    logo:   (id: number) => `/api/tasks/${id}/logo/`,
  },
} as const;
