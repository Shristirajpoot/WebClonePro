"use client";

import React, { useState } from "react";
import {
  ArrowPathIcon,
  ArrowDownTrayIcon,
  LinkIcon,
  ClipboardIcon,
  GlobeAltIcon,
} from "@heroicons/react/24/outline";
import { FaGithub } from "react-icons/fa";          // ← npm i react-icons
import ClipLoader from "react-spinners/ClipLoader"; // ← npm i react-spinners

/* ---------- types ---------- */
interface PageData {
  url: string;
  html: string;
  title: string;
  description: string;
  favicon: string | null;
}

/* ---------- helper: absolutise URLs in cloned HTML ---------- */
function makeUrlsAbsolute(html: string, base: string) {
  const doc = new DOMParser().parseFromString(html, "text/html");
  const rebase = (sel: string, attr: string) =>
    doc.querySelectorAll(sel).forEach((el) => {
      const v = el.getAttribute(attr);
      if (v && !/^https?:|^data:/.test(v))
        el.setAttribute(attr, new URL(v, base).href);
    });

  rebase("img[src]", "src");
  rebase("script[src]", "src");
  rebase("link[href]", "href");
  doc.querySelectorAll("a[href]").forEach((a) => {
    const h = a.getAttribute("href")!;
    if (!/^(https?:|#|mailto:)/.test(h))
      a.setAttribute("href", new URL(h, base).href);
  });

  return doc.documentElement.outerHTML;
}

/* tiny spinner */
const Spinner = () => <ClipLoader size={18} color="#3b82f6" />;

/* ---------- main component ---------- */
export default function Home() {
  const [url, setUrl] = useState("");
  const [pages, setPages] = useState<PageData[]>([]);
  const [sel, setSel] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setErr] = useState<string | null>(null);

  /* clone site */
  async function cloneSite(e: React.FormEvent) {
    e.preventDefault();
    setErr(null);
    setPages([]);
    if (!url) return setErr("Please enter a URL");
    setLoading(true);

    try {
      const r = await fetch("http://localhost:8000/clone", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url }),
      });
      if (!r.ok) {
        const msg = (await r.json()).detail || "Clone failed";
        throw new Error(msg);
      }
      const out = await r.json();
      if (!out.pages?.length) throw new Error("No pages returned");
      setPages(out.pages);
      setSel(0);
    } catch (e) {
  if (e instanceof Error) {
    setErr(e.message);
  } else {
    setErr("An unknown error occurred");
    }
  }

  /* download single page */
  function download(p: PageData) {
    const slug =
      p.title?.trim().replace(/\s+/g, "_").toLowerCase().slice(0, 30) ||
      p.url.replace(/[^a-z0-9]/gi, "_");
    const blob = new Blob([p.html], { type: "text/html" });
    const a = Object.assign(document.createElement("a"), {
      href: URL.createObjectURL(blob),
      download: slug + ".html",
    });
    a.click();
    URL.revokeObjectURL(a.href);
  }

  /* ---------- JSX ---------- */
  return (
    <div className="min-h-screen flex flex-col bg-background text-foreground container">
      {/* header */}
      <header className="flex items-center gap-2 px-6 py-4">
        <img src="/favicon.ico" alt="" className="h-6 w-6" />
        <h1 className="text-2xl font-bold tracking-tight">
          Orchids Website Cloner
        </h1>
      </header>

      {/* URL bar */}
      <form
        onSubmit={cloneSite}
        className="mx-auto w-full max-w-2xl flex items-center gap-3 px-4"
      >
        <LinkIcon className="h-5 w-5 text-gray-400 dark:text-gray-500" />
        <input
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="https://example.com"
          type="url"
          required
          autoComplete="off"
          className="flex-grow bg-white/60 dark:bg-white/10 backdrop-blur px-3 py-2 rounded-l-md border border-gray-300 dark:border-gray-700 focus:outline-none"
        />
        <button
          disabled={loading}
          className="bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white px-5 py-2 rounded-r-md flex items-center gap-2 transition-colors"
        >
          {loading ? <Spinner /> : <ArrowPathIcon className="h-5 w-5" />}
          {loading ? "Cloning" : "Clone"}
        </button>
      </form>

      {/* error */}
      {error && (
        <p className="text-center mt-4 text-red-600 dark:text-red-400">
          {error}
        </p>
      )}

      {/* empty state */}
      {pages.length === 0 && !loading && !error && (
        <p className="mt-12 text-gray-500 dark:text-gray-400 text-center">
          Paste a URL above and hit <em>Clone</em> to get started!
        </p>
      )}

      {/* main split */}
      {pages.length > 0 && (
        <div className="mt-8 flex flex-col md:flex-row flex-grow gap-6 w-full max-w-7xl mx-auto px-4">
          {/* sidebar */}
          <aside className="md:w-64 w-full bg-white/70 dark:bg-gray-900/60 backdrop-blur rounded-lg shadow p-4 max-h-[500px] overflow-y-auto">
            <h2 className="font-semibold mb-3">Pages</h2>
            <ul className="space-y-3">
              {pages.map((p, i) => (
                <li key={p.url} className="flex items-center gap-2">
                  {p.favicon && (
                    <img src={p.favicon} alt="" className="h-4 w-4 rounded" />
                  )}
                  <button
                    onClick={() => setSel(i)}
                    className={`truncate flex-1 text-left ${
                      i === sel
                        ? "font-medium text-blue-700 dark:text-blue-400"
                        : "hover:underline"
                    }`}
                  >
                    {p.title || p.url}
                  </button>
                </li>
              ))}
            </ul>
          </aside>

          {/* preview */}
          <section className="flex-1 flex flex-col bg-white/70 dark:bg-gray-900/60 backdrop-blur rounded-lg shadow overflow-hidden preview-section">
            <div className="flex justify-between items-center px-4 py-2 border-b border-gray-200 dark:border-gray-800">
              <span className="truncate">{pages[sel].title}</span>
              <div className="flex items-center gap-3">
                <button
                  onClick={() => navigator.clipboard.writeText(pages[sel].url)}
                  title="Copy URL"
                  className="text-sm text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 transition"
                >
                  <ClipboardIcon className="h-4 w-4" />
                </button>
                <button
                  onClick={() => download(pages[sel])}
                  className="inline-flex items-center gap-1 text-sm text-green-700 dark:text-green-400 hover:underline"
                >
                  <ArrowDownTrayIcon className="h-4 w-4" />
                  Download
                </button>
              </div>
            </div>

            <iframe
              sandbox="allow-same-origin allow-scripts"
              srcDoc={makeUrlsAbsolute(pages[sel].html, pages[sel].url)}
              className="flex-grow border-0 min-h-[600px] w-full"
              title="Preview"
            />

            <details className="px-4 py-3 border-t border-gray-200 dark:border-gray-800 text-sm">
              <summary className="font-medium cursor-pointer">Metadata</summary>
              <div className="mt-2 space-y-1">
                <p>
                  <strong>URL:</strong> {pages[sel].url}
                </p>
                <p>
                  <strong>Description:</strong> {pages[sel].description}
                </p>
              </div>
            </details>
          </section>
        </div>
      )}

      {/* ---------- footer (icons only) ---------- */}
  <footer className="border-t border-gray-200 dark:border-gray-700 mt-12 px-6 py-6 text-sm text-gray-600 dark:text-gray-400 flex items-center justify-center gap-6 text-center">
        <p className="flex items-center gap-1">
          © {new Date().getFullYear()}{" "}
          <span className="font-semibold text-foreground">Orchids</span> • Built with{" "}
          <span className="text-red-500">❤</span>
        </p>

        <a
          href="https://github.com/your-repo"
          target="_blank"
          rel="noopener noreferrer"
          title="GitHub"
          className="text-gray-500 dark:text-gray-400 hover:text-foreground transition"
        >
          <FaGithub className="h-5 w-5" />
        </a>

        <a
          href="https://orchids.ai"
          target="_blank"
          rel="noopener noreferrer"
          title="Website"
          className="text-gray-500 dark:text-gray-400 hover:text-foreground transition"
        >
          <GlobeAltIcon className="h-5 w-5" />
        </a>
      </footer>
    </div>  {/* <-- this is the root div closing */}
  );
}
