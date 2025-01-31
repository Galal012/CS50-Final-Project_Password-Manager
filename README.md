# Password Manager

#### Video Demo: <URL [HERE](https://youtu.be/f0rk9RWbRDE)>

## Description

Password Manager is a secure web application designed to help users store, manage, and generate strong passwords for their online accounts. Built with Flask for the backend, SQLite for database management, and Bootstrap for the frontend, this application provides a user-friendly interface for managing sensitive account information securely. Key features include user authentication, account management, password generation, and user settings.

## Features

### 1. **User Authentication**
   - Register new users with secure password hashing.
   - Log in and log out functionality with session management.

### 2. **Account Management**
   - Users can add, view, edit, and delete saved accounts.
   - Accounts are stored securely, and passwords can be shown or copied as needed.
   - **Account fields** include:
     - Company
     - Username/Email
     - Password

### 3. **Password Generation**
   - Users can generate strong, random passwords by clicking the "Generate Password" button.
   - The app uses a backend method to create passwords, ensuring they are secure and difficult to guess.

### 4. **Search and Filter Accounts**
   - Users can search and filter their saved accounts by company, username, or password.
   - The filtering option allows for a more organized view of stored credentials.

### 5. **Change Password**
   - Users can change their account password by providing their current password and setting a new one.
   - Password changes require confirmation to ensure both passwords match.

### 6. **Secure Storage**:
   - Passwords are stored securely using hashing and encryption.

### 7. **Personal Settings**
   - Users can update personal information, such as their name, phone number, and gender.
   - Once the user enters edit mode, they can update these details and save the changes.

## Files Overview

### Backend Files

#### 1. **`app.py`**:
   - The main backend script that handles routing, user authentication, and account management.
   - Manages user sessions, password hashing, and database interactions.
   - Includes routes for registration, login, account management, password generation, and user settings.

#### 2. **`helpers.py`**:
   - Contains utility functions:
     - `apology(s)`: Displays error messages to users.
     - `login_required(f)`: A decorator to ensure certain routes are only accessible to logged-in users.

### Templates (Frontend Files)

#### 1. **`layout.html`**:
   - The base template for the application, providing a consistent structure and design.
   - Includes a navigation bar, flashed messages, and a footer.
   - Dynamically adjusts content based on the user’s authentication status.

#### 2. **`index.html`**:
   - The homepage, featuring a welcome message and key features.
   - Displays a personalized greeting for logged-in users.
   - Includes call-to-action buttons for new users (Register and Log In).

#### 3. **`login.html`**:
   - The login page for existing users.
   - Includes form fields for username and password.

#### 4. **`register.html`**:
   - The registration page for new users.
   - Includes form fields for name, phone number, username, password, and gender.

#### 5. **`myAccounts.html`**:
   - Displays and manages the user’s stored accounts.
   - Includes a filtering mechanism to search accounts by company, username, or password.
   - Provides options to edit or delete accounts.

#### 6. **`add.html`**:
   - The page for adding new accounts.
   - Includes form fields for company, username/email, and password.
   - Provides buttons to generate a strong password and toggle password visibility.

#### 7. **`edit.html`**:
   - The page for editing account details.
   - Includes pre-filled form fields for company, username/email, and password.
   - Provides buttons to generate a strong password and toggle password visibility.

#### 8. **`delete.html`**:
   - The page for deleting existing accounts.
   - Includes a dropdown to select the company and a text input for the username/email.

#### 9. **`settings.html`**:
   - The page for updating user information and changing passwords.
   - Displays the user’s current information in a read-only format.
   - Allows editing of personal details when the "Edit" button is clicked.

#### 10. **`changePassword.html`**:
   - The page for changing the user’s account password.
   - Includes form fields for the old password, new password, and confirmation of the new password.

#### 11. **`apology.html`**:
   - Displays error messages to users.
   - Used by the `apology()` helper function to handle errors gracefully.

## Technologies Used

- **Frontend**:
  - HTML
  - CSS (Bootstrap for styling)
  - JavaScript (for password toggling and password generation)
  
- **Backend**:
  - Python
  - Flask (web framework)
  - SQLite (for database management)

- **Security**:
  - Password Hashing
  - Session Management

## Setup and Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Galal012/Password-Manager.git
   cd Password-Manager

2. **Install dependencies**: Make sure you have Python and pip installed. Then, install Flask and other dependencies:
   ```bash
   pip install -r requirements.txt

3. **Run the app**: Start the Flask development server:
   ```bash
   flask run

4. **Access the app**: Open a browser and go to http://127.0.0.1:5000/ to start using the app.

## User Instructions

### 1. Register an Account
To begin using the app, you need to **register** an account:
- Click on the **Get Started** button on the homepage.
- Fill in the registration form with your personal details (name, phone number, username, and gender).
- Click **Submit** to create your account.

### 2. Log In
After registration, you can log in to your account:
- Click on the **Log In** button on the homepage.
- Enter your **username** and **password**.
- Click **Submit** to access your account.

### 3. Add a New Account
To add a new account (such as for a website or service):
- Go to the **My Accounts** page.
- Click **Add New Account**.
- Enter the **company name**, **username**, and **password** for the new account.
- Click **Add Account** to save it.

### 4. View and Manage Your Accounts
On the **My Accounts** page, you can:
- View all your saved accounts.
- Search for accounts by **company**, **username**, or **password**.
- Edit or delete accounts by clicking the **Edit** or **Delete** buttons.

### 5. Edit an Account
To modify an existing account:
- Go to the **My Accounts** page and click the **Edit** button next to the account you want to update.
- Update the **company name**, **username**, or **password**.
- Click **Save Changes** to apply the modifications.

### 6. Change Your Password
To change your account password:
- Go to the **Settings** page.
- Click on the **Change Password** button.
- Enter your **old password**, **new password**, and **confirm new password**.
- Click **Submit** to update your password.

### 7. Log Out
To log out of your account:
- Simply click on the **Log Out** button in the settings or homepage.

### 8. Generate Strong Passwords
If you need a secure password:
- When adding or editing an account, click the **Generate Password** button to get a strong, randomly generated password.
- Click **Show Password** to view the generated password.

### 9. Security Tips
- Always use unique passwords for different accounts.
- Regularly update your passwords to enhance security.

## Contributing

#### We welcome contributions to this project! If you would like to contribute, please follow these steps:

1. **Fork** the repository to your own GitHub account.
2. **Clone** your forked repository to your local machine.
3. Create a new branch for your changes:  
   `git checkout -b feature-branch`
4. Make the necessary changes and commit them:  
   `git commit -am 'Add new feature or fix bug'`
5. **Push** your changes to your fork:  
   `git push origin feature-branch`
6. Submit a **pull request** to the main repository.

### Issues

If you find any bugs or issues with the app, please open an issue in the **Issues** section of the repository. You can also suggest improvements or ask questions.

Thank you for your contribution!

## License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.