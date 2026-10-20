"""Seed the portfolio content.

    python -m app.db.seed

Re-running REPLACES all portfolio content (everything except contact_messages)
with the data below, so this file is the single source of truth for the site.
Fields marked TODO are intentionally empty: fill them in with real details.
"""

import asyncio
from datetime import date

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import dispose_engine, get_session_factory
from app.models import (
    Certification,
    Education,
    Experience,
    Profile,
    Project,
    ProjectTechnology,
    SecurityProfile,
    SecurityTool,
    Skill,
)
from app.models.enums import ProjectCategory, SkillCategory

PROFILE = {
    "name": "Satyam Prajapati",
    "headline": "Backend Engineer & Aspiring Cybersecurity Professional",
    "secondary_title": "B.Tech IT Student",
    "bio": (
        "Information Technology student building backend systems with FastAPI, PostgreSQL "
        "and Express.js, and working towards a career in cybersecurity through hands-on "
        "projects and self-directed learning."
    ),
    "location": "Indore, India",
    "email": None,  # TODO: public contact email
    "github_url": None,  # TODO
    "linkedin_url": None,  # TODO
    "resume_url": None,  # TODO
}

SKILLS: dict[SkillCategory, list[str]] = {
    SkillCategory.PROGRAMMING: ["Python", "C++", "JavaScript", "SQL"],
    SkillCategory.BACKEND: ["FastAPI", "Express.js", "REST API Design", "SQLAlchemy"],
    SkillCategory.FRONTEND: ["React"],
    SkillCategory.CYBERSECURITY: ["Linux", "Nmap", "Burp Suite", "OWASP", "VirusTotal API"],
    SkillCategory.NETWORKING: ["TCP/IP", "Wireshark"],
    SkillCategory.DATABASE: ["PostgreSQL"],
    SkillCategory.TOOLS: ["Git", "GitHub"],
}

PROJECTS = [
    {
        "title": "Cyber Fraud Detection System",
        "slug": "cyber-fraud-detection-system",
        "short_description": (
            "Web platform that helps users check files, URLs, domains, IPs and "
            "email-related indicators using the VirusTotal API."
        ),
        "description": (
            "A full-stack security analysis platform. A FastAPI backend with PostgreSQL "
            "submits indicators to the VirusTotal API and presents the results in a React "
            "interface, giving users a single place to check whether a file, link, domain, "
            "IP address or email-related artifact looks suspicious."
        ),
        "category": ProjectCategory.CYBERSECURITY,
        "technologies": ["FastAPI", "React", "PostgreSQL", "VirusTotal API"],
        "features": [
            "File scanning",
            "URL scanning",
            "Domain scanning",
            "IP scanning",
            "Email-related security analysis",
        ],
        "github_url": None,  # TODO
        "live_url": None,
        "image_url": None,
        "featured": True,
    },
    {
        "title": "Task Management App",
        "slug": "task-management-app",
        "short_description": "Capstone backend project: a task management REST API.",
        "description": (
            "A task management backend built with Express.js and PostgreSQL, developed as a "
            "capstone portfolio project."
        ),
        "category": ProjectCategory.BACKEND,
        "technologies": ["Express.js", "PostgreSQL"],
        "features": ["REST API", "PostgreSQL persistence"],
        "github_url": None,  # TODO
        "live_url": None,
        "image_url": None,
        "featured": False,
    },
]

EXPERIENCE: list[dict] = []  # TODO: add real experience (company, position, dates, ...)

EDUCATION = [
    {
        "degree": "B.Tech",
        "field": "Information Technology",
        "institution": "SGSITS Indore",
        "location": "Indore, India",
        "start_date": None,  # TODO
        "end_date": None,  # TODO
        "description": None,
    }
]

CERTIFICATIONS: list[dict] = []  # TODO: add real certifications; none are invented here

SECURITY_CATEGORIES = [
    ("Web Security", "Understanding and testing common web application weaknesses.",
     ["OWASP Top 10", "Authentication and session handling", "Input validation"]),
    ("Network Security", "Network fundamentals and traffic analysis.",
     ["TCP/IP", "Packet analysis", "Port and service discovery"]),
    ("Linux", "Working comfortably in a Linux command-line environment.",
     ["Shell usage", "File permissions", "Process and service basics"]),
    ("API Security", "Designing and reviewing APIs with security in mind.",
     ["Validation", "Rate limiting", "Safe error handling", "CORS"]),
    ("Reconnaissance", "Information gathering in authorised, lab-style settings.",
     ["Host and service enumeration", "Threat-intelligence lookups"]),
    ("Security Testing", "Hands-on practice in lab environments and CTF-style exercises.",
     ["Vulnerability assessment basics", "Password auditing concepts"]),
]

# (name, description, category)
SECURITY_TOOLS = [
    ("Nmap", "Network scanner used for host and service discovery.", "Reconnaissance"),
    ("Burp Suite", "Intercepting proxy for inspecting and testing web applications.", "Web Security"),
    ("Wireshark", "Packet analyser for inspecting network traffic.", "Network Security"),
    ("Hydra", "Network login auditing tool, used for authorised lab exercises.", "Security Testing"),
    ("Hashcat", "Password-recovery tool, used to understand hash strength in lab exercises.", "Security Testing"),
    ("VirusTotal", "Threat-intelligence service for files, URLs, domains and IPs.", "Reconnaissance"),
]


async def seed(session: AsyncSession) -> None:
    """Replace portfolio content. Caller owns the transaction boundary (commit)."""
    for model in (SecurityTool, SecurityProfile, Skill, Project, Experience, Education,
                  Certification, Profile):
        await session.execute(delete(model))  # project_technologies cascade via FK

    session.add(Profile(**PROFILE))

    for category, names in SKILLS.items():
        session.add_all(
            Skill(category=category.value, name=name, sort_order=i) for i, name in enumerate(names)
        )

    for data in PROJECTS:
        techs = data["technologies"]
        fields = {k: v for k, v in data.items() if k != "technologies"}
        fields["category"] = fields["category"].value
        session.add(Project(
            **fields,
            technologies=[ProjectTechnology(name=n, sort_order=i) for i, n in enumerate(techs)],
        ))

    session.add_all(Experience(**e) for e in EXPERIENCE)
    session.add_all(Education(**e) for e in EDUCATION)
    session.add_all(Certification(**c) for c in CERTIFICATIONS)

    categories = {}
    for i, (name, description, areas) in enumerate(SECURITY_CATEGORIES):
        categories[name] = SecurityProfile(
            category=name, description=description, focus_areas=areas, sort_order=i
        )
    session.add_all(categories.values())
    session.add_all(
        SecurityTool(name=n, description=d, security_profile=categories[c], sort_order=i)
        for i, (n, d, c) in enumerate(SECURITY_TOOLS)
    )
    await session.commit()


async def main() -> None:
    async with get_session_factory()() as session:
        await seed(session)
    await dispose_engine()
    print("Seeded portfolio content.")


if __name__ == "__main__":
    asyncio.run(main())
