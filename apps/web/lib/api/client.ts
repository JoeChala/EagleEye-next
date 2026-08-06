import axios from "axios";

import { env } from "@/lib/utils/env";

export const apiClient = axios.create({
  baseURL: env.NEXT_PUBLIC_API_URL,
});

