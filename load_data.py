import json
import os
import django
from django.conf import settings

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dev.settings')
django.setup()

from crm.models.companies import Company
from crm.models.agreements import Agreement
from crm.models.agents import Agent
from crm.models.bank_accounts import BankAccount
from crm.models.common_business_entities import Business
from contacts.models import Contact

def load_data():
    json_path = os.path.join(os.path.dirname(__file__), 'data.json')
    if not os.path.exists(json_path):
        print(f"File not found: {json_path}")
        return

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for entry in data:
        # Create Company
        # Mapping company_type
        c_type_map = {
            "Legal": Business.Types.Legal,
            "Individual": Business.Types.Individual,
            "Person": Business.Types.Person
        }

        company = Company.objects.create(
            name=entry["name"],
            formal_name=entry["name"], # Using name as formal_name as well for now
            company_type=c_type_map.get(entry["company_type"], Business.Types.Other),
            inn=entry.get("inn"),
            kpp=entry.get("kpp"),
            ogrn=entry.get("OGRN"),
            address=entry.get("address"),
            mail_address=entry.get("mail_address"),
            comment=entry.get("comment", ""),
        )
        print(f"Created company: {company.name}")

        # Create Agreements
        agreements_map = {} # local id -> db id
        for agr_data in entry.get("agreements", []):
            try:
                date_val = agr_data["date"]
                # Convert 14.02.2017 to 2017-02-14
                if "." in date_val:
                    day, month, year = date_val.split(".")
                    date_val = f"{year}-{month}-{day}"
            except:
                date_val = None

            agr = Agreement.objects.create(
                number=agr_data["number"],
                date=date_val,
                company=company
            )
            agreements_map[agr_data["id"]] = agr

        # Set main agreement
        if entry.get("main_agreement") and entry["main_agreement"] in agreements_map:
            company.main_agreement = agreements_map[entry["main_agreement"]]

        # Create Agents
        agents_map = {}
        for ag_data in entry.get("agents", []):
            agent = Agent.objects.create(
                name=ag_data["name"],
                position=ag_data["position"],
                authority_doc=ag_data["authority_doc"],
                details=ag_data["details"],
                company=company
            )
            agents_map[ag_data["id"]] = agent

        # Set representative
        if entry.get("representative") and entry["representative"] in agents_map:
            company.representative = agents_map[entry["representative"]]

        # Create Bank Accounts
        accounts_map = {}
        for acc_data in entry.get("bank_accounts", []):
            acc = BankAccount.objects.create(
                number=acc_data["number"],
                bank=acc_data["bank"],
                bik=acc_data["bik"],
                cor_number=acc_data["cor_number"],
                company=company
            )
            accounts_map[acc_data["id"]] = acc

        # Set main bank account
        if entry.get("main_bank_account") and entry["main_bank_account"] in accounts_map:
            company.main_bank_account = accounts_map[entry["main_bank_account"]]

        # Save company with FKs
        company.save()

        # Create Contacts
        for c_data in entry.get("contacts", []):
            contact = Contact.objects.create(
                name=c_data["name"],
                phone=c_data["phone"], # JSONField
                email=c_data["email"], # JSONField
                comment=c_data.get("comment", "")
            )
            contact.companies.add(company)
            print(f"Created contact: {contact.name}")

if __name__ == '__main__':
    load_data()
