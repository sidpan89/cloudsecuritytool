#!/bin/bash
curl -X POST http://localhost:8000/api/scans -H 'Content-Type: application/json' -d '{"tool":"prowler","fixture":true}'
