import re
from config.websites import WEBSITES


def create_plan(command):

    command = command.lower().strip()

    # 1. LinkedIn Post Creation Intent
    if ("post" in command or "share" in command) and re.search(r"linke?din", command):
        project_name = None
        proj_match = re.search(r"(?:for|about)\s+(?:my\s+)?(?:latest\s+)?(.+)", command)
        if proj_match:
            project_name = proj_match.group(1).strip()
            project_name = re.sub(r"\s+on\s+linke?din.*", "", project_name).strip()

        return [
            {
                "tool": "create_linkedin_post",
                "arguments": {
                    "text": None,
                    "project_name": project_name,
                    "auto_publish": False
                }
            }
        ]

    # 2. LinkedIn Profile Update Intent (headline, description, about)
    if ("headline" in command or "headlight" in command or "about" in command or "description" in command) and ("profile" in command or re.search(r"linke?din", command)):
        headline = None
        about = None
        to_match = re.search(r"(?:to|as)\s+[\"']?(.+?)[\"']?$", command)
        target_val = to_match.group(1).strip() if to_match else None

        if "headline" in command or "headlight" in command:
            headline = target_val
        elif "about" in command or "description" in command:
            about = target_val

        return [
            {
                "tool": "update_linkedin_profile",
                "arguments": {
                    "headline": headline,
                    "about": about,
                    "auto_save": True
                }
            }
        ]

    # 3. LinkedIn Job Review & Easy Apply Intent (Step 3)
    if any(p in command for p in ["apply for this job", "apply to this job", "apply this job", "easy apply for this"]):
        return [
            {
                "tool": "open_linkedin_job",
                "arguments": {
                    "job_index": 1,
                    "click_easy_apply": True
                }
            }
        ]

    apply_match = re.search(r"(?:open|view|review|apply(?:\s+to)?)\s+job\s*(?:page\s*)?(?:#|number\s*)?(\d+)", command)
    if not apply_match and "easy apply" in command:
        num_m = re.search(r"\b(\d+)\b", command)
        if num_m:
            apply_match = num_m

    if apply_match:
        job_idx = int(apply_match.group(1))
        is_apply = any(w in command for w in ["apply", "easy apply", "submission"])
        return [
            {
                "tool": "open_linkedin_job",
                "arguments": {
                    "job_index": job_idx,
                    "click_easy_apply": is_apply
                }
            }
        ]

    # 4. LinkedIn Job Search & CV Curation Intent (Steps 1 & 2)
    is_job_search = False
    if (re.search(r"linke?din", command) and any(w in command for w in ["job", "jobs", "internship", "work", "hiring"])) or (
        any(w in command for w in ["job", "jobs", "internship", "internships"]) and any(w in command for w in ["search", "find", "curate", "get", "look for", "matching", "csv", "excel", "list"])
    ) or (
        "job" in command and any(w in command for w in ["cv", "resume", "curate", "matching", "csv", "excel", "relevant"])
    ):
        is_job_search = True

    if is_job_search:
        keywords = ""
        location = "Remote"
        limit = 10

        # Check for limit (e.g. "top 10", "top 5", "5 jobs", "10 jobs")
        limit_match = re.search(r"(?:top\s+|limit\s+)?(\d+)\s*(?:most\s+relevant\s+)?jobs?", command)
        if limit_match:
            try:
                cand_limit = int(limit_match.group(1))
                if 1 <= cand_limit <= 25:
                    limit = cand_limit
            except Exception:
                pass

        # Check for location specification
        loc_match = re.search(r"\bin\s+([a-zA-Z\s]+?)(?:\s+on\s+linke?din|\s+for\s+me|\s+matching|\s+save|\s+as|$)", command)
        if loc_match:
            cand_loc = loc_match.group(1).strip()
            if cand_loc.lower() not in ["laptop", "pc", "computer", "csv", "excel", "file", "folder"]:
                location = cand_loc

        # Check if CV matching requested
        if any(cv_kw in command for cv_kw in ["matching your cv", "matching my cv", "for my cv", "matching cv", "according to my cv", "relevant to me"]):
            keywords = ""
        else:
            # Extract keyword (e.g. "search job for junior ai/ml engineer", "search python jobs")
            kw_match = re.search(r"(?:search|find|curate)\s+(?:jobs?\s+for\s+|job\s+for\s+|for\s+)?(.+?)(?:\s+on\s+linke?din|\s+in\s+.*|\s+jobs?|$)", command)
            if kw_match:
                cand = kw_match.group(1).strip()
                cand = re.sub(r"\s+on\s+linke?din.*", "", cand)
                cand = re.sub(r"\s+in\s+.*", "", cand)
                if cand not in ["me", "us", "some", "the", "10", "top 10", "top 5"]:
                    keywords = cand

            if not keywords:
                for_match = re.search(r"\bfor\s+([a-zA-Z0-9\s\+\#\/\-]+)", command)
                if for_match:
                    cand = for_match.group(1).strip()
                    cand = re.sub(r"\s+on\s+linke?din.*", "", cand)
                    if cand not in ["me", "us", "my cv", "your cv"]:
                        keywords = cand

        return [
            {
                "tool": "search_linkedin_jobs",
                "arguments": {
                    "keywords": keywords,
                    "location": location,
                    "limit": limit
                }
            }
        ]

    steps = []

    for name, url in WEBSITES.items():


        if name in command:

            steps.append(

                {

                    "tool": "start_browser",

                    "arguments": {}

                }

            )

            steps.append(

                {

                    "tool": "open_website",

                    "arguments": {

                        "url": url

                    }

                }

            )

            break

    if "search" in command:

        query = command.split(

            "search",

            1

        )[1].strip()

        steps.append(

            {

                "tool": "search_google",

                "arguments": {

                    "query": query

                }

            }

        )

    return steps