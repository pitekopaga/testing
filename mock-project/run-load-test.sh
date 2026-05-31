#!/bin/bash
# Run load test with 10 concurrent users for 30 seconds
echo "Starting load test with 10 concurrent users for 30 seconds"
locust -f load_tests/locustfile.py --headless -u 10 -r 2 --run-time 30s --host=http://localhost:5000
