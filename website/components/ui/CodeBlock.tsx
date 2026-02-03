"use client";

import { useState } from "react";
import { cn } from "@/lib/utils";

interface CodeBlockProps {
  code: string;
  language?: string;
  className?: string;
}

export function CodeBlock({ code, language = "bash", className }: CodeBlockProps) {
  const [copied, setCopied] = useState(false);

  const copyToClipboard = async () => {
    await navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className={cn("relative group", className)}>
      <div className="absolute right-2 top-2 opacity-0 group-hover:opacity-100 transition-opacity">
        <button
          onClick={copyToClipboard}
          className="px-3 py-1 text-xs bg-gray-700 hover:bg-gray-600 text-white rounded"
        >
          {copied ? "Copied!" : "Copy"}
        </button>
      </div>
      <pre
        tabIndex={0}
        className="bg-gray-900 text-gray-100 p-4 rounded-lg overflow-x-auto focus:outline-none focus:ring-2 focus:ring-teal focus:ring-offset-2"
      >
        <code className={`language-${language}`}>{code}</code>
      </pre>
    </div>
  );
}
