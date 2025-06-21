from src.reports import data_frame, spending_by_category, spending_by_weekday, spending_by_workday
from src.services import list_of_transactions, search_item, search_personal_transactions, search_telephone_numbers
from src.views import get_events_json

print(get_events_json("21.03.2020", "Y"), end="\n_________________\n")
print(search_item(list_of_transactions, "Супермаркеты"), end="\n_________________\n")
print(search_telephone_numbers(list_of_transactions), end="\n_________________\n")
print(search_personal_transactions(list_of_transactions), end="\n_________________\n")
print(spending_by_category(data_frame, "Супермаркеты", "08.05.2019"), end="\n_________________\n")
print(spending_by_weekday(data_frame, "21.03.2020"), end="\n_________________\n")
print(spending_by_workday(data_frame, "21.03.2020"))
