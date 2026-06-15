"use client";

import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeRaw from "rehype-raw";

export default function Report({ markdown }: { markdown: string }) {
  if (!markdown) return null;
  return (
    <div className="report-md rounded-xl border border-border bg-panel p-5">
      <ReactMarkdown remarkPlugins={[remarkGfm]} rehypePlugins={[rehypeRaw]}>
        {markdown}
      </ReactMarkdown>
    </div>
  );
}
