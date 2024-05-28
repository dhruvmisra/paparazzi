export const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;
export const ENABLE_MOCKING = import.meta.env.MODE !== "production" && import.meta.env.VITE_ENABLE_MOCKING === "true";
export const USER_ID = import.meta.env.VITE_USER_ID;
export const HEALTH_CHECK_INTERVAL = 5000;
