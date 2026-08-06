import { QueryClient } from "@tanstack/react-query";

import {
  DEFAULT_QUERY_RETRY_COUNT,
  DEFAULT_QUERY_STALE_TIME_MS,
} from "@/lib/utils/constants";

export function createQueryClient() {
  return new QueryClient({
    defaultOptions: {
      queries: {
        refetchOnWindowFocus: false,
        retry: DEFAULT_QUERY_RETRY_COUNT,
        staleTime: DEFAULT_QUERY_STALE_TIME_MS,
      },
      mutations: {
        retry: 0,
      },
    },
  });
}

