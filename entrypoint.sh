#!/bin/bash
# $1: password
# $2: timeout(seconds) 
# $3: worker_no
# $4: num_workers
cd /golem/work
echo   -n   $1 | sha256sum | awk '{print $1}' > password.sha256
timeout $2s /jtr/run/john --format=raw-sha256 --node=$3/$4 password.sha256
# Output password to file if had found within requested timeout
/jtr/run/john --format=raw-sha256 --show password.sha256 > /golem/output/result.txt
