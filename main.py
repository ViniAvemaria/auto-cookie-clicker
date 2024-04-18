import time
from selenium import webdriver
from selenium.webdriver.common.by import By


def get_items():
    store = driver.find_elements(By.CSS_SELECTOR, "#store b")
    items = {}
    for i in range(len(store) - 1):
        temp_price = store[i].text.split("-")[1].strip()
        temp_id = "buy" + store[i].text.split("-")[0].strip()
        if "," in temp_price:
            items.update({int(temp_price.replace(",", "")): temp_id})
        else:
            items.update({int(temp_price): temp_id})

    return items


chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://orteil.dashnet.org/experiments/cookie/")

timeout = time.time() + 5
end_game = time.time() + 60*5

while time.time() < end_game:
    driver.find_element(By.ID, ("cookie")).click()

    if time.time() > timeout:
        items = get_items()
        money = int(driver.find_element(By.ID, ("money")).text)

        can_purchase = [item for item in list(items.keys()) if money >= item]
        highest = max(can_purchase)
        id = items[highest]

        if id:
            driver.find_element(By.ID, f"{id}").click()

        timeout = time.time() + 5

cps = driver.find_element(By.ID, "cps").text
cps = cps.split(":")[1].strip()
print(f"Total cookies per second in 5 minutes: {cps}")

driver.quit()
