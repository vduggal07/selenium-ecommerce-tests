import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(scope="class")
def setup(request):
    driver = webdriver.Chrome(service=webdriver.ChromeService(executable_path="C:\\Users\\Vishal's Beast\\Downloads\\chromedriver-win64\\chromedriver.exe"))
    request.cls.driver = driver
    driver.maximize_window()
    yield
    driver.quit()

@pytest.mark.usefixtures("setup")
class TestEcommerce:

    @pytest.mark.parametrize("user_data", [
        {"username": "testuser", "password": "testpassword", "expected_message": "Sign up successful!"},
        {"username": "existinguser", "password": "testpassword", "expected_message": "This user already exists."}
    ])
    def test_user_sign_up(self, user_data):
        self.perform_sign_up(user_data)

    @pytest.mark.parametrize("user_data", [
        {"username": "testuser", "password": "testpassword", "expected_message": "Log in successful!"},
        {"username": "invaliduser", "password": "invalidpassword", "expected_message": "User does not exist."}
    ])
    def test_user_login(self, user_data):
        self.perform_login(user_data)

    def perform_sign_up(self, user_data):
        self.driver.get("https://www.demoblaze.com/signup.html")
        self.fill_credentials(user_data["username"], user_data["password"])
        self.click_sign_up()
        self.verify_message(user_data["expected_message"])

    def perform_login(self, user_data):
        self.driver.get("https://www.demoblaze.com/login.html")
        self.fill_credentials(user_data["username"], user_data["password"])
        self.click_login()
        self.verify_message(user_data["expected_message"])

    def fill_credentials(self, username, password):
        username_field = self.driver.find_element(By.ID, "sign-username" if "sign" in self.driver.current_url else "loginusername")
        password_field = self.driver.find_element(By.ID, "sign-password" if "sign" in self.driver.current_url else "loginpassword")
        username_field.send_keys(username)
        password_field.send_keys(password)

    def click_sign_up(self):
        sign_up_button = self.driver.find_element(By.XPATH, "//button[text()='Sign up']")
        sign_up_button.click()

    def click_login(self):
        login_button = self.driver.find_element(By.XPATH, "//button[text()='Log in']")
        login_button.click()

    def verify_message(self, expected_message):
        message_locator = (By.XPATH, "//div[@id='signInModal']//h5[@class='modal-title']" if "sign" in self.driver.current_url else "//div[@id='logInModal']//h5[@class='modal-title']")
        actual_message = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(message_locator)).text
        assert actual_message == expected_message
