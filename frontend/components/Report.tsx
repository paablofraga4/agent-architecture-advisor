"use client";

import { Fragment, type ReactNode } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeRaw from "rehype-raw";

const CITATION_RE = /\[CTX-\d{3,4}\]/g;

/** Turn raw [CTX-0283] tokens inside a text node into styled chips. */
function withCitationChips(children: ReactNode): ReactNode {
  return mapText(children, (text, key) => {
    if (!CITATION_RE.test(text)) return text;
    CITATION_RE.lastIndex = 0;
    const out: ReactNode[] = [];
    let last = 0;
    let m: RegExpExecArray | null;
    let i = 0;
    while ((m = CITATION_RE.exec(text)) !== null) {
      if (m.index > last) out.push(text.slice(last, m.index));
      const id = m[0].slice(1, -1); // CTX-0283
      out.push(
        <span
          key={`${key}-c${i++}`}
          title={`Contexto recuperado ${id}`}
          className="citation-chip"
        >
          {id}
        </span>
      );
      last = m.index + m[0].length;
    }
    if (last < text.length) out.push(text.slice(last));
    return <Fragment key={key}>{out}</Fragment>;
  });
}

function mapText(
  node: ReactNode,
  fn: (text: string, key: string, idx: number) => ReactNode,
  keyPrefix = "t"
): ReactNode {
  if (typeof node === "string") return fn(node, keyPrefix, 0);
  if (Array.isArray(node))
    return node.map((c, i) => (
      <Fragment key={`${keyPrefix}-${i}`}>
        {mapText(c, fn, `${keyPrefix}-${i}`)}
      </Fragment>
    ));
  return node;
}

export default function Report({ markdown }: { markdown: string }) {
  if (!markdown) return null;
  return (
    <div className="report-md panel-card rounded-2xl border border-border bg-panel p-6 md:p-8">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        rehypePlugins={[rehypeRaw]}
        components={{
          p: ({ children }) => <p>{withCitationChips(children)}</p>,
          li: ({ children }) => <li>{withCitationChips(children)}</li>,
          td: ({ children }) => <td>{withCitationChips(children)}</td>,
        }}
      >
        {markdown}
      </ReactMarkdown>
    </div>
  );
}
