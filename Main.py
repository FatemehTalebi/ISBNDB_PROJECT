import requests
from bs4 import BeautifulSoup
import xlsxwriter

base_url = "https://isbndb.com/search/books/"
search_item = input("Enter book name: ")
url = base_url + search_item
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Accept-Language": "en-US, en, q=.5",
}
r = requests.get(url, headers=headers)

soup = BeautifulSoup(r.text, "html.parser")
titles = soup.find_all("div", attrs={"class": "book-cover col-md-2 col-xs-4"})

# Create a new Excel file
workbook = xlsxwriter.Workbook("book_data.xlsx")
worksheet = workbook.add_worksheet()

# Write headers
headerss = ["Book Number", "Book Title", "ISBN13", "Price"]
worksheet.write_row(0, 0, headerss)

# Write data
row = 1
counter = 1
for title in titles:
    next_page = base_url + title.a["href"]
    r2 = requests.get(next_page, headers=headers)
    soup2 = BeautifulSoup(r2.text, "html.parser")
    book_info = soup2.find_all("tr")
    worksheet.write(row, 0, counter)
    counter += 1
    col = 1
    for row_data in book_info:
        th_tag = row_data.find("th")
        td_tag = row_data.find("td")
        if th_tag and td_tag:
            # worksheet.write(row, col, th_tag.text.strip())

            worksheet.write(row, col, td_tag.text.strip())

            col += 1
    row += 1

# Close the workbook
workbook.close()

print("Data saved to 'book_data.xlsx'.")
print("Written by Fatemeh Talebi")
