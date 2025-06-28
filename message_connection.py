from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pyperclip

connection_list_file = 'rafi_connections_2025-06-28_14-56.txt'

log_file_initialized = False

def print_and_log(message:str):
    global log_file_initialized

    print(message)

    mode = 'a'
    if not log_file_initialized:
        mode = 'w'  # Overwrite the first time
        log_file_initialized = True

    with open('final_log.txt', mode, encoding='utf-8') as f:
        f.write(message + '\n')

driver = webdriver.Chrome()

# LOGIN
wait_time_login = 45
driver.get('https://www.linkedin.com/login')

print_and_log(f"Please log in manually within {wait_time_login} seconds...")
for remaining in range(wait_time_login, 0, -1):
    if remaining % 15 == 0 or remaining <= 10:
        print_and_log(f"{remaining} seconds remaining...")
    time.sleep(1)

print_and_log("Time's up! Attempting to proceed...\n\n")

# BEGIN MESSAGING CONNECTION

message_to_send_ORIGINAL = """Testing message
multiline
"""

message_to_send = "Linkedin automated message 🤖🤖☺️ testing... thank you for understanding!"

def message_connection(connection_url: str):
    start_time = time.time()

    driver.execute_script(f"window.open('{connection_url}', '_blank');")
    time.sleep(2)

    # Switch to the new tab
    driver.switch_to.window(driver.window_handles[-1])
    print_and_log(f"Switched to tab: {driver.current_url}")

    time.sleep(5)

    message_button_found = False
    message_button_xpaths = [
        "/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[3]/div/div[1]/button",
        "/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[3]/div/div[1]/button",
    ]

    message_form_found = False
    message_form_xpaths = [
        "/html/body/div[5]/div[4]/div/aside[1]/div[2]/div[1]/div[2]/div/form/div[3]/div[1]/div/div[1]",
        "/html/body/div[6]/div[4]/div/aside[1]/div[2]/div[1]/div[2]/div/form/div[3]/div[1]/div/div[1]",
    ]

    message_send_button_found = False
    message_send_button_xpaths = [
        "/html/body/div[6]/div[4]/div/aside[1]/div[2]/div[1]/div[2]/div/form/footer/div[2]/div[1]/button",
        "/html/body/div[5]/div[4]/div/aside[1]/div[2]/div[1]/div[2]/div/form/footer/div[2]/div[1]/button",
    ]

    message_send_close_button_found = False
    message_send_close_button_xpaths = [
        "/html/body/div[5]/div[4]/div/aside[1]/div[2]/div[1]/header/div[4]/button[3]",
        "/html/body/div[6]/div[4]/div/aside[1]/div[2]/div[1]/header/div[4]/button[3]"
    ]

    try:
        # MESSAGE BUTTON
        for xpath in message_button_xpaths:
            try:
                print_and_log(f"🔍 Attempting to find message button with XPath: {xpath}")
                message_button = driver.find_element(By.XPATH, xpath)
                print_and_log("🕹️🕹️🕹️ Found message button, clicking...")
                message_button.click()
                message_button_found = True
                time.sleep(3)
                break
            except Exception as e:
                print_and_log(f"❌ Message button not found with {xpath}")
                continue

        if not message_button_found:
            raise (f"❌❌❌ Could not find message BUTTON with any provided XPaths for {connection_url}")
        

        # MESSAGE FORM
        for xpath in message_form_xpaths:
            try:
                print_and_log(f"🔍 Attempting to find message FORM with XPath: {xpath}")
                message_form = driver.find_element(By.XPATH, xpath)
                print_and_log("✅✅✅✅ Found message FORM, sending keys...")

                pyperclip.copy(message_to_send)
                message_form.send_keys(Keys.CONTROL, 'v')
                time.sleep(3)

                #print_and_log(f"COPY x PATH SEND BUTTON! 📩📩📩")
                #time.sleep(15)

                message_form_found = True
                break
            except Exception as e:
                print_and_log(f"❌ Message FORM not SUCCESSFUL for {xpath}")
                #print_and_log(f"Error REASON:{e}")
                time.sleep(2)
                continue

        if not message_form_found:
            raise (f"❌❌❌ Could not find message FORM with any provided XPaths for {connection_url}")
        
        # SEND MESSAGE BUTTON
        for xpath in message_send_button_xpaths:
            try:
                print_and_log(f"🔍 Attempting to find message SEND BUTTON with XPath: {xpath}")
                message_send_button = driver.find_element(By.XPATH, xpath)
                print_and_log("📩 Found SEND MESSAGE button, clicking...")
                message_send_button.click()
                message_send_button_found = True
                time.sleep(3)
                break
            except Exception as e:
                print_and_log(f"❌💀 Message SEND button not found with {xpath}")
                continue

        if not message_send_button_found:
            raise (f"❌❌❌ Could not find message SEND BUTTON with any provided XPaths for {connection_url}")
        
        # CLOSE MESSAGE BUTTON
        for xpath in message_send_close_button_xpaths:
            try:
                print_and_log(f"🔍 Attempting to find message SEND BUTTON with XPath: {xpath}")
                message_close_button = driver.find_element(By.XPATH, xpath)
                print_and_log("📩 Found CLOSE send message button, clicking...")
                message_close_button.click()
                message_send_close_button_found = True
                time.sleep(3)
                break
            except Exception as e:
                print_and_log(f"❌❌ Message CLOSE SEND button not found with {xpath}")
                continue

        if not message_send_close_button_found:
            raise (f"❌❎✖️ Could not find message SEND BUTTON with any provided XPaths for {connection_url}")

    except Exception as e:
        if not message_button_found or not message_form_found or not message_send_button_found or not message_send_close_button_found:
            print_and_log(f"\n\n😞😞😞 Failed with {connection_url}\n\n")

            # Check if the connection already exists in the file
            try:
                with open('failed_connections.txt', 'r', encoding='utf-8') as f:
                    failed_urls = set(line.strip() for line in f)
            except FileNotFoundError:
                failed_urls = set()  # File might not exist on first run

            if connection_url not in failed_urls:
                with open('failed_connections.txt', 'a', encoding='utf-8') as f:
                    f.write(f"{connection_url}\n")
                    print_and_log("🔁 Added to failed_connections.txt")
            return False

    finally:
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        print_and_log("Switched back to main tab.")
        time.sleep(3)

        #time taken for connection
        finished_time = time.time()
        time_taken = finished_time-start_time

        if message_button_found and message_form_found and message_send_button_found and message_send_close_button_found:
            print_and_log(f"\n\n🎊🎊🎊 Success with {connection_url}, time taken: {time_taken:.2f}s\n\n")

            # Remove connection_url from failed_connections.txt if present
            try:
                with open('failed_connections.txt', 'r', encoding='utf-8') as f:
                    failed_urls = [line.strip() for line in f]
            except FileNotFoundError:
                failed_urls = []

            if connection_url in failed_urls:
                failed_urls.remove(connection_url)
                with open('failed_connections.txt', 'w', encoding='utf-8') as f:
                    for url in failed_urls:
                        f.write(url + '\n')
                print_and_log(f"✅ Removed {connection_url} from failed_connections.txt")

            return True


with open(connection_list_file, 'r') as file:
    connections = [line.strip() for line in file]

for connection in connections.copy():  # Iterate over a copy to modify the list
    print_and_log(f"\n📱📱 Messaging {connection}...\n")
    message_sent = message_connection(connection)
    time.sleep(1)

    # If success, remove connection and rewrite file
    if message_sent:
        connections.remove(connection)
        with open(connection_list_file, 'w') as f:
            f.writelines(line + '\n' for line in connections)
        print_and_log(f"✅ Removed {connection} from list file.")

driver.quit() # Close the browser when done
print_and_log("Script finished.")