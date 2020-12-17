import requests
from bs4 import BeautifulSoup
import pandas as pd

if __name__ == "__main__":
    utcs_url = "https://www.cs.utexas.edu/people"
    page = requests.get(utcs_url)
    page.raise_for_status()
    soup = BeautifulSoup(page.content, "html.parser")

    professors = []
    titles = []
    fields = []
    homepages = []
    email_addrs = []
    phone_numbers = []
    addrs = []
    for div in soup.findAll("div", "ds-teaser"):
        name = div.find("div", "field-name-title")
        title = div.find("div", "field-name-field-contact-faculty-title")

        faculty_url = name.find("a").get("href")
        faculty_page = requests.get("https://www.cs.utexas.edu/" + faculty_url)
        faculty_page.raise_for_status()
        soup_faculty = BeautifulSoup(faculty_page.content, "html.parser")

        div_contact_info = soup_faculty.find("div", "ds-contactinfo")
        if (
            div_contact_info.find("div", "field-name-field-contact-faculty-homepage")
            is None
        ):
            homepages.append("N/A")
        else:
            div_homepage = (
                div_contact_info.find(
                    "div", "field-name-field-contact-faculty-homepage"
                )
                .find("a")
                .get("href")
            )
            homepages.append(div_homepage)

        if (
            div_contact_info.find("div", "field-name-faculty-page-email-address")
            is None
        ):
            email_addrs.append("N/A")
        else:
            div_email_addr = div_contact_info.find(
                "div", "field-name-faculty-page-email-address"
            ).find("a")
            email_addrs.append(div_email_addr.text)

        if (
            div_contact_info.find("div", "field-name-field-contact-faculty-phone")
            is None
        ):
            phone_numbers.append("N/A")
        else:
            div_phone_number = div_contact_info.find(
                "div", "field-name-field-contact-faculty-phone"
            ).find("div", class_="field-item even")
            phone_numbers.append(div_phone_number.text)

        if (
            div_contact_info.find("div", "field-name-field-contact-faculty-office")
            is None
        ):
            addrs.append("N/A")
        else:
            div_addr = div_contact_info.find(
                "div", "field-name-field-contact-faculty-office"
            ).find("div", class_="field-item even")
            addrs.append(div_addr.text)

        field = div.find("div", "field-name-field-research-groups")
        if field is not None:
            field = field.find("a")
        professors.append(name.text)
        titles.append(title.text)

        if field is None:
            fields.append("N/A")
        else:
            fields.append(field.text)

    table = sorted(
        list(
            zip(
                professors, titles, fields, homepages, email_addrs, phone_numbers, addrs
            )
        ),
        key=lambda x: x[2],
    )
    p = []
    t = []
    f = []
    h = []
    ea = []
    pn = []
    a = []
    for e in table:
        p.append(e[0])
        t.append(e[1])
        f.append(e[2])
        h.append(e[3])
        ea.append(e[4])
        pn.append(e[5])
        a.append(e[6])

    dataframe = pd.DataFrame(
        {
            "Professor": p,
            "Title": t,
            "Field": f,
            "Homepage": h,
            "Email": ea,
            "Phone Number": pn,
            "Address": a,
        }
    )
    dataframe.index += 1
    dataframe.to_csv("utcs_faculty.csv", encoding="utf-8")
