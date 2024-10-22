# Chegg Question Notifier

Automates the login process to the Chegg Expert platform, saves the login session as cookies, and continually checks for new questions by periodically refreshing the Q&A page, saving manual time and effort. It uses Selenium WebDriver to simulate browser actions and notify users when a new question is available.


## Features

- **Automated Login**: Logs into Chegg Expert using the credentials stored in environment variables.
- **Cookie Management**: Saves and reuses cookies to maintain the session across script runs.
- **Question Availability Checker**: Periodically refreshes the Q&A page to detect new questions.
- **Desktop Notification**: Sends a desktop notification when a new question is available.
- **Hard Refresh**: Performs a hard refresh to clear cache and prevent stale data issues.


## Setup

This project is written in `Python 3.10`.

1. **Install Required Python Packages**:

   ```bash
   pip install -r requirements.txt
   ```

2. **Download ChromeDriver**:

   Install `Chrome` if not present. Download the appropriate version of `ChromeDriver` that matches your version of Chrome and place it in a directory of your choice.

3. **Set up Environment Variables**:

   Create a `.env` file in the project directory. (refer `.env.example`):

   ```bash
   EMAIL=example@domain.com
   PASSWORD=your_password_here
   
   CHROMEDRIVER_PATH=/path/to/chromedriver/executable
   COOKIES_DIR=/path/to/cookies/directory
   ```

   Replace with actual values.


## How to Use

1. **Run the Script**:

   ```bash
   python notifier.py
   ```

   This will:
   - Log in to Chegg Expert.
   - Save the session cookies for future runs.
   - Start checking for new questions automatically.

2. **Notifications**:
   
   The script will send a desktop notification when a question is found, alerting the user.

**Recommended Usage:**

Once cookies are saved, only use `check_for_question()` for further runs.


## License

This project is open-source under the MIT License.

### Disclaimer

This project is intended for educational purposes only. Ensure compliance with Chegg's terms of service when using automation scripts.
