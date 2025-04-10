# Jobrex AI-Workflows  

**Smarter Hiring & Career Growth with AI**  

Jobrex AI-Workflows leverages LLMs, intelligent agents, and deep learning to automate and optimize recruitment processes. From resume enhancement to talent matching, Jobrex streamlines hiring for both job seekers and employers.

## Job Seeker Workflows  

**Job-Based Resume Tailoring**  
Intelligently adapts and optimizes your resume to align with specific job requirements, enhancing your chances of getting noticed by highlighting relevant qualifications and experience.

**Inputs:**  
- Candidate's resume (PDF/DOCX)  
- Job description (TXT)  

**Parameters:**
- `--api_key`: Your Jobrex API key
- `--resume_path`: Path to the candidate's resume file
- `--job_description_path`: Path to the job description file (TXT)
- `--output_dir`: Directory to save the output files

**Flow Command:**

`python ./workflows/python/pipelines/resume_tailoring_pipeline.py --api_key= <jobrex_api_key> --resume_path <Resume.pdf> --job_description_path <job_description.txt> --output_dir <output_dir>`

**Flow Expected Output:**

This workflow produces a JSON file with a tailored version of the candidate's resume, strategically optimized to match the provided job description. The customized content is provided as a recommendation that candidates can review and modify as needed.


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

**Job Description Generation**

Generate a professional job description based on provided job details and requirements.

**Parameters:**
- `--api_key`: Your Jobrex API key
- `--job_title`: Title of the job position
- `--hiring_needs`: Description of the hiring needs and requirements
- `--company_description`: Brief description of the company
- `--job_type`: Type of job (e.g., Full-time, Part-time, Contract)
- `--job_location`: Location of the job
- `--specific_benefits`: List of benefits offered
- `--output_dir`: Directory to save the output file

**Flow Command:**

`python ./workflows/python/pipelines/job_description_generation_pipeline.py --api_key=<jobrex_api_key> --job_title="Senior Software Engineer"  --hiring_needs="Looking for a skilled developer with experience in Python and machine learning." --company_description="XYZ Corp is a leading tech company."  --job_type="Full-time" --job_location="San Francisco, CA" --specific_benefits="Health insurance, 401k, and flexible hours." --output_dir=<output_dir>
`

**Flow Expected Output:**

This workflow generates a professional job description based on the provided inputs. The output includes:
- A JSON file containing the generated job description (`generated_job_description.json`)

The script intelligently skips generation if the output file already exists in the specified directory.

**Job Description and Screening Questions Generation**

Generate tailored screening questions based on a job description and candidate's resume.

**Inputs:**  
- Job description (TXT)
- Candidate's resume (PDF)  

**Parameters:**
- `--api_key`: Your Jobrex API key
- `--resume_path`: Path to the candidate's resume file (.pdf)
- `--job_description_path`: Path to the job description file (.txt)
- `--output_dir`: Directory to save the output files

**Flow Command:**

`python ./workflows/python/pipelines/job_description_screening_pipeline.py --api_key= <jobrex_api_key> --resume_path <Resume.pdf> --job_description_path <job_description.txt> --output_dir <output_dir>`

**Flow Expected Output:**

This workflow:
1. Reads and parses the provided job description into structured data
2. Parses the provided resume to extract structured information
3. Generates relevant screening questions based on the parsed job and resume data

The output includes:
- A JSON file with the structured job description data (`parsed_job.json`)
- A JSON file with the structured resume data (`parsed_resume.json`)
- A JSON file containing tailored screening questions based on the parsed data (`screening_questions.json`)

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
