import argparse
import os
import json
from jobrex import JobsClient

def main():
    parser = argparse.ArgumentParser(description="Generate a professional job description.")
    parser.add_argument("--api_key", required=True, help="Your Jobrex API key.")
    parser.add_argument("--job_title", required=True, help="Title of the job position.")
    parser.add_argument("--hiring_needs", required=True, help="Description of the hiring needs and requirements.")
    parser.add_argument("--company_description", required=True, help="Brief description of the company.")
    parser.add_argument("--job_type", required=True, help="Type of job (e.g., Full-time, Part-time, Contract).")
    parser.add_argument("--job_location", required=True, help="Location of the job.")
    parser.add_argument("--specific_benefits", required=True, help="List of benefits offered.")
    parser.add_argument("--output_dir", required=True, help="Directory to save the output JSON file.")

    args = parser.parse_args()
    job_client = JobsClient(api_key=args.api_key)
    
    try:
        os.makedirs(args.output_dir, exist_ok=True)
        
        # Set file path for output
        job_description_path = os.path.join(args.output_dir, "generated_job_description.json")
        
        # Generate job description if file doesn't exist
        if not os.path.exists(job_description_path):
            job_description = job_client.write_job_description(
                job_title=args.job_title,
                hiring_needs=args.hiring_needs,
                company_description=args.company_description,
                job_type=args.job_type,
                job_location=args.job_location,
                specific_benefits=args.specific_benefits
            )
            
            # Save the job description
            with open(job_description_path, "w") as json_file:
                json.dump(job_description, json_file, indent=4)
            print(f"Job description generated and saved to {job_description_path}")
        else:
            print(f"Using existing job description from {job_description_path}")
            with open(job_description_path, "r") as json_file:
                job_description = json.load(json_file)
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main() 