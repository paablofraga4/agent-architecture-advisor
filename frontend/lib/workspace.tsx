"use client";

import {
  createContext,
  useContext,
  useEffect,
  useState,
  type ReactNode,
} from "react";

/**
 * Lightweight multi-user model WITHOUT login. A "workspace" stands in for a
 * tenant/user: it scopes the client_id used across the app (history, KB,
 * runs), recolors the whole UI via the --accent CSS variable, and shows
 * distinct branding in the header. Persisted in localStorage so a refresh
 * keeps you in the same workspace.
 */
export type Workspace = {
  id: string; // also used as client_id
  name: string;
  role: string;
  tagline: string;
  initials: string;
  /** space-separated RGB triplet for the --accent CSS var */
  accentRgb: string;
  plan: "Demo" | "Team" | "Enterprise";
};

export const WORKSPACES: Workspace[] = [
  {
    id: "default",
    name: "Demo pública",
    role: "Sandbox compartido",
    tagline: "Explora el advisor con datos de ejemplo.",
    initials: "DP",
    accentRgb: "14 165 233", // sky
    plan: "Demo",
  },
  {
    id: "acme",
    name: "Acme Consulting",
    role: "Cloud advisory partner",
    tagline: "Recomendaciones para tus clientes enterprise.",
    initials: "AC",
    accentRgb: "139 92 246", // violet
    plan: "Enterprise",
  },
  {
    id: "nordic",
    name: "Nordic Bank",
    role: "Equipo de arquitectura",
    tagline: "Banca regulada · residencia de datos UE.",
    initials: "NB",
    accentRgb: "16 185 129", // emerald
    plan: "Team",
  },
];

export function getWorkspace(id: string): Workspace {
  return WORKSPACES.find((w) => w.id === id) ?? WORKSPACES[0];
}

const STORAGE_KEY = "aaa.workspace";

type Ctx = {
  workspace: Workspace;
  setWorkspaceId: (id: string) => void;
};

const WorkspaceContext = createContext<Ctx | null>(null);

export function WorkspaceProvider({ children }: { children: ReactNode }) {
  const [id, setId] = useState<string>("default");

  // Hydrate from localStorage on mount (client only).
  useEffect(() => {
    const saved =
      typeof window !== "undefined" ? localStorage.getItem(STORAGE_KEY) : null;
    if (saved && WORKSPACES.some((w) => w.id === saved)) setId(saved);
  }, []);

  const workspace = getWorkspace(id);

  // Recolor the whole UI + persist whenever the workspace changes.
  useEffect(() => {
    if (typeof document !== "undefined") {
      document.documentElement.style.setProperty("--accent", workspace.accentRgb);
    }
    if (typeof window !== "undefined") {
      localStorage.setItem(STORAGE_KEY, workspace.id);
    }
  }, [workspace.id, workspace.accentRgb]);

  return (
    <WorkspaceContext.Provider value={{ workspace, setWorkspaceId: setId }}>
      {children}
    </WorkspaceContext.Provider>
  );
}

export function useWorkspace(): Ctx {
  const ctx = useContext(WorkspaceContext);
  if (!ctx) throw new Error("useWorkspace must be used within WorkspaceProvider");
  return ctx;
}
