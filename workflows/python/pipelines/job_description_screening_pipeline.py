import argparse
import os
import json
from jobrex import ResumesClient
from jobrex import JobsClient

def main():
    parser = argparse.ArgumentParser(description="Generate a job description and screening questions.")
    parser.add_argument("--api_key", required=True, help="Your Jobrex API key.")
    parser.add_argument("--resume_path", required=True, help="Path to the resume file (.pdf).")
    parser.add_argument("--output_dir", required=True, help="Directory to save the output JSON files.")

    args = parser.parse_args()
    resume_client = ResumesClient(api_key=args.api_key)
    job_client = JobsClient(api_key=args.api_key)
    
    try:
        os.makedirs(args.output_dir, exist_ok=True)
        
        # 1. Create artificial data for a Java position
        java_job_data = {
            "job_title": "Senior Java Developer",
            "hiring_needs": "We are looking for an experienced Java developer to join our team. The ideal candidate should have strong expertise in Java, Spring Boot, and microservices architecture. Experience with cloud platforms like AWS or Azure is a plus.",
            "company_description": "TechInnovate is a leading software development company specializing in enterprise solutions. We create cutting-edge applications that help businesses streamline their operations and achieve digital transformation.",
            "job_type": "Full-time",
            "job_location": "Remote with occasional travel to headquarters",
            "specific_benefits": "Competitive salary, health insurance, flexible work hours, professional development opportunities, and annual team retreats."
        }
        
        # Set file paths
        job_description_path = os.path.join(args.output_dir, "java_job_description.json")
        resume_output_path = os.path.join(args.output_dir, "parsed_resume.json")
        questions_path = os.path.join(args.output_dir, "screening_questions.json")
        
        # 2. Generate job description if file doesn't exist
        if not os.path.exists(job_description_path):
            job_description = job_client.write_job_description(
                job_title=java_job_data["job_title"],
                hiring_needs=java_job_data["hiring_needs"],
                company_description=java_job_data["company_description"],
                job_type=java_job_data["job_type"],
                job_location=java_job_data["job_location"],
                specific_benefits=java_job_data["specific_benefits"]
            )
            
            # Save the job description
            with open(job_description_path, "w") as json_file:
                json.dump(job_description, json_file, indent=4)
            print(f"Job description generated and saved to {job_description_path}")
        else:
            print(f"Using existing job description from {job_description_path}")
            with open(job_description_path, "r") as json_file:
                job_description = json.load(json_file)
        
        # 3. Parse the resume if file doesn't exist
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
        
        # 4. Generate screening questions if file doesn't exist
        if not os.path.exists(questions_path):
            screening_questions = job_client.generate_screening_questions(
                resume_data["data"],
                job_description
                
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