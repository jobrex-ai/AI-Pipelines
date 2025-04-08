import requests
import argparse
import os
import json
import uuid
import pandas as pd
from jobrex import ResumesClient
from jobrex import JobsClient

def main():
    parser = argparse.ArgumentParser(description="Tailoring candidate resume given a job descripiton.")
    parser.add_argument("--api_key", required=True, help="Your Jobrex API key.")
    parser.add_argument("--resume_path", required=True, help="path to the resume (pdf or docx).")
    parser.add_argument("--job_description_path", required=True, help="job description path (.txt file).")
    parser.add_argument("--output_dir", required=True, help="Path to save the output JSON file to.")

    args = parser.parse_args()
    output_path = os.path.join(args.output_dir, os.path.splitext(os.path.basename(args.resume_path))[0] + "_new_resume.json")
    job_details_path = os.path.join(args.output_dir, "job_details.json")
    resume_details_path = os.path.join(args.output_dir, os.path.splitext(os.path.basename(args.resume_path))[0] + "_resume_details.json")
    os.makedirs(args.output_dir, exist_ok=True)
    resume_client = ResumesClient(api_key=args.api_key)
    job_client = JobsClient(api_key=args.api_key)
    try:
        # Check if job details already exist
        if os.path.exists(job_details_path):
            print(f"Job details already exist at {job_details_path}, skipping job parsing...")
            with open(job_details_path, 'r') as f:
                job_details = json.load(f)
        else:
            job_details = job_client.parse_job_description(open(args.job_description_path).read())
            json.dump(job_details, open(job_details_path, "w"), indent=2)
            print(f"Job details saved to {job_details_path}")
        
        # Check if resume details already exist
        if os.path.exists(resume_details_path):
            print(f"Resume details already exist at {resume_details_path}, skipping resume parsing...")
            with open(resume_details_path, 'r') as f:
                resume_details = json.load(f)
        else:
            resume_details = resume_client.parse_resume(args.resume_path)
            json.dump(resume_details, open(resume_details_path, "w"), indent=2)
            print(f"Resume details saved to {resume_details_path}")
        
        # Check if tailored resume already exists
        if os.path.exists(output_path):
            print(f"Tailored resume already exists at {output_path}, skipping resume tailoring...")
        else:
            new_resume = resume_client.tailor_resume(user_data=resume_details["data"], job_details=job_details["data"], sections=["summary", "certifications", "experience", "education", "skills"])
            json.dump(new_resume, open(output_path, "w"), indent=2)
            print(f"Done tailoring new resume and saved to {output_path}")
    except Exception as e:
        print(f"Error: {e}")
    
if __name__ == "__main__":
    main()
