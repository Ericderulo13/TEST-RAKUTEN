#Installing all the dependencies
#from selenium
from selenium import webdriver
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdrivermanager_cn.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
options = Options()
options.add_experimental_option("detach", True)
# Web used for automation :'https://www.saucedemo.com/')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get('https://www.saucedemo.com/')
# Maximizing the window size.
driver.maximize_window()


# Theoretically user available in the webpage:
usuarios = ["standard_user", "locked_out_user", "problem_user", "performance_glitch_user", "error_user", "visual_user"]
lista_usuarios = []
lista_high_low_users = []
# All the time sleeps used in the automation are included in order to avoid some problems in finding elements on the page.
# Also to see the process that I am performing with my script.

# Test 1 + Test 2 + Test 3
# Automation for the user login and different sorting options about products
print("Login + sorting methods test + logout: \n")
for usuario in usuarios:
    if usuario == "error_user":
        print("USER:" + str(usuario) + " " + "no login due to its sorting problem")
    else:
        # time.sleep(2)
        username = driver.find_element(By.XPATH, '//*[@id="user-name"]')
        password = driver.find_element(By.XPATH, '//*[@id="password"]')
        username.clear()
        password.clear()
        username.send_keys(usuario)
        password.send_keys("secret_sauce")
        # Computing the login time
        start_time = time.time()
        driver.find_element(By.XPATH, '//*[@id="login-button"]').click()
        end_time = time.time()
        login_time = end_time - start_time
        print(str(usuario) + " " + " login time: " + " " + str(login_time))
        try:
            driver.find_element(By.XPATH, '//*[@id="react-burger-menu-btn"]').click()
        except:
            # If we do not find the menu button, we go to the main page.
            print("usuario :" + " " + str(usuario) + " " + "Login Unsuccesful")
            driver.get("https://www.saucedemo.com")
            continue
        # Looking for the sorting methods available
        try:
            # A-Z Products
            driver.find_element(By.XPATH, '//*[@id="header_container"]/div[2]/div/span/select/option[1]').click()
            # time.sleep(2)
            # Z-A Products
            driver.find_element(By.XPATH, '//*[@id="header_container"]/div[2]/div/span/select/option[2]').click()
            # time.sleep(2)
            # Low high
            driver.find_element(By.XPATH, '//*[@id="header_container"]/div[2]/div/span/select/option[3]').click()
            # time.sleep(2)
            # High low
            driver.find_element(By.XPATH, '//*[@id="header_container"]/div[2]/div/span/select/option[4]').click()
            # We add the prices of the HIGH-LOW Section
            lista = []
            for i in range(6):
                a = driver.find_element(By.XPATH, '//*[@id="inventory_container"]/div/div[' + str(i + 1) + ']/div[2]/div[2]/div')
                lista.append(a.text)

        except:
            print(usuario,"Sorting button problem")
        # time.sleep(2)
        lista_usuarios.append(usuario)
        lista_high_low_users.append(lista)
        driver.find_element(By.XPATH, '//*[@id="logout_sidebar_link"]').click()
        # time.sleep(2)

#Proving that the items of the high low section are the same for each user(Error_user,Locked_out_user are not contempled).
#We can do it for each section but is the same code for all of them.
for i in range(len(lista_usuarios) - 1):
    if lista_high_low_users[0] == lista_high_low_users[i + 1]:
        print(f"Text lists for {usuarios[0]} and {lista_usuarios[i + 1]} are equal.")
    else:
        print(f"Text lists {usuarios[0]} and {lista_usuarios[i + 1]} are different.")


# Test 4:
print("Testing buttons add to cart + fulfilling information for the checkout + checkout: \n")
driver.quit()
options = Options()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get('https://www.saucedemo.com/')
# Maximizing the window size.
driver.maximize_window()
# Prove purchasing one product by different users:
for usuario in usuarios:
    if usuario == "error_user":
        print(str(usuario) + " " + "no login due to its sorting problem")
    else:
        # time.sleep(2)
        username = driver.find_element(By.XPATH, '//*[@id="user-name"]')
        password = driver.find_element(By.XPATH, '//*[@id="password"]')
        username.clear()
        password.clear()
        username.send_keys(usuario)
        time.sleep(2)
        password.send_keys("secret_sauce")
        time.sleep(2)
        driver.find_element(By.XPATH, '//*[@id="login-button"]').click()
        links = driver.find_elements("xpath", "//a[@href]")
        try:
            driver.find_element(By.XPATH, '//*[@id="react-burger-menu-btn"]').click()
        except:
            # If we do not find the menu button, we go to the main page.
            print("usuario :" + " " + str(usuario) + " " + "LOGIN UNSUCCSSEFUL")
            driver.get("https://www.saucedemo.com")
            continue
        time.sleep(3)
        try:
            driver.find_element(By.XPATH, '//*[@id="add-to-cart-sauce-labs-backpack"]').click()
        except:
            print("The", usuario, "not manage to do the checkout ")
            driver.get('https://www.saucedemo.com/')
            continue
        # Adding to cart the first product and proceed to do the checkout.
        driver.find_element(By.XPATH, '//*[@id="shopping_cart_container"]/a').click()
        time.sleep(5)
        driver.find_element(By.XPATH, '// *[ @ id = "checkout"]').click()
        # Filling the information for CheckOut
        first_name = driver.find_element(By.XPATH, '// *[ @ id = "first-name"]')
        last_name = driver.find_element(By.XPATH, '// *[ @ id = "last-name"]')
        zipcode = driver.find_element(By.XPATH, '// *[ @ id = "postal-code"]')
        first_name.send_keys("paquito")
        time.sleep(1)
        last_name.send_keys("torres")
        time.sleep(1)
        zipcode.send_keys("00324")
        time.sleep(2)
        driver.find_element(By.XPATH, '// *[ @ id = "continue"]').click()
        try:
            driver.find_element(By.XPATH, '// *[ @ id = "finish"]').click()
        except:
            # Could not click finish -> Not Purchase.
            print(usuario, "Can not buy items")
            driver.get('https://www.saucedemo.com/')
            continue
        # Going to Initial web in order to do the next automation user.
        driver.get('https://www.saucedemo.com/')
driver.quit()

options = Options()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get('https://www.saucedemo.com/')
# Maximizing the window size.
driver.maximize_window()
print("Testing the reset app button for all users: \n")
#Test 5:
for usuario in usuarios:
    # time.sleep(2)
    username = driver.find_element(By.XPATH, '//*[@id="user-name"]')
    password = driver.find_element(By.XPATH, '//*[@id="password"]')
    username.clear()
    password.clear()
    username.send_keys(usuario)
    password.send_keys("secret_sauce")
    time.sleep(2)
    driver.find_element(By.XPATH, '//*[@id="login-button"]').click()
    try:
        driver.find_element(By.XPATH, '//*[@id="react-burger-menu-btn"]').click()
    except:
        # If we do not find the menu button, we go to the main page.
        print("The" + " " + str(usuario) + " " + "login unsuccessful")
        driver.get("https://www.saucedemo.com")
        continue
    time.sleep(2)
    driver.find_element(By.XPATH, '//*[@id="add-to-cart-sauce-labs-backpack"]').click()
    driver.find_element(By.XPATH, '//*[@id="add-to-cart-sauce-labs-onesie"]').click()
    driver.find_element(By.XPATH, '//*[@id="add-to-cart-sauce-labs-bike-light"]').click()
    time.sleep(1)
    check_out_number = driver.find_element(By.XPATH, '//*[@id="shopping_cart_container"]/a').text
    driver.find_element(By.XPATH, '// *[ @ id = "reset_sidebar_link"]').click()
    # Going to checklist to check if the number of elements inside is zero:
    try:
        driver.find_element(By.XPATH, '//*[@id="shopping_cart_container"]/a/span')
        print(usuario, " not correctly_removed")
    except:
        print(usuario, "correctly removed from the shopping cart")

    time.sleep(2)
    inventory_list = driver.find_elements("xpath", '//*[@id="root"]')
    # Counting how elements are removed or no.
    elements_not_removed = 0
    lista = []
    for link in inventory_list:
        lista.append(link.text)
    lines = str(lista).split('\\n')
    for i in range(len(lines)):
        if lines[i] == 'Remove':
            elements_not_removed+=1
    print(usuario, "num of elements not removed is", elements_not_removed)
    driver.find_element(By.XPATH, '//*[@id="logout_sidebar_link"]').click()

##Test 7: Image testing
print("Testing if the images displayed are the correct photos: \n")
for usuario in usuarios:
    # time.sleep(2)
    username = driver.find_element(By.XPATH, '//*[@id="user-name"]')
    password = driver.find_element(By.XPATH, '//*[@id="password"]')
    username.clear()
    password.clear()
    username.send_keys(usuario)
    password.send_keys("secret_sauce")
    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id="login-button"]').click()

    try:
        driver.find_element(By.XPATH, '//*[@id="react-burger-menu-btn"]').click()
        time.sleep(2)
    except:
        # If we do not find the menu button, we go to the main page.
        print("usuario :" + " " + str(usuario) + " " + "Login unsuccessful")
        driver.get("https://www.saucedemo.com")
        continue
    # Images
    images_list=[]
    for i in range(6):
        if i ==0:
            first_element = driver.find_element(By.XPATH, '//*[@id="item_' + str(i) + '_img_link"]/img').get_attribute("src")
            images_list.append(first_element)
            if first_element == "https://www.saucedemo.com/static/media/sl-404.168b1cce.jpg":
                print("Incorrect photo product from",usuario)
        else:
            element=driver.find_element(By.XPATH, '//*[@id="item_' + str(i) + '_img_link"]/img').get_attribute("src")
            if element in images_list:
                print("Duplicated photo",element)
            images_list.append(element)
            if element == "https://www.saucedemo.com/static/media/sl-404.168b1cce.jpg":
                print("Incorrect photo product from",usuario)
    images_list.clear()
    driver.find_element("xpath", '//*[@id="logout_sidebar_link"]').click()

