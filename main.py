import time
import os
import sys
import json
import hashlib
import random
import string

# --- Configuration for simulating workload ---
NUM_RECORDS = 10000  # Number of data records to process
PROCESSING_INTENSITY = 500  # Number of iterations for CPU-bound work per record
OUTPUT_FILE_NAME = "processed_integration_data.json"
# --- End Configuration ---

def generate_dummy_record(record_id):
    """Generates a single dummy data record."""
    return {
        "id": record_id,
        "timestamp": time.time(),
        "source_system": random.choice(["CRM", "ERP", "CMS", "LegacyDB"]),
        "data_payload": ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(50, 200))),
        "status": "pending"
    }

def perform_cpu_intensive_task(data_payload, intensity):
    """Simulates CPU-bound data transformation/validation."""
    # This loop simulates CPU-intensive operations, directly impacting CPU usage.
    result = data_payload
    for _ in range(intensity):
        result = hashlib.sha256(result.encode()).hexdigest()
    return result[:32] # Return a portion to simulate a transformed value

def simulate_integration_runtime_task(num_records, processing_intensity, output_file):
    """
    Simulates an on-premise integration runtime task, processing data
    and writing it to an output file, demonstrating resource consumption.
    """
    print(f"Starting integration task simulation with {num_records} records...")
    print(f"Processing intensity per record: {processing_intensity} iterations.")

    start_time = time.perf_counter()
    processed_data = []
    total_memory_usage_estimate = 0 # Rough estimate for demonstration

    for i in range(num_records):
        record = generate_dummy_record(i)
        # Simulate CPU-bound transformation
        # This part consumes CPU resources based on PROCESSING_INTENSITY
        transformed_value = perform_cpu_intensive_task(record["data_payload"], processing_intensity)
        record["transformed_hash"] = transformed_value
        record["status"] = "processed"
        processed_data.append(record)

        # Estimate memory usage (very rough for demonstration purposes)
        total_memory_usage_estimate += sys.getsizeof(record)

        if (i + 1) % (num_records // 10 if num_records >= 10 else 1) == 0:
            print(f"  Processed {i + 1}/{num_records} records...")

    # Simulate writing processed data to a target system (disk I/O)
    # This part consumes disk I/O resources, impacting disk throughput.
    print(f"\nWriting {len(processed_data)} records to '{output_file}'...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(processed_data, f, indent=2)

    end_time = time.perf_counter()
    duration = end_time - start_time

    file_size_bytes = os.path.getsize(output_file)

    print("\n--- Simulation Results ---")
    print(f"Total execution time: {duration:.4f} seconds")
    print(f"Output file '{output_file}' size: {file_size_bytes / (1024*1024):.2f} MB")
    print(f"Estimated in-memory data size: {total_memory_usage_estimate / (1024*1024):.2f} MB (rough estimate)")
    print("\nTo observe resource consumption, monitor your system's CPU, Memory, and Disk I/O during execution.")
    print("Try changing NUM_RECORDS and PROCESSING_INTENSITY variables to see impact.")

if __name__ == "__main__":
    simulate_integration_runtime_task(NUM_RECORDS, PROCESSING_INTENSITY, OUTPUT_FILE_NAME)
