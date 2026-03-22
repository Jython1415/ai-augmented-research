#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Audit classification agent JSONL logs for tool compliance."""
import json
import glob
import os
import sys

def audit_agent(agent_id):
    """Parse agent JSONL log and return tool usage summary."""
    matches = glob.glob(os.path.expanduser(
        f"~/.claude/projects/-Users-Joshua-agent/*/subagents/agent-{agent_id}.jsonl"
    ))
    if not matches:
        return {"agent_id": agent_id, "error": "log not found"}

    logfile = matches[0]
    tools = {}
    with open(logfile) as f:
        for line in f:
            try:
                entry = json.loads(line.strip())
            except json.JSONDecodeError:
                continue
            msg = entry.get("message", {})
            content = msg.get("content", [])
            if not isinstance(content, list):
                continue
            for block in content:
                if isinstance(block, dict) and block.get("type") == "tool_use":
                    name = block.get("name", "unknown")
                    tools[name] = tools.get(name, 0) + 1

    bash_count = tools.get("Bash", 0)
    return {
        "agent_id": agent_id,
        "tools": tools,
        "compliant": bash_count == 0,
        "bash_violations": bash_count
    }

def main():
    agent_ids = json.loads(sys.argv[1])
    labels = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}

    violations = []
    for aid in agent_ids:
        result = audit_agent(aid)
        label = labels.get(aid, aid[:12])
        status = "OK" if result.get("compliant", False) else "VIOLATION"
        if "error" in result:
            status = "MISSING"
        tools_str = ", ".join(f"{k}:{v}" for k, v in sorted(result.get("tools", {}).items()))
        print(f"[{status:9s}] {label:15s} tools=[{tools_str}]")
        if not result.get("compliant", True):
            violations.append(label)

    print(f"\nTotal: {len(agent_ids)} agents, {len(violations)} violations")
    if violations:
        print(f"Violators: {', '.join(violations)}")
    return len(violations)

if __name__ == "__main__":
    sys.exit(main())
