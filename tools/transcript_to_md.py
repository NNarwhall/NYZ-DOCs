"""Turn an exported Claude Code session (zip) into a readable Markdown transcript.

Usage: python transcript_to_md.py <export.zip> <out.md> "<title>"
Keeps only what was said: the developer's messages, their answers in question dialogs, and Claude's replies.
Other tool calls, tool output, images and hidden reasoning are left out (they stay in the zip).
"""
import json, re, sys, zipfile

src, out, title = sys.argv[1], sys.argv[2], sys.argv[3]
lines = zipfile.ZipFile(src).read("transcript.jsonl").decode("utf-8").splitlines()
HIDDEN = re.compile(r"<(system-reminder|command-[a-z-]+|local-command-[a-z-]+)>.*?</\1>", re.S)

parts, seen, asks = [], set(), set()
for line in lines:
    o = json.loads(line)
    if o.get("type") not in ("user", "assistant") or o.get("isMeta"):
        continue
    content = o["message"]["content"]
    blocks = [content] if isinstance(content, str) else [b.get("text", "") for b in content if b.get("type") == "text"]
    if not isinstance(content, str):
        # Question dialogs: the answer's tool result repeats each question with the developer's choice.
        asks |= {b["id"] for b in content if b.get("type") == "tool_use" and b.get("name") == "AskUserQuestion"}
        for b in content:
            if b.get("type") == "tool_result" and b.get("tool_use_id") in asks:
                c = b.get("content")
                blocks.append(c if isinstance(c, str) else "\n".join(x.get("text", "") for x in c if x.get("type") == "text"))
    for text in blocks:
        text = HIDDEN.sub("", text).strip()
        key = (o["type"], o["message"].get("id"), text)
        if not text or key in seen:
            continue
        seen.add(key)
        who = "Developer" if o["type"] == "user" else "Claude"
        stamp = o.get("timestamp", "")[:16].replace("T", " ")
        parts.append(f"### {who} ({stamp})\n\n{text}\n")

with open(out, "w", encoding="utf-8") as f:
    f.write(f"# {title}\n\nReadable transcript: the developer's messages and Claude's replies only. "
            "The full export (tool calls, screenshots, metadata) is in the matching .zip.\n\n---\n\n")
    f.write("\n".join(parts))
print(f"{len(parts)} messages -> {out}")
