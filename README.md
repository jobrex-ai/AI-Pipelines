# Jobrex AI-Workflows  

**Smarter Hiring & Career Growth with AI**  

Jobrex AI-Workflows leverages LLMs, intelligent agents, and deep learning to automate and optimize recruitment processes. From resume enhancement to talent matching, Jobrex streamlines hiring for both job seekers and employers.

## Meeting Transcripts

**Zoom Meeting Transcript Extraction**  
Automatically extract transcripts from recorded Zoom meetings.

**Inputs:**  
- Zoom Meeting ID
- Zoom API Key

**Parameters:**
- `--api_key`: Your Zoom API key
- `--meeting_id`: ID of the Zoom meeting to get transcript from
- `--output_dir`: Directory to save the output files

**Flow Command:**

`python ./workflows/python/pipelines/zoom_transcript_pipeline.py --api_key <zoom_api_key> --meeting_id <meeting_id> --output_dir <output_dir>`

**Flow Expected Output:**

This workflow generates a text file containing the full transcript of the Zoom meeting, including speaker labels. The output file will be named `meeting_<meeting_id>_transcript.txt`.

## Job Seeker Workflows  

**Job-Based Resume Tailoring**  
Automatically customize a resume to match a specific job description, improving application relevance.

**Inputs:**  
- Candidate's resume (PDF/DOCX)  
- Job description (TXT)  

**Parameters:**
- `--api_key`: Your Jobrex API key
- `--resume_path`: Path to the candidate's resume file
- `--job_description_path`: Path to the job description file
- `--output_dir`: Directory to save the output files

**Flow Command:**

`python ./workflows/python/pipelines/resume_tailoring_pipeline.py --api_key= <jobrex_api_key> --resume_path <Resume.pdf> --job_description_path <job_description.txt> --output_dir <output_dir>`

**Flow Expected Output:**

This workflow generates a JSON file containing a customized version of the candidate's resume, optimized to align with the provided job description.


## Recruitment Workflows  

**Job-Based Candidates Scoring**  

Automatically evaluate your candidate list against the provided job description. This helps sort candidates based on how well their resumes match the job requirements and can also eliminate those with lower matching scores.

**Inputs:**  
- Candidates' resumes (PDF/DOCX)  
- Job description (TXT)  

**Parameters:**
- `--api_key`: Your Jobrex API key
- `--resumes_dir`: Directory containing candidate resumes
- `--job_description_path`: Path to the job description file
- `--output_dir`: Directory to save the output files

**Flow Command:**

`python ./workflows/python/pipelines/job_fit_pipeline.py --api_key= <jobrex_api_key> --resumes_dir <Resumes_dir> --job_description_path <job_description.txt> --output_dir <output_dir>`

**Flow Expected Output:**

This workflow parsed candidates' resumes and dumps their details as JSON files into `<output_dir>/resumes_details/` and evaluats each candidate resume against the input job description. The fianl output is sheet conatins a summary of the evaluated candidates in th following format:

|Name|Headline|Email|Phone|Location|Final Score|Summary Comment|Is accepted?|
|----|--------|-----|-----|--------|-----------|---------------|------------|
|Candidate's name|Candidate's headline|candidate's email|Candidate's phone number|Candidate's location|Matching score|Overall comment over the candidate's resume|Yes/No|

**Job-Based Candidates Search & Scoring from Jobrex Pool**  

Search and evaluate candidates from the Jobrex talent pool against a provided job description. This helps find and score relevant candidates based on how well their profiles match the job requirements.

**Inputs:**  
- Job description (TXT)  

**Parameters:**
- `--api_key`: Your Jobrex API key
- `--job_description_path`: Path to the job description file
- `--output_dir`: Directory to save the output files
- `--top_k`: Number of top candidates to retrieve and evaluate (default: 10)

**Flow Command:**

`python ./workflows/python/pipelines/job_fit_from_pool.py --api_key= <jobrex_api_key> --job_description_path <job_description.txt> --output_dir <output_dir> --top_k <number_of_candidates>`

**Flow Expected Output:**

This workflow searches the Jobrex talent pool for candidates matching the job description and evaluates each candidate's profile. The output includes:
- A list of matching candidates from the Jobrex pool
- Evaluation scores and feedback for each candidate
- A summary CSV file containing candidate details and scores in the following format:

|Name|Headline|Email|Phone|Location|Final Score|Summary Comment|Is accepted?|
|----|--------|-----|-----|--------|-----------|---------------|------------|
|Candidate's name|Candidate's headline|candidate's email|Candidate's phone number|Candidate's location|Matching score|Overall comment on the candidate's profile|Yes/No|

**Job Description and Screening Questions Generation**

Generate a professional job description and create tailored screening questions based on a candidate's resume.

**Inputs:**  
- Candidate's resume (PDF)  

**Parameters:**
- `--api_key`: Your Jobrex API key
- `--resume_path`: Path to the candidate's resume file (.pdf)
- `--output_dir`: Directory to save the output files

**Flow Command:**

`python ./workflows/python/pipelines/job_description_screening_pipeline.py --api_key= <jobrex_api_key> --resume_path <Resume.pdf> --output_dir <output_dir>`

**Flow Expected Output:**

This workflow:
1. Creates a detailed job description for using artificial data
2. Parses the provided resume to extract structured information
3. Generates relevant screening questions based on the job description and candidate's resume

The output includes:
- A JSON file with the complete job description (`job_description.json`)
- A JSON file with the structured data from the parsed resume (`parsed_resume.json`)
- A JSON file containing tailored screening questions based on the job and resume (`screening_questions.json`)

The script intelligently skips any steps where output files already exist in the specified directory.

**Interview Criteria and Report Generation**

Generate interview evaluation criteria from a job description and optionally create a final interview report using a transcript.

**Inputs:**  
- Job description (TXT) - required  
- Interview transcript (TXT) - optional  

**Parameters:**
- `--api_key`: Your Jobrex API key
- `--job_description_path`: Path to the job description file (.txt)
- `--transcript_path`: Path to the interview transcript file (.txt) - optional
- `--output_dir`: Directory to save the output files

**Flow Command:**

For generating just the interview criteria:
`python ./workflows/python/pipelines/interview_criteria_pipeline.py --api_key= <jobrex_api_key> --job_description_path <job_description.txt> --output_dir <output_dir>`

For generating both criteria and a final report:
`python ./workflows/python/pipelines/interview_criteria_pipeline.py --api_key= <jobrex_api_key> --job_description_path <job_description.txt> --transcript_path <interview_transcript.txt> --output_dir <output_dir>`

**Flow Expected Output:**

This workflow:
1. Parses the job description to extract structured information
2. Generates interview evaluation criteria based on the job requirements
3. Optionally produces a final interview report if a transcript is provided

The output includes:
- A JSON file with the parsed job description (`parsed_job_description.json`)
- A JSON file with the interview evaluation criteria (`interview_criteria.json`)
- A JSON file with the final interview report if a transcript was provided (`interview_report.json`)

The script intelligently skips any steps where output files already exist in the specified directory.
