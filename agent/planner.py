import re
from config.websites import WEBSITES

# Bilingual Urdu Script and Roman Urdu Normalization Rules
URDU_NORMALIZATION = [
    # Urdu Script
    (r"یوٹیوب", "youtube"),
    (r"لنکڈان|لنکڈ ان|لنکڈن", "linkedin"),
    (r"گوگل", "google"),
    (r"واٹس ایپ|واٹسایپ", "whatsapp"),
    (r"گٹ ہب", "github"),
    (r"کھولو|کھولیں|کھول دو", "open"),
    (r"بند کرو|بند کریں", "close"),
    (r"تلاش کرو|ڈھونڈو|سرچ کرو", "search"),
    (r"جابز?|ملازمت", "jobs"),
    (r"نوٹ پیڈ", "notepad"),
    (r"کیلکولیٹر", "calculator"),
    (r"آواز بڑھاؤ|آواز تیز کرو", "volume up"),
    (r"آواز کم کرو|آواز دھیمی کرو", "volume down"),
    (r"آواز بند کرو|میوٹ کرو", "mute"),
    (r"لاک کرو|اسکرین لاک", "lock laptop"),
    (r"اسکرین شاٹ", "take screenshot"),
    (r"بیٹری", "battery"),

    # Compound volume phrases
    (r"\b(awaz|aawaz|volume|sound)\s+(band\s+karo|off\s+karo|mute\s+karo|band)\b", "mute volume"),
    (r"\b(awaz|aawaz|volume|sound)\s+(kholo|on\s+karo|unmute\s+karo)\b", "unmute volume"),

    # Roman Urdu phrases
    (r"\bkholo\b|\bkhol do\b|\bopen karo\b", "open"),
    (r"\bband karo\b|\bclose karo\b", "close"),
    (r"\bdhundo\b|\bdhund do\b|\btalash karo\b|\bsearch karo\b", "search"),
    (r"\bmera?\s+liye\b|\bmere\s+liye\b", "for me"),
    (r"\bki\s+jobs?\b", "jobs"),
    (r"\bka\s+status\b", "status"),
    (r"\bchalao\b|\blagao\b", "play"),
    (r"\bteez\s+karo\b|\bbarhao\b|\bbadha do\b", "up"),
    (r"\bkam\s+karo\b|\bdheemi\s+karo\b|\bghata do\b", "down"),
    (r"\bawaz\b|\baawaz\b", "volume"),
]


def normalize_bilingual_command(text: str) -> str:
    """Normalizes Urdu script and Roman Urdu to canonical command keywords."""
    res = text.strip()
    for pat, rep in URDU_NORMALIZATION:
        res = re.sub(pat, rep, res, flags=re.IGNORECASE)
    return res


def create_plan(command):
    if not command:
        return []

    # Normalize Urdu/Roman Urdu and typos
    normalized = normalize_bilingual_command(command)
    cmd = normalized.lower().strip()

    # Normalize common typos
    cmd = re.sub(r"\blinkdin\b", "linkedin", cmd)

    # =========================================================
    # 1. Laptop & System Automation (Volume, Battery, Lock, etc.)
    # =========================================================
    if re.search(r"\b(volume|sound)\s+(up|increase|raise|high)\b", cmd) or cmd in ["volume up", "sound up"]:
        return [{"tool": "volume_up", "arguments": {"step": 10}}]

    if re.search(r"\b(volume|sound)\s+(down|decrease|lower|low)\b", cmd) or cmd in ["volume down", "sound down"]:
        return [{"tool": "volume_down", "arguments": {"step": 10}}]

    if "unmute" in cmd or re.search(r"\b(volume|sound)\s+(on|unmute)\b", cmd):
        return [{"tool": "unmute_volume", "arguments": {}}]

    if (re.search(r"\b(mute|silent)\b", cmd) or "volume mute" in cmd or "mute volume" in cmd) and "unmute" not in cmd:
        return [{"tool": "mute_volume", "arguments": {}}]

    set_vol_m = re.search(r"(?:set\s+)?volume\s+(?:to\s+)?(\d{1,3})(?:%|percent)?", cmd)
    if set_vol_m:
        val = int(set_vol_m.group(1))
        if 0 <= val <= 100:
            return [{"tool": "set_volume", "arguments": {"level_percent": val}}]

    if "battery" in cmd:
        return [{"tool": "get_battery_status", "arguments": {}}]

    if any(k in cmd for k in ["system stats", "system status", "cpu ram", "cpu usage", "ram usage", "performance"]):
        return [{"tool": "get_system_stats", "arguments": {}}]

    if any(k in cmd for k in ["lock laptop", "lock screen", "lock pc", "laptop lock", "screen lock"]):
        return [{"tool": "lock_laptop", "arguments": {}}]

    if any(k in cmd for k in ["screenshot", "screen capture", "take screenshot"]):
        return [{"tool": "take_desktop_screenshot", "arguments": {}}]

    if any(k in cmd for k in ["notepad", "open notepad"]):
        return [{"tool": "open_notepad", "arguments": {}}]

    if any(k in cmd for k in ["calculator", "open calculator"]):
        return [{"tool": "open_calculator", "arguments": {}}]

    # =========================================================
    # 2. LinkedIn Post Creation Intent
    # =========================================================
    if ("post" in cmd or "share" in cmd) and re.search(r"linke?din", cmd):
        project_name = None
        proj_match = re.search(r"(?:for|about)\s+(?:my\s+)?(?:latest\s+)?(.+)", cmd)
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

    # =========================================================
    # 3. LinkedIn Profile Update Intent (headline, description, about)
    # =========================================================
    if ("headline" in cmd or "headlight" in cmd or "about" in cmd or "description" in cmd) and ("profile" in cmd or re.search(r"linke?din", cmd)):
        headline = None
        about = None
        to_match = re.search(r"(?:to|as)\s+[\"']?(.+?)[\"']?$", cmd)
        target_val = to_match.group(1).strip() if to_match else None

        if "headline" in cmd or "headlight" in cmd:
            headline = target_val
        elif "about" in cmd or "description" in cmd:
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

    # =========================================================
    # 4. LinkedIn Job Review & Easy Apply Intent (Step 3)
    # =========================================================
    if any(p in cmd for p in ["apply for this job", "apply to this job", "apply this job", "easy apply for this"]):
        return [
            {
                "tool": "open_linkedin_job",
                "arguments": {
                    "job_index": 1,
                    "click_easy_apply": True
                }
            }
        ]

    apply_match = re.search(r"(?:open|view|review|apply(?:\s+to)?)\s+job\s*(?:page\s*)?(?:#|number\s*)?(\d+)", cmd)
    if not apply_match and "easy apply" in cmd:
        num_m = re.search(r"\b(\d+)\b", cmd)
        if num_m:
            apply_match = num_m

    if apply_match:
        job_idx = int(apply_match.group(1))
        is_apply = any(w in cmd for w in ["apply", "easy apply", "submission"])
        return [
            {
                "tool": "open_linkedin_job",
                "arguments": {
                    "job_index": job_idx,
                    "click_easy_apply": is_apply
                }
            }
        ]

    # =========================================================
    # 5. LinkedIn Job Search & CV Curation Intent (Steps 1 & 2)
    # =========================================================
    is_job_search = False
    if (re.search(r"linke?din", cmd) and any(w in cmd for w in ["job", "jobs", "internship", "work", "hiring"])) or (
        any(w in cmd for w in ["job", "jobs", "internship", "internships"]) and any(w in cmd for w in ["search", "find", "curate", "get", "look for", "matching", "csv", "excel", "list"])
    ) or (
        "job" in cmd and any(w in cmd for w in ["cv", "resume", "curate", "matching", "csv", "excel", "relevant"])
    ):
        is_job_search = True

    if is_job_search:
        keywords = ""
        location = "Remote"
        limit = 10

        # Check for limit (e.g. "top 10", "top 5", "5 jobs", "10 jobs")
        limit_match = re.search(r"(?:top\s+|limit\s+)?(\d+)\s*(?:most\s+relevant\s+)?jobs?", cmd)
        if limit_match:
            try:
                cand_limit = int(limit_match.group(1))
                if 1 <= cand_limit <= 25:
                    limit = cand_limit
            except Exception:
                pass

        # Check for location specification
        loc_match = re.search(r"\bin\s+([a-zA-Z\s]+?)(?:\s+on\s+linke?din|\s+for\s+me|\s+matching|\s+save|\s+as|$)", cmd)
        if loc_match:
            cand_loc = loc_match.group(1).strip()
            if cand_loc.lower() not in ["laptop", "pc", "computer", "csv", "excel", "file", "folder"]:
                location = cand_loc

        # Check if CV matching requested
        if any(cv_kw in cmd for cv_kw in ["matching your cv", "matching my cv", "for my cv", "matching cv", "according to my cv", "relevant to me"]):
            keywords = ""
        else:
            # Extract keyword (e.g. "search job for junior ai/ml engineer", "search python jobs")
            kw_match = re.search(r"(?:search|find|curate)\s+(?:jobs?\s+for\s+|job\s+for\s+|for\s+)?(.+?)(?:\s+on\s+linke?din|\s+in\s+.*|\s+jobs?|$)", cmd)
            if kw_match:
                cand = kw_match.group(1).strip()
                cand = re.sub(r"\s+on\s+linke?din.*", "", cand)
                cand = re.sub(r"\s+in\s+.*", "", cand)
                if cand not in ["me", "us", "some", "the", "10", "top 10", "top 5"]:
                    keywords = cand

            if not keywords:
                for_match = re.search(r"\bfor\s+([a-zA-Z0-9\s\+\#\/\-]+)", cmd)
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

    # =========================================================
    # 6. Browser & Website Intents
    # =========================================================
    if any(k in cmd for k in ["close browser", "exit browser", "browser close"]):
        return [{"tool": "close_browser", "arguments": {}}]

    steps = []
    for name, url in WEBSITES.items():
        if name in cmd:
            steps.append({"tool": "start_browser", "arguments": {}})
            steps.append({"tool": "open_website", "arguments": {"url": url}})
            return steps

    if "search" in cmd:
        query = cmd.split("search", 1)[1].strip()
        if query:
            steps.append({"tool": "start_browser", "arguments": {}})
            steps.append({"tool": "search_google", "arguments": {"query": query}})
            return steps

    return []