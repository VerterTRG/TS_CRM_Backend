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
    data = [
      {
        "id": "1",
        "company_type": "Legal",
        "name": "ООО \"Энергоучет\"",
        "main_agreement": 1,
        "agreements": [
          {
            "id": 1,
            "number": "502",
            "date": "2017-02-14"
          }
        ],
        "inn": "0273050716",
        "kpp": "027301001",
        "OGRN": "1040203729939",
        "address": "450038, г. Уфа ул. Свободы, д.16",
        "mail_address": "450038, г. Уфа ул. Свободы, д.16",
        "representative": 1,
        "agents": [
          {
            "id": 1,
            "name": "",
            "position": "",
            "authority_doc": "Устава",
            "details": ""
          }
        ],
        "main_bank_account": 1,
        "bank_accounts": [
          {
            "id": 1,
            "number": "40702810906000006444",
            "bank": "Отд. N8598 Сбербанка России г. Уфа",
            "bik": "48073601",
            "cor_number": "30101810300000000601"
          }
        ],
        "comment": "",
        "contacts": [
          {
            "id": 1,
            "name": "Игорь",
            "phone": [
              "89196180999"
            ],
            "email": [],
            "comment": "от Руслана"
          }
        ]
      },
      {
        "id": "2",
        "company_type": "Legal",
        "name": "ООО \"УРАЛТЕХСЕРВИС\"",
        "main_agreement": 1,
        "agreements": [
          {
            "id": 1,
            "number": "509",
            "date": "2017-02-20"
          }
        ],
        "inn": "0273900836",
        "kpp": "027301001",
        "OGRN": "1150280008427",
        "address": "450064, РБ, г. Уфа, ул. Интернациональная, 20",
        "mail_address": "450112, РБ, г. Уфа, а/я 55",
        "representative": 1,
        "agents": [
          {
            "id": 1,
            "name": "Хуснияров Юлай Марзавиевич",
            "position": "Директор",
            "authority_doc": "Устава",
            "details": ""
          }
        ],
        "main_bank_account": 1,
        "bank_accounts": [
          {
            "id": 1,
            "number": "40702810400130000789",
            "bank": "Фил. ПАО \"УРАЛСИБ\" в г. Уфа",
            "bik": "48073770",
            "cor_number": "30101810600000000770"
          }
        ],
        "comment": "",
        "contacts": [
          {
            "id": 1,
            "name": "",
            "phone": [],
            "email": [],
            "comment": "от Руслана"
          }
        ]
      },
      {
        "id": "3",
        "company_type": "Individual",
        "name": "ИП ЗОЛОТОВ ДЕНИС НИКОЛАЕВИЧ",
        "main_agreement": 1,
        "agreements": [
          {
            "id": 1,
            "number": "636",
            "date": "2017-08-15"
          }
        ],
        "inn": "740201758906",
        "kpp": "",
        "OGRN": "306740224200020",
        "address": "454021 г. Челябинск, Молодогвардейцев 39в, кв. 70",
        "mail_address": "454021 г. Челябинск, Молодогвардейцев 39в, кв. 70",
        "representative": None,
        "agents": [],
        "main_bank_account": 1,
        "bank_accounts": [
          {
            "id": 1,
            "number": "40802810522110003146",
            "bank": "АО КБ \"МОДУЛЬБАНК\"",
            "bik": "45003734",
            "cor_number": "30101810300000000734"
          }
        ],
        "comment": "",
        "contacts": [
          {
            "id": 1,
            "name": "Елена",
            "phone": [
              "89193005684"
            ],
            "email": [
              "zolotova_1984@bk.ru"
            ],
            "comment": ""
          }
        ]
      }
    ]

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
