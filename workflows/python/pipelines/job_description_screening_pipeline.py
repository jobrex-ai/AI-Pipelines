import argparse
import os
import json
from jobrex import ResumesClient
from jobrex import JobsClient

def main():
    parser = argparse.ArgumentParser(description="Generate screening questions based on a resume and job description.")
    parser.add_argument("--api_key", required=True, help="Your Jobrex API key.")
    parser.add_argument("--resume_path", required=True, help="Path to the resume file (.pdf).")
    parser.add_argument("--job_description_path", required=True, help="Path to the job description file (.txt).")
    parser.add_argument("--output_dir", required=True, help="Directory to save the output JSON files.")

    args = parser.parse_args()
    resume_client = ResumesClient(api_key=args.api_key)
    job_client = JobsClient(api_key=args.api_key)
    
    try:
        os.makedirs(args.output_dir, exist_ok=True)
        
        # Set file paths
        resume_output_path = os.path.join(args.output_dir, "parsed_resume.json")
        job_output_path = os.path.join(args.output_dir, "parsed_job.json")
        questions_path = os.path.join(args.output_dir, "screening_questions.json")
        
        # 1. Read and parse the job description
        with open(args.job_description_path, "r") as file:
            job_description_text = file.read()
            print(f"Job description loaded from {args.job_description_path}")
        
        if not os.path.exists(job_output_path):
            parsed_job = job_client.parse_job_description(job_description_text)
            # Save the parsed job
            with open(job_output_path, "w") as json_file:
                json.dump(parsed_job, json_file, indent=4)
            print(f"Job description parsed and saved to {job_output_path}")
        else:
            print(f"Using existing parsed job from {job_output_path}")
            with open(job_output_path, "r") as json_file:
                parsed_job = json.load(json_file)
        
        # 2. Parse the resume if file doesn't exist
        if not os.path.exists(resume_output_path):
            resume_data = resume_client.parse_resume(args.resume_path)
            # Save the parsed resume
            with open(resume_output_path, "w") as json_file:
                json.dump(resume_data, json_file, indent=4)
            print(f"Resume parsed and saved to {resume_output_path}")
        else:
            print(f"Using existing parsed resume from {resume_output_path}")
            with open(resume_output_path, "r") as json_file:
                resume_data = json.load(json_file)
        
        # 3. Generate screening questions if file doesn't exist
        if not os.path.exists(questions_path):
            screening_questions = job_client.generate_screening_questions(
                resume_data["data"],
                parsed_job
            )
            
            # Save the screening questions
            with open(questions_path, "w") as json_file:
                json.dump(screening_questions, json_file, indent=4)
            print(f"Screening questions generated and saved to {questions_path}")
        else:
            print(f"Using existing screening questions from {questions_path}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main() 