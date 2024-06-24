FORM_DATA = {
    "contact_lastname": "Contact last name",
    "contact_email": "contact@example.com",
    "alternative_contact": "No",
    "licence_holder_lastname": "",
    "licence_holder_email": "",
    "agent_companyname": "The <malicious company>",
    "agent_companyname_other": "A completely benign company",
    "agent_country": "country:GB",
    "tna_contacttype": {
        "choices": ["Private limited company"],
        "other": "Other company type",
    },
    "agent_companyid": "company id",
    "partners": "partner names",
    "project_name": "Project name",
    "project_url": "https://example.com",
    "project_purpose": {
        "choices": ["Publish legal information"],
        "other": "Other project purpose",
    },
    "user": "Public access",
    "benefit": {
        "choices": ["General public", "The Judiciary"],
        "community_other": "Other community",
        "profession_other": "Other profession",
        "other": "Other benefit",
    },
    "public_statement": "Public statement",
    "focus_on_specific": "Yes",
    "anonymise_individuals": "No",
    "algorithm_review": "Yes",
    "code_of_ethics": "No",
    "third_party_ethics_review": "Yes",
    "entire_record_available": "No",
    "data_extracted_available": "Yes",
    "methodology_available": "No",
    "publish_findings": "Yes",
    "computational_analysis_type": "Computational analysis type",
    "generative_ai_use": "No",
    "explain_limitations": "Yes",
    "accept_principles": "No",
    "principles_statement": "Principles statement",
    "additional_comments": "Additional comments",
}

EXPECTED_SANITIZED_RESULT = """
<contact_lastname>Contact last name</contact_lastname>
<contact_email>contact@example.com</contact_email>
<alternative_contact>No</alternative_contact>
<licence_holder_lastname>Contact last name</licence_holder_lastname>
<licence_holder_email>contact@example.com</licence_holder_email>
<agent_companyname>The &lt;malicious company&gt;</agent_companyname>
<agent_companyname_other>A completely benign company</agent_companyname_other>
<agent_country>United Kingdom</agent_country>
<tna_contacttype>Private limited company</tna_contacttype>
<tna_contacttype_other>Other company type</tna_contacttype_other>
<agent_companyid>company id</agent_companyid>
<partners>partner names</partners>
<project_name>Project name</project_name>
<project_url>https://example.com</project_url>
<project_purpose>Publish legal information</project_purpose>
<project_purpose_other>Other project purpose</project_purpose_other>
<user>Public access</user>
<benefit>General public, The Judiciary</benefit>
<benefit_community_other>Other community</benefit_community_other>
<benefit_profession_other>Other profession</benefit_profession_other>
<benefit_other>Other benefit</benefit_other>
<public_statement>Public statement</public_statement>
<focus_on_specific>Yes</focus_on_specific>
<anonymise_individuals>No</anonymise_individuals>
<algorithm_review>Yes</algorithm_review>
<code_of_ethics>No</code_of_ethics>
<third_party_ethics_review>Yes</third_party_ethics_review>
<entire_record_available>No</entire_record_available>
<data_extracted_available>Yes</data_extracted_available>
<methodology_available>No</methodology_available>
<publish_findings>Yes</publish_findings>
<computational_analysis_type>Computational analysis type</computational_analysis_type>
<generative_ai_use>No</generative_ai_use>
<explain_limitations>Yes</explain_limitations>
<accept_principles>No</accept_principles>
<principles_statement>Principles statement</principles_statement>
<additional_comments>Additional comments</additional_comments>
"""
