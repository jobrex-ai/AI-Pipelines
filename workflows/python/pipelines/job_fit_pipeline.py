import requests
import argparse
import os
import json
import uuid
import pandas as pd
from jobrex import ResumesClient
from jobrex import JobsClient

def main():
    parser = argparse.ArgumentParser(description="Get the evauation for a lsit of candidates given a job description.")
    parser.add_argument("--api_key", required=True, help="Your Jobrex API key.")
    parser.add_argument("--resumes_dir", required=True, help="Directory contains resumes files.")
    parser.add_argument("--job_description_path", required=True, help="job description path (.txt file).")
    parser.add_argument("--output_dir", required=True, help="Directory to save the output JSON files.")


    args = parser.parse_args()
    resume_client = ResumesClient(api_key=args.api_key)
    job_client = JobsClient(api_key=args.api_key)
    resumes_paths = [os.path.join(args.resumes_dir,i) for i in os.listdir(args.resumes_dir) if i.split(".")[-1].lower() in ["docx","pdf"]]
    try:
        os.makedirs(args.output_dir, exist_ok=True)
        os.makedirs(args.output_dir+"/resumes_details/", exist_ok=True)
        job_details = job_client.parse_job_description(open(args.job_description_path).read())
        json.dump(job_details,open(os.path.join(args.output_dir,"job_details.json"),"w"),indent=2)
        candidates = []
        for resume_path in resumes_paths:
            output_path = os.path.join(args.output_dir,"resumes_details", os.path.splitext(os.path.basename(resume_path))[0] + ".json")
            if not os.path.exists(output_path):
                response = resume_client.parse_resume(resume_path)
                with open(output_path, "w") as json_file:
                    json.dump(response, json_file, indent=2)
            else:
                response = json.load(open(output_path))
            candidate_data = {
                    "resume_path": resume_path,
                    "resume_details_path": output_path,
                    "basic_info": response["data"]["basics"],
                    "resume_details": response["data"]}
            _ = candidate_data["basic_info"].pop("url")
            # Get each candidate scores and feedback
            candidate_feedback = job_client.get_candidate_score(job_details,response)
            candidate_data["feedback"] = candidate_feedback
            candidates.append(candidate_data)
            print(f"Done with {resume_path} candidate.")
        # show candidate feedback summary
        data = [{**c["basic_info"],"final_score":c["feedback"]["final_score"],"summary_comment":c["feedback"]["summary_comment"],
                 "is_accepted":c["feedback"]["is_accepted"],} for c in candidates]
        df = pd.DataFrame(data)
        df.to_csv(os.path.join(args.output_dir,"feedback.csv"),index=False)
        print(f"Done with {len(candidates)} candidates.")
    except Exception as e:
        print(f"Error: {e}")
    
if __name__ == "__main__":
    main()
