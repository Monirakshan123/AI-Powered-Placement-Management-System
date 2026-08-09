def calculate_match_score(student_skills, job_skills):

    student_skills = set(
        skill.strip().lower()
        for skill in student_skills.split(",")
    )

    job_skills = set(
        skill.strip().lower()
        for skill in job_skills.split(",")
    )


    matched_skills = student_skills.intersection(job_skills)


    if len(job_skills) == 0:
        return 0


    score = (
        len(matched_skills)
        /
        len(job_skills)
    ) * 100


    return round(score,2)