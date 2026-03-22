#!/usr/bin/env python3
"""Audit classification agent JSONL logs for tool compliance."""
import json
import sys
import os

def audit_agent_log(filepath):
    """Parse a JSONL log and extract tool usage."""
    tools = {}
    total_tool_calls = 0
    batch_file = None
    results_file = None

    with open(filepath) as f:
        for line in f:
            try:
                entry = json.loads(line.strip())
            except json.JSONDecodeError:
                continue

            # Look for assistant messages with tool_use
            msg = entry.get("message", {})
            content = msg.get("content", [])
            if not isinstance(content, list):
                continue

            for block in content:
                if isinstance(block, dict) and block.get("type") == "tool_use":
                    tool_name = block.get("name", "unknown")
                    tools[tool_name] = tools.get(tool_name, 0) + 1
                    total_tool_calls += 1

                    # Check what files were read/written
                    inp = block.get("input", {})
                    if tool_name == "Read":
                        fp = inp.get("file_path", "")
                        if "batch_" in fp:
                            batch_file = os.path.basename(fp)
                    elif tool_name == "Write":
                        fp = inp.get("file_path", "")
                        if "results_" in fp:
                            results_file = os.path.basename(fp)

    bash_count = tools.get("Bash", 0)
    return {
        "tools": tools,
        "total_tool_calls": total_tool_calls,
        "bash_violations": bash_count,
        "batch_file": batch_file,
        "results_file": results_file,
        "compliant": bash_count == 0
    }

def main():
    log_dir = sys.argv[1] if len(sys.argv) > 1 else ""
    agent_ids_file = sys.argv[2] if len(sys.argv) > 2 else ""

    with open(agent_ids_file) as f:
        agent_ids = json.load(f)

    results = []
    compliant = 0
    violations = 0

    for agent_id in agent_ids:
        filepath = os.path.join(log_dir, f"agent-{agent_id}.jsonl")
        if not os.path.exists(filepath):
            # Try other session dirs
            import glob
            matches = glob.glob(os.path.expanduser(
                f"~/.claude/projects/-Users-Joshua-agent/*/subagents/agent-{agent_id}.jsonl"
            ))
            if matches:
                filepath = matches[0]
            else:
                results.append({"agent_id": agent_id, "error": "log not found"})
                continue

        audit = audit_agent_log(filepath)
        audit["agent_id"] = agent_id
        results.append(audit)

        if audit["compliant"]:
            compliant += 1
        else:
            violations += 1

    summary = {
        "total_audited": len(results),
        "compliant": compliant,
        "violations": violations,
        "agents": results
    }

    # Print summary
    print(f"Audited: {len(results)} agents")
    print(f"Compliant: {compliant}")
    print(f"Violations: {violations}")

    for r in results:
        status = "OK" if r.get("compliant", False) else "VIOLATION"
        tools_str = ", ".join(f"{k}:{v}" for k,v in r.get("tools", {}).items())
        batch = r.get("batch_file", "?")
        print(f"  [{status}] {r['agent_id'][:12]}... batch={batch} tools=[{tools_str}]")

    # Save full report
    with open("/private/tmp/claude/relevance/audit_full_report.json", "w") as f:
        json.dump(summary, f, indent=2)

if __name__ == "__main__":
    main()
