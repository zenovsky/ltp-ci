#!/bin/bash
# License: MIT
# Copyright (c) 2025 Konstantin Zenovsky <https://github.com/zenovsky>
# Script for running the main LTP tests
# https://github.com/zenovsky/ltp-ci
set -e

LTP_DIR="/opt/ltp"
RESULTS_JSON="/tmp/kirk.ciuser/latest/results.json"

echo "[+] Running LTP via kirk..."
cd "$LTP_DIR"
./kirk -U ltp -f syscalls fs fs_perms_simple dio mm irq sched math nptl pty containers fs_bind controllers fcntl-locktests power_management_tests hugetlb commands hyperthreading can cpuhotplug cve net.ipv6_lib input crypto kernel_misc uevent watchqueue
ls -l /tmp/kirk.ciuser/latest/