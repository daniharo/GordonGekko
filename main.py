import json
import yfinance as yf
import requests
from auth import auth

pm_url = "https://sync.appfluence.com"
projects_route = "/api/v1/project/"
items_route = "/api/v1/item/"
headers = {'Authorization': 'Bearer ' + auth["token"]}
owner = auth["email"]


def get_projects_user():
    response = requests.get(pm_url + projects_route, headers=headers)
    return response.json()["objects"]


def to_string(projects_list):
    res = ""
    for idx, project in enumerate(projects_list):
        project_name = project["name"]
        res += f"{idx+1}. {project_name}\n"
    return res


def check_ticker_going_down(ticker_symbol):
    ticker = yf.Ticker(ticker_symbol)
    data = ticker.history(period="max")
    current_price = float(data["Close"][-1])
    previous_price = float(data["Close"][-2])

    print(f"Previous price: {previous_price}")
    print(f"Current price: {current_price}")

    if current_price < previous_price:
        print("\n\nCurrent price is less than previous close.")
        return True
    else:
        print("\n\nCurrent price is greater than previous close.")
        return False


def create_item_in_priority_matrix(project_id, ticker):
    item = {
        "name": f"Sell shares for {ticker}",
        "descriptionText":
            f"Price is going down so we have to sell shares for {ticker}",
        "owner": owner,
        "projects": [
            f"/api/v1/project/{project_id}/"
        ],
        "quadrant": 0
    }
    response = requests.post(
        f"{pm_url}{items_route}", json=item, headers=headers)
    response_data = response.json()
    print("Item was created. Response data:\n\n" +
          json.dumps(response_data, indent=4))
    print("\n\nYou can visit the item in the following link:\n" +
          response_data["webLink"] + "\n\n")


def main():
    print("\n\nPlease introduce the ticker you want to check:")
    ticker = input().upper()

    going_down = check_ticker_going_down(ticker)
    if not going_down:
        print(f"\n\nNo need to sell anything for {ticker}")
        return

    projects = get_projects_user()

    print("\n\nChoose the project in which you want the item to be added:")
    print(to_string(projects))

    project_index = int(input()) - 1

    # Check that project_index is valid index in projects list
    if project_index < 0 or project_index >= len(projects):
        print("Invalid index")
        return

    project_idd = projects[project_index]["idd"]
    print(f"Chosen project id: {project_idd}")

    # Create item in the chosen project
    create_item_in_priority_matrix(project_idd, ticker)


if __name__ == "__main__":
    main()
