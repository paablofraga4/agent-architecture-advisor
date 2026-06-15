"use client";

import { getWorkspace, type Workspace } from "@/lib/workspace";

/**
 * A distinct SVG monogram per workspace, tinted with its accent color.
 * Each workspace gets a different geometric motif so the brand reads
 * differently at a glance — not just different initials.
 */
function Glyph({ id, color }: { id: string; color: string }) {
  switch (id) {
    case "acme":
      // overlapping diamonds
      return (
        <g stroke={color} strokeWidth="2.4" fill="none">
          <rect x="9" y="9" width="12" height="12" transform="rotate(45 15 15)" />
          <rect x="13" y="13" width="14" height="14" transform="rotate(45 20 20)" />
        </g>
      );
    case "nordic":
      // shield / vault
      return (
        <g stroke={color} strokeWidth="2.4" fill="none" strokeLinejoin="round">
          <path d="M20 6 L31 11 V20 C31 27 26 31 20 34 C14 31 9 27 9 20 V11 Z" />
          <circle cx="20" cy="19" r="3.2" fill={color} stroke="none" />
        </g>
      );
    default:
      // concentric nodes (demo)
      return (
        <g fill="none" stroke={color} strokeWidth="2.4">
          <circle cx="20" cy="20" r="11" />
          <circle cx="20" cy="20" r="4.5" fill={color} stroke="none" />
          <line x1="20" y1="9" x2="20" y2="14" />
          <line x1="20" y1="26" x2="20" y2="31" />
          <line x1="9" y1="20" x2="14" y2="20" />
          <line x1="26" y1="20" x2="31" y2="20" />
        </g>
      );
  }
}

export default function BrandMark({
  workspace,
  size = 40,
  className = "",
}: {
  workspace?: Workspace;
  size?: number;
  className?: string;
}) {
  const ws = workspace ?? getWorkspace("default");
  const color = `rgb(${ws.accentRgb})`;
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 40 40"
      className={className}
      role="img"
      aria-label={`${ws.name} logo`}
    >
      <rect
        x="1"
        y="1"
        width="38"
        height="38"
        rx="10"
        fill={`rgb(${ws.accentRgb} / 0.12)`}
        stroke={color}
        strokeOpacity="0.4"
      />
      <Glyph id={ws.id} color={color} />
    </svg>
  );
}
