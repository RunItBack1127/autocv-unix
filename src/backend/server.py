from re import L
from flask import Flask, request, jsonify
from flask_cors import CORS

from github import Github

import os
import uuid
import zipfile
import tempfile

TAB_TO_SPACES = "      "

# Define paths for all application roles
MICROSERVICES_DIR = "templates/resume/microservices"
DATABASES_DIR = "templates/resume/databases"
DEFAULT_COVER_LETTER_DIR = "templates/cover_letter/default"
SD_COVER_LETTER_DIR = "templates/cover_letter/sd"

SOFTWARE_ENGINEER_PATH__MICROSERVICES_RESUME = f"{MICROSERVICES_DIR}/WPG_Software_Engineer.odt"
FRONT_END_ENGINEER_PATH__MICROSERVICES_RESUME = f"{MICROSERVICES_DIR}/WPG_Front_End_Engineer.odt"
FULL_STACK_ENGINEER_PATH__MICROSERVICES_RESUME = f"{MICROSERVICES_DIR}/WPG_Full_Stack_Engineer.odt"

SOFTWARE_ENGINEER_PATH__DATABASES_RESUME = f"{DATABASES_DIR}/WPG_Software_Engineer.odt"
FRONT_END_ENGINEER_PATH__DATABASES_RESUME = f"{DATABASES_DIR}/WPG_Front_End_Engineer.odt"
FULL_STACK_ENGINEER_PATH__DATABASES_RESUME = f"{DATABASES_DIR}/WPG_Full_Stack_Engineer.odt"

SOFTWARE_ENGINEER_PATH__MICROSERVICES_GENERATED_RESUME = f"{MICROSERVICES_DIR}/generated/WPG_Software_Engineer.odt"
FRONT_END_ENGINEER_PATH__MICROSERVICES_GENERATED_RESUME = f"{MICROSERVICES_DIR}/generated/WPG_Front_End_Engineer.odt"
FULL_STACK_ENGINEER_PATH__MICROSERVICES_GENERATED_RESUME = f"{MICROSERVICES_DIR}/generated/WPG_Full_Stack_Engineer.odt"

SOFTWARE_ENGINEER_PATH__DATABASES_GENERATED_RESUME = f"{DATABASES_DIR}/generated/WPG_Software_Engineer.odt"
FRONT_END_ENGINEER_PATH__DATABASES_GENERATED_RESUME = f"{DATABASES_DIR}/generated/WPG_Front_End_Engineer.odt"
FULL_STACK_ENGINEER_PATH__DATABASES_GENERATED_RESUME = f"{DATABASES_DIR}/generated/WPG_Full_Stack_Engineer.odt"

SOFTWARE_ENGINEER_PATH__DEFAULT_COVER_LETTER = f"{DEFAULT_COVER_LETTER_DIR}/WPG_Software_Engineer.odt"
FRONT_END_ENGINEER_PATH__DEFAULT_COVER_LETTER = f"{DEFAULT_COVER_LETTER_DIR}/WPG_Front_End_Engineer.odt"
FULL_STACK_ENGINEER_PATH__DEFAULT_COVER_LETTER = f"{DEFAULT_COVER_LETTER_DIR}/WPG_Full_Stack_Engineer.odt"

SOFTWARE_ENGINEER_PATH__DEFAULT_GENERATED_COVER_LETTER = f"{DEFAULT_COVER_LETTER_DIR}/generated/WPG_Software_Engineer.odt"
FRONT_END_ENGINEER_PATH__DEFAULT_GENERATED_COVER_LETTER = f"{DEFAULT_COVER_LETTER_DIR}/generated/WPG_Front_End_Engineer.odt"
FULL_STACK_ENGINEER_PATH__DEFAULT_GENERATED_COVER_LETTER = f"{DEFAULT_COVER_LETTER_DIR}/generated/WPG_Full_Stack_Engineer.odt"

SOFTWARE_ENGINEER_PATH__SD_COVER_LETTER = f"{SD_COVER_LETTER_DIR}/WPG_Software_Engineer.odt"
FRONT_END_ENGINEER_PATH__SD_COVER_LETTER = f"{SD_COVER_LETTER_DIR}/WPG_Front_End_Engineer.odt"
FULL_STACK_ENGINEER_PATH__SD_COVER_LETTER = f"{SD_COVER_LETTER_DIR}/WPG_Full_Stack_Engineer.odt"

SOFTWARE_ENGINEER_PATH__SD_GENERATED_COVER_LETTER = f"{SD_COVER_LETTER_DIR}/generated/WPG_Software_Engineer.odt"
FRONT_END_ENGINEER_PATH__SD_GENERATED_COVER_LETTER = f"{SD_COVER_LETTER_DIR}/generated/WPG_Front_End_Engineer.odt"
FULL_STACK_ENGINEER_PATH__SD_GENERATED_COVER_LETTER = f"{SD_COVER_LETTER_DIR}/generated/WPG_Full_Stack_Engineer.odt"

def get_abs_path(filename):
    return os.path.abspath(filename)

# Initialize Flask server
app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})

github = Github(os.environ.get("GITHUB_TOKEN"))
repo = github.get_user().get_repo("autocv-blob-storage")

# Initialize generation directories
def create_dir(dirname):
    if os.path.exists(dirname):
        return
    os.mkdir(dirname)

# GitHub PDF filename generation
def get_pdf_filename():
    return f"{str(uuid.uuid4()).replace('-', '')}.pdf"

# ODT to PDF filename conversion
def convert_extension_to_pdf( filename ):
    return f"{filename[:-4]}.pdf"

create_dir(f"{MICROSERVICES_DIR}/generated")
create_dir(f"{DATABASES_DIR}/generated")
create_dir(f"{DEFAULT_COVER_LETTER_DIR}/generated")
create_dir(f"{SD_COVER_LETTER_DIR}/generated")

"""
    GET endpoint for populating the resume template,
    with options for modifying the languages and
    toggling the bottom skill between microservices
    and databases

    RETURNS the link to the generated resume PDF
    as retrieved from the GitHub REST API
"""
@app.route('/resume', methods=['GET'])
def generate_resume():
    input_filename = ""
    output_filename = ""
    outdir = ""

    applicant_role = request.args["applicantRole"]
    competency = request.args["competency"]
    graduation_month = request.args["graduationMonth"][:3]
    graduation_year = request.args["graduationYear"]

    if competency == "Microservices":
        outdir = f"{MICROSERVICES_DIR}/generated"
    elif competency == "Databases":
        outdir = f"{DATABASES_DIR}/generated"

    if applicant_role == "Software Engineer":
        if competency == "Microservices":
            input_filename = SOFTWARE_ENGINEER_PATH__MICROSERVICES_RESUME
            output_filename = SOFTWARE_ENGINEER_PATH__MICROSERVICES_GENERATED_RESUME
        elif competency == "Databases":
            input_filename = SOFTWARE_ENGINEER_PATH__DATABASES_RESUME
            output_filename = SOFTWARE_ENGINEER_PATH__DATABASES_GENERATED_RESUME
    elif applicant_role == "Front End Engineer":
        if competency == "Microservices":
            input_filename = FRONT_END_ENGINEER_PATH__MICROSERVICES_RESUME
            output_filename = FRONT_END_ENGINEER_PATH__MICROSERVICES_GENERATED_RESUME
        elif competency == "Databases":
            input_filename = FRONT_END_ENGINEER_PATH__DATABASES_RESUME
            output_filename = FRONT_END_ENGINEER_PATH__DATABASES_GENERATED_RESUME
    elif applicant_role == "Full Stack Engineer":
        if competency == "Microservices":
            input_filename = FULL_STACK_ENGINEER_PATH__MICROSERVICES_RESUME
            output_filename = FULL_STACK_ENGINEER_PATH__MICROSERVICES_GENERATED_RESUME
        elif competency == "Databases":
            input_filename = FULL_STACK_ENGINEER_PATH__DATABASES_RESUME
            output_filename = FULL_STACK_ENGINEER_PATH__DATABASES_GENERATED_RESUME
    
    def to_bytes( str ):
        return bytes( str, 'utf-8' )

    with zipfile.ZipFile(input_filename, "r") as input_doc, zipfile.ZipFile(output_filename, "w") as output_doc:
        for input_doc_info in input_doc.infolist():
            with input_doc.open(input_doc_info) as input_doc_file:
                content = input_doc_file.read()
                if input_doc_info.filename == "content.xml":

                    relevantSkills = request.args["relevantSkills"].split(",")
                    for (skill_index, skill) in enumerate(relevantSkills):
                        content = content.replace(to_bytes(f"{{{{L{skill_index + 1}}}}}"), to_bytes(skill))

                    content = content.replace(to_bytes(f"{{{{GRAD_MONTH}}}}"), to_bytes(graduation_month))
                    content = content.replace(to_bytes(f"{{{{GRAD_YEAR}}}}"), to_bytes(graduation_year))
                output_doc.writestr(input_doc_info.filename, content)
    
    pdf_filename = convert_extension_to_pdf( output_filename )
    tmp_dir = tempfile.gettempdir()
    os.system(f"soffice --headless \"-env:UserInstallation=file:///{tmp_dir}/AUTOCV\" --convert-to pdf:writer_pdf_Export --outdir {outdir} {output_filename}")

    github_pdf_path = get_pdf_filename()
    pdf_contents = open(pdf_filename, "rb").read()
    github_response = repo.create_file(github_pdf_path, "Appending generated resume file", pdf_contents, branch="master")

    os.remove(output_filename)
    os.remove(pdf_filename)

    return jsonify(url=github_response['content'].download_url)

"""
    GET endpoint for populating the cover letter
    template with options for modifying the name of
    the hiring manager, the name of the role, and
    the company name

    RETURNS the link to the generated cover letter
    PDF  as retrieved from the GitHub REST API
"""
@app.route('/cv', methods=['GET'])
def generate_cover_letter():
    input_filename = ""
    output_filename = ""
    outdir = ""
    
    applicant_role = request.args["applicantRole"]
    cover_letter_content = request.args["coverLetterContent"]

    if cover_letter_content == "Self Driving":
        outdir = f"{SD_COVER_LETTER_DIR}/generated"
    elif cover_letter_content == "Default":
        outdir = f"{DEFAULT_COVER_LETTER_DIR}/generated"

    if applicant_role == "Software Engineer":
        if cover_letter_content == "Self Driving":
            input_filename = SOFTWARE_ENGINEER_PATH__SD_COVER_LETTER
            output_filename = SOFTWARE_ENGINEER_PATH__SD_GENERATED_COVER_LETTER
        elif cover_letter_content == "Default":
            input_filename = SOFTWARE_ENGINEER_PATH__DEFAULT_COVER_LETTER
            output_filename = SOFTWARE_ENGINEER_PATH__DEFAULT_GENERATED_COVER_LETTER
    elif applicant_role == "Front End Engineer":
        if cover_letter_content == "Self Driving":
            input_filename = FRONT_END_ENGINEER_PATH__SD_COVER_LETTER
            output_filename = FRONT_END_ENGINEER_PATH__SD_GENERATED_COVER_LETTER
        elif cover_letter_content == "Default":
            input_filename = FRONT_END_ENGINEER_PATH__DEFAULT_COVER_LETTER
            output_filename = FRONT_END_ENGINEER_PATH__DEFAULT_GENERATED_COVER_LETTER
    elif applicant_role == "Full Stack Engineer":
        if cover_letter_content == "Self Driving":
            input_filename = FULL_STACK_ENGINEER_PATH__SD_COVER_LETTER
            output_filename = FULL_STACK_ENGINEER_PATH__SD_GENERATED_COVER_LETTER
        elif cover_letter_content == "Default":
            input_filename = FULL_STACK_ENGINEER_PATH__DEFAULT_COVER_LETTER
            output_filename = FULL_STACK_ENGINEER_PATH__DEFAULT_GENERATED_COVER_LETTER
    
    with zipfile.ZipFile(input_filename, "r") as input_doc, zipfile.ZipFile(output_filename, "w") as output_doc:
        for input_doc_info in input_doc.infolist():
            with input_doc.open(input_doc_info) as input_doc_file:
                content = input_doc_file.read()
                if input_doc_info.filename == "content.xml":

                    name_of_role = request.args['nameOfRole']
                    company_name = request.args['companyName']
                    recruiter_name = request.args['recruiterName']

                    content = content.replace(bytes("{{HIRING_MANAGER}}", "utf-8"), bytes(recruiter_name, "utf-8"))
                    content = content.replace(bytes("{{NAME_OF_ROLE}}", "utf-8"), bytes(name_of_role, "utf-8"))
                    content = content.replace(bytes("{{COMPANY_NAME}}", "utf-8"), bytes(company_name, "utf-8"))
                output_doc.writestr(input_doc_info.filename, content)
    
    pdf_filename = convert_extension_to_pdf( output_filename )
    tmp_dir = tempfile.gettempdir()
    os.system(f"soffice --headless \"-env:UserInstallation=file:///{tmp_dir}/AUTOCV\" --convert-to pdf:writer_pdf_Export --outdir {outdir} {output_filename}")

    github_pdf_path = get_pdf_filename()
    pdf_contents = open(pdf_filename, "rb").read()
    github_response = repo.create_file(github_pdf_path, "Appending generated cover letter file", pdf_contents, branch="master")

    os.remove(pdf_filename)
    os.remove(output_filename)

    return jsonify(url=github_response['content'].download_url)

"""
    GET endpoint for retrieving a formatted template cover letter
    in raw text for the end user - this text is then persisted to
    the system clipboard for applications that do not have a file
    field for the cover letter
"""
@app.route('/copy', methods=['GET'])
def copy_cover_letter():
    recruiter_name = request.args["recruiterName"]
    company_name = request.args["companyName"]
    name_of_role = request.args["nameOfRole"]
    cover_letter_content = request.args["coverLetterContent"]

    default_or_av_paragraph = ""
    if cover_letter_content == "Self Driving":
        default_or_av_paragraph = "Having followed the changing self-driving landscape closely since 2015, joining the research team at the EcoPRT autonomous vehicle lab at NC State was my first step in making my mark on the industry. Assuming the role of the lead web developer further enforced my technical skillset, with the goal of redesigning the web presence for showcasing the work of deploying an autonomous vehicle. Maintaining and organizing all of the assets and leveraging each new feature, along with overseeing the design and technical implementation of the website, demonstrates my ability to contribute and dedicate to a project within the scope of a professional environment."
    elif cover_letter_content == "Default":
        default_or_av_paragraph = "Contributing in a team on a large project across many different microservices also improved my overall technical skillset, placing me in many different roles for various parts of the development cycle - working in the DevEx team at SailPoint required me to sometimes assume frontend responsibilities, other times required a richer set of backend skills, and a few times would require me to exercise more of my full stack expertise. Ensuring effective communication across teams and within our own team was critical, and deploying a consistent and functional product for the end user was kept as our paramount goal, in spite of a specific set of technologies necessary."

    contents = f"Dear {recruiter_name},\n\n{TAB_TO_SPACES}I wanted to reach out to you to further express my interest in the {name_of_role} position. As a recent graduate of the Computer Science program at North Carolina State University, a Software Engineer Intern for SailPoint Technologies, and as the current lead web developer for the EcoPRT autonomous vehicle lab at NC State, I believe that my technically sound and detailed set of front end skills and coding architecture expertise, along with my ability to collaborate, communicate, and implement punctually within a team, would make me an ideal candidate for this role.\n\n{TAB_TO_SPACES}I possess a strong facility in an array of frontend languages, notably Vue, Node.js and Typescript, along with a robust set of backend technologies in Java, C and C++, and Python. My capacity for developing alone for either personal projects, coursework, or independent lab work would integrate seamlessly with a larger team ??? I can be expected to fulfill expectations concisely, accurately, and under demanding and changing time constraints without sacrificing quality or project longevity.\n\n{TAB_TO_SPACES}{default_or_av_paragraph}\n\n{TAB_TO_SPACES}My passion and dedication are the qualities I strive to bring to the position and the team. I am confident that I can work diligently with my potential co-workers and further promote the development process of {company_name}. Thank you for your consideration, and I look forward to hearing from you to discuss the position further.\n\nSincerely,\nWeston P. Greene"

    return jsonify(contents=contents)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
