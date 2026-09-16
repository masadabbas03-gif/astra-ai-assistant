import re
from config.websites import WEBSITES


def create_plan(command):

    command = command.lower().strip()

    # 1. LinkedIn Job Review & Easy Apply Intent (Step 3)
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

    # 2. LinkedIn Job Search & CV Curation Intent (Steps 1 & 2)
    is_job_search = False
    if ("linkedin" in command and any(w in command for w in ["job", "jobs", "internship", "work", "hiring"])) or (
        any(w in command for w in ["job", "jobs", "internship", "internships"]) and any(w in command for w in ["search", "find", "curate", "get", "look for", "matching", "csv", "excel", "list"])
    ) or (
        "job" in command and any(w in command for w in ["cv", "resume", "curate", "matching", "csv", "excel"])
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

        # Check for location specification (e.g. "in Pakistan", "in USA", "in Lahore")
        loc_match = re.search(r"\bin\s+([a-zA-Z\s]+?)(?:\s+on\s+linkedin|\s+for\s+me|\s+matching|$)", command)
        if loc_match:
            location = loc_match.group(1).strip()

        # Check if CV matching requested
        if any(cv_kw in command for cv_kw in ["matching your cv", "matching my cv", "for my cv", "matching cv", "according to my cv"]):
            keywords = ""
        else:
            # Extract keyword (e.g. "search python developer jobs on linkedin")
            kw_match = re.search(r"(?:search|find|curate)\s+(?:for\s+)?(.+?)\s+(?:jobs?|internships?)", command)
            if kw_match:
                cand = kw_match.group(1).strip()
                if cand not in ["me", "us", "some", "the", "10", "top 10", "top 5"]:
                    keywords = cand

            if not keywords:
                # Check "for <keyword>" e.g. "search jobs on linkedin for python"
                for_match = re.search(r"\bfor\s+([a-zA-Z0-9\s\+\#]+)", command)
                if for_match:
                    cand = for_match.group(1).strip()
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