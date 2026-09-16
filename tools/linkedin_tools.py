import csv
import json
import os
import re
import urllib.parse
from datetime import datetime

from agent.profile import load_profile
from tools.browser_tools import get_browser_page
from voice.speaker import speak


def load_cv_profile():
    """
    Loads candidate CV details from data/cv.json, data/cv.txt,
    or falls back to memory/profile.json with intelligent defaults.
    """
    cv_json_path = os.path.join("data", "cv.json")
    if os.path.exists(cv_json_path):
        try:
            with open(cv_json_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[CV Loader] Error reading {cv_json_path}: {e}")

    # Check for raw text CV
    cv_txt_path = os.path.join("data", "cv.txt")
    if os.path.exists(cv_txt_path):
        try:
            with open(cv_txt_path, "r", encoding="utf-8") as f:
                content = f.read()
            # Extract basic skills from text
            skills = []
            for skill in [
                "Python", "Machine Learning", "Deep Learning", "Artificial Intelligence",
                "Playwright", "LLM", "LangChain", "PyTorch", "TensorFlow", "NLP",
                "Computer Vision", "FastAPI", "Flask", "SQL", "Git", "Automation"
            ]:
                if re.search(r"\b" + re.escape(skill) + r"\b", content, re.IGNORECASE):
                    skills.append(skill)
            return {
                "name": "Muhammad Assad Abbas",
                "profession": "AI Engineer & Python Developer",
                "target_roles": ["AI Engineer", "Machine Learning Engineer", "Python Developer"],
                "skills": skills if skills else ["Python", "Machine Learning", "AI", "Automation"],
                "preferred_location": "Remote",
                "experience_level": "Entry Level / Internship / Junior"
            }
        except Exception as e:
            print(f"[CV Loader] Error reading {cv_txt_path}: {e}")

    # Fallback to profile.json
    profile = load_profile()
    profession = profile.get("profession", "AI Student")
    goals = profile.get("goals", [])
    target_roles = ["AI Engineer", "Machine Learning Engineer", "Python Developer"]
    if "internship" in " ".join(goals).lower():
        target_roles.append("AI Intern")

    return {
        "name": profile.get("name", "Muhammad Assad Abbas"),
        "profession": profession,
        "target_roles": target_roles,
        "skills": [
            "Python", "Machine Learning", "Deep Learning", "Artificial Intelligence",
            "Playwright", "Agentic AI", "LLM", "LangChain", "PyTorch", "Automation"
        ],
        "preferred_location": "Remote",
        "experience_level": "Entry Level / Internship / Junior"
    }


def score_job_against_cv(title, company, card_text, cv):
    """
    Computes a relevance match score (0-100%) between a job listing
    and the candidate's CV profile (roles, skills, experience level).
    """
    title_lower = title.lower()
    full_text = f"{title} {company} {card_text}".lower()

    # Base match score for matching query
    score = 45
    matched_skills = []

    # 1. Target Role Title Matching (+15 to +30 points)
    target_roles = cv.get("target_roles", [])
    role_matched = False
    for role in target_roles:
        words = [w.lower() for w in role.split() if len(w) > 2]
        if all(w in title_lower for w in words):
            score += 30
            matched_skills.append(role)
            role_matched = True
            break
        elif any(w in title_lower for w in words):
            score += 15
            matched_skills.append(role)
            role_matched = True
            break

    if not role_matched and any(kw in title_lower for kw in ["developer", "engineer", "scientist", "analyst"]):
        score += 10

    # 2. Key Technical Skills Matching (+5 per matched skill)
    skills = cv.get("skills", [])
    for skill in skills:
        pattern = r"\b" + re.escape(skill.lower()) + r"\b"
        if re.search(pattern, full_text):
            if skill not in matched_skills:
                matched_skills.append(skill)
            score += 5

    # 3. Experience Level Alignment (+15 or -15)
    exp_level = cv.get("experience_level", "").lower()
    if any(lvl in exp_level for lvl in ["entry", "intern", "junior", "student"]):
        if any(w in title_lower for w in ["junior", "intern", "internship", "graduate", "trainee", "entry"]):
            score += 15
            matched_skills.append("Junior/Intern")
        elif any(w in title_lower for w in ["lead", "principal", "director", "head of", "vp", "architect", "senior"]):
            score -= 15

    # 4. Cap score cleanly between 40% and 98%
    score = max(40, min(score, 98))

    return score, matched_skills


def search_linkedin_jobs(keywords=None, location=None, limit=10):
    """
    Step 1: Searches & curates the top 10 most relevant jobs matching your CV.
    Step 2: Saves them to a neat CSV/Excel file and Markdown report.
    """
    profile = load_profile()
    nickname = profile.get("nickname", "Boss")
    cv = load_cv_profile()

    # Determine targeted search keywords from CV if not provided or generic
    generic_queries = ["jobs", "job", "work", "find jobs", "search jobs", "matching my cv", "cv", "matching cv", "my cv", "for me"]
    if not keywords or keywords.strip().lower() in generic_queries:
        target_role = cv.get("target_roles", ["AI Engineer"])[0]
        keywords = f"{target_role} Python"

    keywords = keywords.strip()

    # Determine location from CV preferred location if not provided
    if not location:
        location = cv.get("preferred_location", "Remote")
    location = location.strip()

    limit = max(1, min(int(limit), 25))

    encoded_keywords = urllib.parse.quote(keywords)
    encoded_location = urllib.parse.quote(location)
    search_url = f"https://www.linkedin.com/jobs/search?keywords={encoded_keywords}&location={encoded_location}"

    print(f"\n[LinkedIn] Navigating to: {search_url}")
    print(f"[LinkedIn] Curating top {limit} jobs matching CV for '{cv.get('name', 'User')}'...")

    try:
        page = get_browser_page()
        try:
            page.goto(search_url, wait_until="commit", timeout=35000)
        except Exception:
            pass

        page.wait_for_timeout(3500)

        # Scroll down slightly to trigger lazy-loading of job cards
        try:
            page.evaluate("window.scrollBy(0, 1200);")
            page.wait_for_timeout(2000)
        except Exception:
            pass

        # Scrape job cards from public or logged-in LinkedIn search page
        card_locators = page.locator("ul.jobs-search__results-list > li")
        total_found = card_locators.count()

        if total_found == 0:
            card_locators = page.locator("li.jobs-search-results__list-item")
            total_found = card_locators.count()

        if total_found == 0:
            card_locators = page.locator("div.base-card")
            total_found = card_locators.count()

        if total_found == 0:
            msg = f"No job listings could be extracted for '{keywords}' in '{location}'. The LinkedIn page has been opened for you."
            speak(f"{nickname}, I opened LinkedIn for {keywords}, but couldn't parse the listings automatically.")
            return msg

        # Evaluate candidate jobs with deduplication
        raw_jobs = []
        seen_urls = set()
        seen_titles = set()

        for i in range(total_found):
            card = card_locators.nth(i)
            h3 = card.locator("h3, .base-search-card__title").first
            h4 = card.locator("h4, .base-search-card__subtitle").first
            loc = card.locator(".job-search-card__location, span.job-card-container__metadata-item").first
            link = card.locator("a.base-card__full-link, a").first

            title = h3.text_content().strip() if h3.count() > 0 else "Position Available"
            company = h4.text_content().strip() if h4.count() > 0 else "Company Not Listed"
            job_loc = loc.text_content().strip() if loc.count() > 0 else location
            href = link.get_attribute("href") if link.count() > 0 else search_url

            # Clean URL tracking query parameters
            if "?" in href and "linkedin.com/jobs/view" in href:
                href = href.split("?")[0]

            # Skip duplicates
            dedup_key = (title.lower().strip(), company.lower().strip())
            if href in seen_urls or dedup_key in seen_titles:
                continue
            if href != search_url:
                seen_urls.add(href)
            seen_titles.add(dedup_key)

            card_text = card.text_content() or ""

            # Check if Easy Apply is indicated on the card
            easy_apply = False
            try:
                ea_loc = card.locator("span:has-text('Easy Apply'), .job-card-container__apply-method, .job-search-card__easy-apply")
                if ea_loc.count() > 0:
                    easy_apply = True
            except Exception:
                pass

            # Score job against CV
            score, matched_skills = score_job_against_cv(title, company, card_text, cv)

            raw_jobs.append({
                "title": title,
                "company": company,
                "location": job_loc,
                "url": href,
                "match_score": score,
                "matched_skills": ", ".join(matched_skills) if matched_skills else "General Match",
                "easy_apply": "Yes" if easy_apply else "No",
                "status": "Curated (Pending Review)"
            })

            if len(raw_jobs) >= 25:
                break

        # Rank and curate the top 10 most relevant jobs
        raw_jobs.sort(key=lambda x: x["match_score"], reverse=True)
        curated_jobs = raw_jobs[:limit]

        for idx, j in enumerate(curated_jobs, 1):
            j["rank"] = idx

        # Ensure reports directory exists
        os.makedirs("reports", exist_ok=True)
        safe_kw = re.sub(r'[^a-zA-Z0-9_-]', '_', keywords).lower()
        now_str = datetime.now().strftime("%Y-%m-%d %I:%M %p")

        # =======================================================
        # Step 2: Save to a neat CSV / Excel file
        # =======================================================
        csv_filename = f"linkedin_jobs_{safe_kw}.csv"
        csv_path = os.path.join("reports", csv_filename)
        latest_csv_path = os.path.join("reports", "curated_jobs_matching_cv.csv")

        fieldnames = [
            "Rank",
            "Job Title",
            "Company",
            "Location",
            "Match Score (%)",
            "Matched Skills",
            "Easy Apply",
            "Job URL",
            "Status",
            "Extracted Date"
        ]

        for target_path in [csv_path, latest_csv_path]:
            with open(target_path, mode="w", newline="", encoding="utf-8-sig") as cf:
                writer = csv.DictWriter(cf, fieldnames=fieldnames)
                writer.writeheader()
                for j in curated_jobs:
                    writer.writerow({
                        "Rank": j["rank"],
                        "Job Title": j["title"],
                        "Company": j["company"],
                        "Location": j["location"],
                        "Match Score (%)": f"{j['match_score']}%",
                        "Matched Skills": j["matched_skills"],
                        "Easy Apply": j["easy_apply"],
                        "Job URL": j["url"],
                        "Status": j["status"],
                        "Extracted Date": now_str
                    })

        # Save JSON cache for interactive apply / review tools (Step 3)
        cache_path = os.path.join("reports", "latest_curated_jobs.json")
        with open(cache_path, "w", encoding="utf-8") as jf:
            json.dump({
                "keywords": keywords,
                "location": location,
                "extracted_at": now_str,
                "cv_used": cv.get("name", "User"),
                "jobs": curated_jobs
            }, jf, indent=4)

        # Save to Markdown report
        md_filename = f"linkedin_jobs_{safe_kw}.md"
        md_path = os.path.join("reports", md_filename)
        with open(md_path, "w", encoding="utf-8") as rf:
            rf.write(f"# LinkedIn Job Search & CV Curation Report: {keywords}\n\n")
            rf.write(f"- **Generated At**: {now_str}\n")
            rf.write(f"- **Candidate Name**: {cv.get('name', 'User')}\n")
            rf.write(f"- **Candidate Role**: {cv.get('profession', 'AI Engineer')}\n")
            rf.write(f"- **Target Location**: {location}\n")
            rf.write(f"- **Total Found on Page**: {total_found}\n")
            rf.write(f"- **Top Curated Matches**: {len(curated_jobs)}\n")
            rf.write(f"- **Excel / CSV Export**: [{csv_filename}]({csv_filename})\n\n")
            rf.write("## Top 10 Curated Job Openings Matching CV\n\n")

            for j in curated_jobs:
                rf.write(f"### #{j['rank']}. {j['title']} ({j['match_score']}% Match)\n")
                rf.write(f"- **Company**: {j['company']}\n")
                rf.write(f"- **Location**: {j['location']}\n")
                rf.write(f"- **Matched Skills**: {j['matched_skills']}\n")
                rf.write(f"- **Easy Apply**: {j['easy_apply']}\n")
                rf.write(f"- **Apply / View**: [{j['url']}]({j['url']})\n\n")

        # Spoken summary via Piper TTS
        top_match = curated_jobs[0]
        spoken_summary = (
            f"{nickname}, I curated the top {len(curated_jobs)} jobs matching your CV for {keywords}. "
            f"Top match is {top_match['title']} at {top_match['company']} with {top_match['match_score']}% relevance. "
            f"I have saved all top {len(curated_jobs)} jobs to a neat CSV file and markdown report."
        )
        speak(spoken_summary)

        # Terminal Output
        output_lines = [
            f"=== Astra Top {len(curated_jobs)} Curated Jobs Matching CV ===",
            f"Keywords: '{keywords}' | Location: '{location}'",
            f"CV Profile: {cv.get('name', 'User')} ({cv.get('profession', 'AI Engineer')})",
            "",
            f"{'#':<3} | {'Match':<5} | {'Easy Apply':<10} | {'Job Title':<35} | {'Company':<20} | {'Location'}",
            "-" * 95
        ]

        for j in curated_jobs:
            title_disp = (j['title'][:32] + "..") if len(j['title']) > 34 else j['title']
            comp_disp = (j['company'][:18] + "..") if len(j['company']) > 20 else j['company']
            output_lines.append(
                f"{j['rank']:<3} | {j['match_score']}% | {j['easy_apply']:<10} | {title_disp:<35} | {comp_disp:<20} | {j['location']}"
            )

        output_lines.append("-" * 95)
        output_lines.append("")
        output_lines.append(f"-> Neat CSV File (Excel compatible): {csv_path}")
        output_lines.append(f"-> Latest Master CSV: {latest_csv_path}")
        output_lines.append(f"-> Detailed Markdown Report: {md_path}")
        output_lines.append("")
        output_lines.append("Step 3: To view or Easy Apply, say 'open job 1' or 'apply to job 1'.")

        return "\n".join(output_lines)

    except Exception as e:
        err_msg = f"Error during LinkedIn job curation: {e}"
        print(f"\n[LinkedIn Error] {err_msg}")
        return err_msg


def fill_easy_apply_steps(page, cv):
    """
    Helper to detect common fields in the LinkedIn Easy Apply modal,
    pre-fill phone, CV attachment, and advance through 'Next' steps
    until reaching the final 'Review' screen.
    """
    profile = load_profile()
    phone = profile.get("phone", "03001234567")
    actions_taken = []

    # Iterate up to 5 steps safely
    for step in range(5):
        page.wait_for_timeout(1500)

        # 1. Phone number field
        try:
            phone_inputs = page.locator("input[type='tel'], input[id*='phone'], input[name*='phoneNumber'], input[aria-label*='Phone']")
            if phone_inputs.count() > 0:
                first_phone = phone_inputs.first
                curr_val = first_phone.input_value().strip()
                if not curr_val:
                    first_phone.fill(phone)
                    actions_taken.append(f"Pre-filled phone: {phone}")
        except Exception:
            pass

        # 2. File Upload for CV/Resume
        try:
            file_inputs = page.locator("input[type='file']")
            if file_inputs.count() > 0:
                for cand_path in ["data/cv.pdf", "data/resume.pdf", "data/cv.txt"]:
                    if os.path.exists(cand_path):
                        file_inputs.first.set_input_files(os.path.abspath(cand_path))
                        actions_taken.append(f"Attached CV: {cand_path}")
                        break
        except Exception:
            pass

        # 3. Check for Review button (Reached final step)
        try:
            review_btn = page.locator("button[aria-label*='Review your application'], button:has-text('Review')")
            if review_btn.count() > 0 and review_btn.first.is_visible() and review_btn.first.is_enabled():
                review_btn.first.click()
                actions_taken.append("Advanced to final Review screen.")
                page.wait_for_timeout(1500)
                break
        except Exception:
            pass

        # 4. Check for Next button
        try:
            next_btn = page.locator("button[aria-label*='Continue to next step'], button:has-text('Next')")
            if next_btn.count() > 0 and next_btn.first.is_visible() and next_btn.first.is_enabled():
                next_btn.first.click()
                actions_taken.append(f"Advanced step {step + 1}")
                page.wait_for_timeout(1500)
            else:
                break
        except Exception:
            break

    return actions_taken


def open_linkedin_job(job_index=1, click_easy_apply=False, auto_fill_steps=True):
    """
    Step 3: Opens a specific job page from the top 10 curated list in the browser,
    or clicks "Easy Apply", pre-fills inputs, and pauses with user confirmation
    before final submission.
    """
    profile = load_profile()
    nickname = profile.get("nickname", "Boss")
    cv = load_cv_profile()
    cache_path = os.path.join("reports", "latest_curated_jobs.json")

    if not os.path.exists(cache_path):
        msg = "No curated jobs found yet. Please ask Astra to search or curate jobs first."
        speak(f"{nickname}, please run a job search first so I can curate the jobs.")
        return msg

    try:
        with open(cache_path, "r", encoding="utf-8") as jf:
            data = json.load(jf)
        jobs = data.get("jobs", [])

        idx = int(job_index) - 1
        if idx < 0 or idx >= len(jobs):
            return f"Job #{job_index} is out of range. Available jobs: 1 to {len(jobs)}."

        job = jobs[idx]
        title = job.get("title", "Position Available")
        company = job.get("company", "Company")
        job_url = job.get("url")

        print(f"\n[LinkedIn] Opening Job #{job_index}: {title} at {company}")
        page = get_browser_page()
        try:
            page.goto(job_url, wait_until="domcontentloaded", timeout=45000)
        except Exception:
            pass

        page.wait_for_timeout(3000)

        # Check for Easy Apply button
        easy_apply_btn = page.locator("button.jobs-apply-button, button:has-text('Easy Apply'), button[aria-label*='Easy Apply']")
        has_easy_apply = easy_apply_btn.count() > 0

        if click_easy_apply and has_easy_apply:
            try:
                easy_apply_btn.first.click()
                page.wait_for_timeout(2000)
            except Exception as e:
                print(f"[LinkedIn] Could not click Easy Apply automatically: {e}")

            actions = []
            if auto_fill_steps:
                actions = fill_easy_apply_steps(page, cv)

            spoken_msg = f"{nickname}, I opened Easy Apply for {title} at {company} and pre-filled your details. Please review and confirm before submitting."
            speak(spoken_msg)

            actions_str = "\n".join(f"- {a}" for a in actions) if actions else "- Opened Easy Apply modal"

            return (
                f"=== Easy Apply Processed: Job #{job_index} ===\n"
                f"Title: {title}\n"
                f"Company: {company}\n"
                f"Automated Steps:\n{actions_str}\n"
                f"Status: Reached review stage. Waiting for user confirmation before final submission.\n"
                f"Job URL: {job_url}\n"
                f"\n[Safety Confirmation Required]: Astra will not auto-submit your application without your direct confirmation."
            )
        else:
            status_ea = "Available" if has_easy_apply else "External / Standard Apply"
            spoken_msg = f"{nickname}, I opened job #{job_index}: {title} at {company} in your browser."
            speak(spoken_msg)

            return (
                f"=== Opened Job #{job_index} ===\n"
                f"Title: {title}\n"
                f"Company: {company}\n"
                f"Location: {job.get('location')}\n"
                f"Match Score: {job.get('match_score')}%\n"
                f"Easy Apply: {status_ea}\n"
                f"Job URL: {job_url}"
            )

    except Exception as e:
        err_msg = f"Error opening job #{job_index}: {e}"
        print(f"\n[LinkedIn Error] {err_msg}")
        return err_msg


def create_linkedin_post(text=None, project_name=None, auto_publish=False):
    """
    Drafts and creates a professional post on LinkedIn about a project or custom announcement.
    """
    profile = load_profile()
    nickname = profile.get("nickname", "Boss")
    cv = load_cv_profile()

    if not text:
        if not project_name:
            project_name = "Astra AI Automation Agent"
        text = (
            f"🚀 Excited to introduce my latest project: {project_name}!\n\n"
            "I developed an autonomous agentic AI system capable of multi-step task execution, "
            "browser automation with Playwright, and intelligent CV-matched job curation.\n\n"
            "Key Highlights:\n"
            "⚡ Autonomous Multi-step Tool Planning & Execution\n"
            "🗣️ Real-time Neural Voice Assistant with Piper TTS\n"
            "💼 Intelligent Job Curation & Excel Export based on CV Stack\n"
            "🛠️ Tech Stack: Python, Playwright, LLM Orchestration, Vector RAG\n\n"
            "Always open to feedback and connecting with fellow AI builders!\n\n"
            "#ArtificialIntelligence #Python #MachineLearning #AIAgents #Automation #Playwright #Developer"
        )

    print(f"\n[LinkedIn] Navigating to LinkedIn feed: https://www.linkedin.com/feed/")
    try:
        page = get_browser_page()
        page.goto("https://www.linkedin.com/feed/", wait_until="domcontentloaded", timeout=45000)
        page.wait_for_timeout(3500)

        # Check login
        if "login" in page.url or page.locator("input#username, input#session_key").count() > 0:
            msg = f"{nickname}, please log into your LinkedIn account in the opened browser window first."
            speak(msg)
            return msg

        # Click Start a post button
        start_post_btn = page.locator(
            "button.share-box-feed-entry__trigger, "
            "button:has-text('Start a post'), "
            "div.share-box-feed-entry__trigger, "
            "button[aria-label*='Start a post']"
        )

        if start_post_btn.count() == 0:
            msg = "Could not locate 'Start a post' button. Please ensure you are logged in."
            speak(f"{nickname}, I couldn't find the post button on LinkedIn.")
            return msg

        start_post_btn.first.click()
        page.wait_for_timeout(2000)

        # Fill text editor
        editor = page.locator("div.ql-editor[contenteditable='true'], div[role='textbox'][aria-label*='post'], div.editor-content")
        if editor.count() == 0:
            editor = page.locator("div[contenteditable='true']")

        if editor.count() > 0:
            editor.first.click()
            editor.first.fill(text)
            page.wait_for_timeout(1000)

        if auto_publish:
            post_btn = page.locator("button.share-actions__primary-action, button:has-text('Post')")
            if post_btn.count() > 0 and post_btn.first.is_enabled():
                post_btn.first.click()
                page.wait_for_timeout(2500)
                speak(f"{nickname}, your post has been published to LinkedIn!")
                return f"LinkedIn post published successfully!\n\nContent:\n{text}"
            else:
                speak(f"{nickname}, I drafted the post in your browser. Please click Post.")
                return f"Post drafted in browser. Ready to publish.\n\nContent:\n{text}"
        else:
            speak(f"{nickname}, I drafted your project post on LinkedIn. Please review it in your browser and click Post.")
            return (
                f"=== LinkedIn Post Drafted in Browser ===\n\n"
                f"{text}\n\n"
                f"[Review Required]: Please review the drafted post in your browser window and click 'Post' to publish."
            )

    except Exception as e:
        err_msg = f"Error creating LinkedIn post: {e}"
        print(f"\n[LinkedIn Error] {err_msg}")
        return err_msg


def update_linkedin_profile(headline=None, about=None, auto_save=True):
    """
    Updates your LinkedIn profile headline or about description.
    """
    profile = load_profile()
    nickname = profile.get("nickname", "Boss")
    cv = load_cv_profile()

    if not headline and not about:
        headline = f"{cv.get('profession', 'AI Engineer')} | Python & Agentic AI Specialist"

    print(f"\n[LinkedIn] Navigating to profile: https://www.linkedin.com/in/me/")
    try:
        page = get_browser_page()
        page.goto("https://www.linkedin.com/in/me/", wait_until="domcontentloaded", timeout=45000)
        page.wait_for_timeout(3500)

        # Check login
        if "login" in page.url or page.locator("input#username, input#session_key").count() > 0:
            msg = f"{nickname}, please log into LinkedIn in the browser first."
            speak(msg)
            return msg

        updates_made = []

        # 1. Update Headline
        if headline:
            edit_intro_btn = page.locator(
                "button[aria-label*='Edit intro'], "
                "button.artdeco-button--tertiary:has([data-test-icon='pencil-medium']), "
                "button:has-text('Edit intro')"
            )

            if edit_intro_btn.count() > 0:
                edit_intro_btn.first.click()
                page.wait_for_timeout(2500)

                headline_input = page.locator("input[id*='headline'], textarea[id*='headline'], input[name='headline'], textarea[name='headline']")
                if headline_input.count() > 0:
                    headline_input.first.fill("")
                    headline_input.first.fill(headline)
                    updates_made.append(f"Headline updated to: '{headline}'")

                    if auto_save:
                        save_btn = page.locator("button:has-text('Save'), button[data-view-name='profile-form-save']")
                        if save_btn.count() > 0:
                            save_btn.first.click()
                            page.wait_for_timeout(2500)
                            updates_made.append("Headline saved successfully.")
            else:
                updates_made.append("Could not locate 'Edit intro' pencil icon on profile.")

        # 2. Update About Section
        if about:
            edit_about_btn = page.locator("button[aria-label*='Edit about'], div#about ~ * button[aria-label*='Edit']")
            if edit_about_btn.count() > 0:
                edit_about_btn.first.click()
                page.wait_for_timeout(2000)

                about_input = page.locator("textarea[id*='summary'], textarea[name='summary'], textarea[aria-label*='About']")
                if about_input.count() > 0:
                    about_input.first.fill("")
                    about_input.first.fill(about)
                    updates_made.append("About section updated.")

                    if auto_save:
                        save_btn = page.locator("button:has-text('Save')")
                        if save_btn.count() > 0:
                            save_btn.first.click()
                            page.wait_for_timeout(2000)
                            updates_made.append("About saved successfully.")
            else:
                updates_made.append("Could not locate 'Edit about' pencil icon on profile.")

        summary_text = "\n".join(updates_made) if updates_made else "No profile updates could be applied."
        speak(f"{nickname}, I processed your LinkedIn profile update.")
        return f"=== LinkedIn Profile Update Result ===\n{summary_text}"

    except Exception as e:
        err_msg = f"Error updating LinkedIn profile: {e}"
        print(f"\n[LinkedIn Error] {err_msg}")
        return err_msg
