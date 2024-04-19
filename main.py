from time import time
from selenium import webdriver
from selenium.webdriver.common.by import By


def get_items():
    store = driver.find_elements(By.CSS_SELECTOR, "#store b")

    ids = ["".join(["buy", store[i].text.split("-")[0].strip()]) for i in range(len(store) - 1)]
    prices = [int(store[i].text.split("-")[1].strip().replace(",", "")) for i in range(len(store) - 1)]
    items = {prices[i]: ids[i] for i in range(len(ids))}

    return items


chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://orteil.dashnet.org/experiments/cookie/")

timeout = time() + 5
end_game = time() + 60 * 5

while time() < end_game:
    driver.find_element(By.ID, ("cookie")).click()

    if time() > timeout:
        items = get_items()
        money = int(driver.find_element(By.ID, ("money")).text.replace(",", ""))

        can_purchase = [item for item in list(items.keys()) if money >= item]

        try:
            price = max(can_purchase)
        except ValueError:
            pass
        else:
            id = items[price]
            if id:
                driver.find_element(By.ID, id).click()

        timeout += 5

cps = driver.find_element(By.ID, "cps").text.split(":")[1].strip()
print(f"Total cookies per second in 5 minutes: {cps}")

driver.quit()
