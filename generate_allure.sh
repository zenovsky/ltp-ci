#!/bin/bash
# License: MIT
# Copyright (c) 2025 Konstantin Zenovsky <https://github.com/zenovsky>
# Generates allure-report from allure-results while maintaining the history of previous tests.
# https://github.com/zenovsky/ltp-ci

# Folders with results and report
RESULTS_DIR="allure-results"
REPORT_DIR="allure-report"
ALLURE_BIN="/opt/allure/bin/allure"

# Copy the history from the previous report, if there is one
if [ -d "$REPORT_DIR/history" ]; then
    echo "Copying history from previous report..."
    cp -r "$REPORT_DIR/history" "$RESULTS_DIR/" 2>/dev/null
fi

# Generating the allure-report
echo "Generate a new report..."
"$ALLURE_BIN" generate "$RESULTS_DIR" --clean -o "$REPORT_DIR"