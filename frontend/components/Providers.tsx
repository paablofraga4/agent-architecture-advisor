"use client";

import type { ReactNode } from "react";
import { WorkspaceProvider } from "@/lib/workspace";
import { AuthProvider } from "@/lib/auth";

export default function Providers({ children }: { children: ReactNode }) {
  return (
    <AuthProvider>
      <WorkspaceProvider>{children}</WorkspaceProvider>
    </AuthProvider>
  );
}
