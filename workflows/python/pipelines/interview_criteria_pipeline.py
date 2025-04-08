import argparse
import os
import json
from jobrex import JobsClient

def main():
    parser = argparse.ArgumentParser(description="Generate interview criteria and/or final report from job description and interview transcript.")
    parser.add_argument("--api_key", required=True, help="Your Jobrex API key.")
    parser.add_argument("--job_description_path", required=True, help="Path to the job description file (.txt).")
    parser.add_argument("--transcript_path", help="Path to the interview transcript file (.txt), optional.")
    parser.add_argument("--output_dir", required=True, help="Directory to save the output JSON files.")

    args = parser.parse_args()
    job_client = JobsClient(api_key=args.api_key)
    
    try:
        os.makedirs(args.output_dir, exist_ok=True)
        
        # Set file paths
        job_details_path = os.path.join(args.output_dir, "parsed_job_description.json")
        criteria_path = os.path.join(args.output_dir, "interview_criteria.json")
        
        # 1. Parse job description if not already parsed
        if not os.path.exists(job_details_path):
            with open(args.job_description_path, 'r') as file:
                job_description_text = file.read()
            
            job_details = job_client.parse_job_description(job_description_text)
            
            # Save the parsed job description
            with open(job_details_path, "w") as json_file:
                json.dump(job_details, json_file, indent=4)
            print(f"Job description parsed and saved to {job_details_path}")
        else:
            print(f"Using existing parsed job description from {job_details_path}")
            with open(job_details_path, "r") as json_file:
                job_details = json.load(json_file)
        
        # 2. Generate interview criteria if not already generated
        if not os.path.exists(criteria_path):
            # Generate interview evaluation criteria based on job details
            evaluation_criteria = job_client.generate_interview_criteria(job_details)
            
            # Save the interview criteria
            with open(criteria_path, "w") as json_file:
                json.dump(evaluation_criteria, json_file, indent=4)
            print(f"Interview criteria generated and saved to {criteria_path}")
        else:
            print(f"Using existing interview criteria from {criteria_path}")
            with open(criteria_path, "r") as json_file:
                evaluation_criteria = json.load(json_file)
        
        # 3. Generate final report if transcript is provided
        if args.transcript_path:
            report_path = os.path.join(args.output_dir, "interview_report.json")
            
            if not os.path.exists(report_path):
                # Read the transcript
                with open(args.transcript_path, 'r') as file:
                    transcript_text = file.read()
                
                # Generate the final report using the criteria and transcript
                evaluation_criteria = [{"criteria_name":i["description"],**i} for i in evaluation_criteria["criteria_with_weights"]]
                final_report = job_client.generate_final_report(
                    transcript=transcript_text,
                    evaluation_criteria=evaluation_criteria
                )
                
                # Save the final report
                with open(report_path, "w") as json_file:
                    json.dump(final_report, json_file, indent=4)
                print(f"Interview report generated and saved to {report_path}")
            else:
                print(f"Using existing interview report from {report_path}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main() 