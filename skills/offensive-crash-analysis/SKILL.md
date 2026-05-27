---
name: offensive-crash-analysis
description: "*Report generated: $(date)*"
domain: cybersecurity
---
*Report generated: $(date)*
*Analyst: [Your Name]*
EOF

echo "Report saved to reports/vulnerability_report.md"
```

### Capstone Checklist

- [ ] Lab environment set up (`~/crash_analysis_lab/capstone/`)
- [ ] 28+ crash inputs generated from vulnerable_suite.c
- [ ] CASR reports generated for all crashes
- [ ] Crashes clustered into 5 unique bug classes
- [ ] Root cause identified for all unique bugs
- [ ] Exploitability assessment completed (4 EXPLOITABLE, 1 NOT_EXPLOITABLE)
- [ ] Minimum trigger sizes found for overflow bugs
- [ ] Python PoC suite created and tested
- [ ] Final vulnerability report generated

### Expected Deliverables

```
~/crash_analysis_lab/capstone/
├── crashes/           # 28 raw crash inputs
│   ├── stack_*.txt    # Stack overflow variants
│   ├── heap_*.txt     # Heap overflow variants
│   ├── uaf_*.txt      # UAF crashes
│   ├── df_*.txt       # Double-free crashes
│   └── null_*.txt     # NULL deref crashes
├── casrep/            # CASR analysis reports
├── deduped/           # Clustered unique crashes
│   ├── cl1/           # Stack overflow cluster
│   ├── cl2/           # Heap overflow cluster
│   ├── cl3/           # UAF cluster
│   ├── cl4/           # Double-free cluster
│   └── cl5/           # NULL deref cluster
├── minimized/         # Minimized crash inputs
│   ├── stack_min.txt
│   ├── heap_min.txt
│   ├── uaf_min.txt
│   └── df_min.txt
├── pocs/              # PoC scripts
│   └── capstone_poc.py
└── reports/           # Final report
    └── vulnerability_report.md
```

### Key Takeaways

1.  **Triage is a Filter**: The 28 crash inputs reduced to just 5 unique bugs - automation saves hours of manual analysis.
2.  **Root Cause > Crash Location**: ASAN shows where corruption is _detected_, but the bug is in the `strcpy()` call.
3.  **Reproducibility is King**: All PoCs achieve 100% reliability because the bugs are deterministic.
4.  **Report for the Audience**: The vulnerability report includes both technical details (for developers) and severity ratings (for management).
5.  **Stack Overflow = RIP Control**: The 72-byte offset gives direct control over the return address.

### Discussion Questions

1.  Why does the stack overflow require 72 bytes to control RIP (not 64)?
2.  How would ASLR affect exploitation of the stack overflow in `vuln_protected`?
3.  Why is the NULL pointer dereference classified as NOT_EXPLOITABLE while the others are EXPLOITABLE?
4.  How would you extend this analysis to include the `vuln_http_server` network target?

### Bonus Challenge: Network Target Analysis

Extend the capstone to include the `vuln_http_server` from Day 4:

```bash
cd ~/crash_analysis_lab/capstone

# Generate HTTP server crashes with long paths
for size in 100 500 1000 2000; do
    python3 -c "import sys; sys.stdout.buffer.write(b'GET /' + b'X'*$size + b' HTTP/1.1\r\n\r\n')" > crashes/http_path_${size}.bin
done

# Test with non-ASAN binary (will show heap corruption on free)
../vuln_http_server &
SERVER_PID=$!
sleep 1

for crash in crashes/http_path_*.bin; do
    echo "Testing $(basename $crash)..."
    cat "$crash" | nc localhost 8888 || true
    sleep 0.5

    if ! kill -0 $SERVER_PID 2>/dev/null; then
        echo "  Server crashed!"
        ../vuln_http_server &
        SERVER_PID=$!
        sleep 1
    fi
done

kill $SERVER_PID 2>/dev/null
```

This adds a **network-accessible** vulnerability to your report and demonstrates an important lesson: **sanitizers have blind spots** - always use multiple detection methods.

### Looking Ahead to Week 5

Next week, we cross the Rubicon. You have the crash, you have the PoC, and you know it's exploitable. Now, we **build the exploit**. We will start with basic stack overflows, defeat simple mitigations, and learn to turn that instruction pointer overwrite into code execution.

<!-- Written by AnotherOne from @Pwn3rzs Telegram channel -->
