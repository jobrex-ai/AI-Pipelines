import requests
import argparse
import os
import json
import uuid
import pandas as pd
from jobrex import ResumesClient
from jobrex import JobsClient
import ast
def main():
    parser = argparse.ArgumentParser(description="Get the evauation for a lsit of candidates given a job description.")
    parser.add_argument("--api_key", required=True, help="Your Jobrex API key.")
    parser.add_argument("--job_description_path", required=True, help="job description path (.txt file).")
    parser.add_argument("--output_dir", required=True, help="Directory to save the output JSON files.")
    parser.add_argument("--top_k", type=int, default=10, help="Number of top candidates to retrieve from the search.")


    args = parser.parse_args()
    resume_client = ResumesClient(api_key=args.api_key)
    job_client = JobsClient(api_key=args.api_key)
    try:
        os.makedirs(args.output_dir, exist_ok=True)
        job_details = job_client.parse_job_description(open(args.job_description_path).read())
        json.dump(job_details,open(os.path.join(args.output_dir,"job_details.json"),"w"),indent=2)
        filters= {
        "operator": "AND",
        "conditions": [
            
        ]
        }
        custom_query = {
            "query": {
                "bool": {
                    "must": [
                        { "multi_match": {
                            "query": "$query",
                            "fields": ["content"],
                            "fuzziness": "AUTO"
                        }}
                    ],
                    "filter":"$filters"
                }
            }
        }
        candidates = resume_client.search_jobrex_resumes(query=open(args.job_description_path).read(),filters=filters,custom_query=custom_query, top_k=args.top_k)
        candidates = candidates["documents"]
        candidates = [ ast.literal_eval(c["content"]) for c in candidates]
        processed_candidates = []
        for candidate in candidates:
            candidate_data = {
                "basic_info": candidate.get("basics", {}),
                "resume_details": candidate
            }
            if "url" in candidate_data["basic_info"]:
                _ = candidate_data["basic_info"].pop("url")
            
            # Get each candidate scores and feedback
            candidate_feedback = job_client.get_candidate_score(job_details, candidate)
            candidate_data["feedback"] = candidate_feedback
            processed_candidates.append(candidate_data)
            print(f"Done with candidate {candidate_data['basic_info'].get('name', 'Unknown')}.")

        # show candidate feedback summary
        data = [{**c["basic_info"], 
                "final_score": c["feedback"]["final_score"],
                "summary_comment": c["feedback"]["summary_comment"],
                "is_accepted": c["feedback"]["is_accepted"]} for c in processed_candidates]
        df = pd.DataFrame(data)
        df.to_csv(os.path.join(args.output_dir,"feedback.csv"), index=False)
        print(f"Done with {len(processed_candidates)} candidates.")
    except Exception as e:
        print(f"Error: {e}")
    
if __name__ == "__main__":
    main()
