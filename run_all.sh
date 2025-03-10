#!/bin/bash

# Directory containing the .lean files
LEAN_DIR="./examples/minif2ftest/nanti1"
# Directory for output files
OUTPUT_DIR="./output_logs"
# Maximum duration in seconds
MAX_DURATION=1260

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Trap for handling Ctrl+C
trap 'skip_current=true' INT

# Set default value
skip_current=false

echo "Press Ctrl+C once to skip the current file and continue to the next"
echo "Press Ctrl+C twice in quick succession to exit the script completely"

# Loop through each .lean file in the directory
for file in "$LEAN_DIR"/*.lean; do
    # Reset skip flag at the start of each iteration
    skip_current=false
    
    # Extract the filename without path and extension
    filename=$(basename "$file" .lean)
    
    # Define output file
    output_file="$OUTPUT_DIR/${filename}_output.log"
    
    echo "Starting processing $filename, output will be saved to $output_file"
    
    # Run the command in the background and get its PID
    python ./leansearch/__main__.py runasync \
        "$file" "minif2f_test.lean","$filename" \
        --sandbox ExternalProcessSandbox \
        --team yzh0123-uw-madison \
        --model vllm*8\
        --evaluators 8 --samplers 8 --islands 15 --duration 1200 --tag minif2f_test_hard_3 --envfile .env \
        > "$output_file" 2>&1 &
    
    PID=$!
    
    # Wait for process to complete, timeout, or manual skip
    SECONDS=0
    while kill -0 $PID 2>/dev/null; do
        if [ $SECONDS -ge $MAX_DURATION ] || [ "$skip_current" = true ]; then
            # Record reason for termination
            if [ "$skip_current" = true ]; then
                echo "Process for $filename manually skipped by user after $SECONDS seconds" | tee -a "$output_file"
            else
                echo "Process for $filename timed out after $MAX_DURATION seconds" | tee -a "$output_file"
            fi
            
            # Send termination signal
            echo "Sending SIGINT to process $PID..." | tee -a "$output_file"
            kill -SIGINT $PID
            
            # Wait a bit for graceful shutdown
            sleep 30

            kill -SIGINT $PID

            sleep 10
            
            # If process still running, force kill
            if kill -0 $PID 2>/dev/null; then
                echo "Process still running, sending SIGTERM..." | tee -a "$output_file"
                kill -SIGTERM -$PID
                sleep 5
                pkill -9 -P $PID
                sleep 5
                
                # Last resort: SIGKILL
                if kill -0 $PID 2>/dev/null; then
                    echo "Process still running, forcing SIGKILL..." | tee -a "$output_file"
                    kill -9 -$PID
                fi
            fi
            
            break
        fi
        sleep 1
    done
    
    # Check if process completed normally
    if ! kill -0 $PID 2>/dev/null && [ $SECONDS -lt $MAX_DURATION ] && [ "$skip_current" = false ]; then
        echo "Completed processing $filename"
    fi
    
    # Small delay between runs to ensure resources are freed
    sleep 2
    
    echo "Press Enter to continue to the next file, or Ctrl+C to exit completely"
    read -t 3 || true  # Optional 3-second pause between files
done

# Reset the trap when we're done
trap - INT
echo "All files processed"
