# GenshinAccountManager
Automatically manages multiple accounts on your hoyoverse account. Redeems and claims your dailies to multiple accounts at once.

## Overview
The `accounts.json` file is a configuration file used by the Genshin Account Manager to store account credentials for seamless management and access. This file simplifies account switching by maintaining an organized list of accounts in JSON format.

## File Format
The `accounts.json` file contains an array of accounts, where each account has a `username` and a `password`.

### Example Format
```json
{
  "accounts": [
    {"username": "test123", "password": "password123"},
    {"username": "sampleuser", "password": "mypassword"}
  ]
}
```

## Fields
### 1. `accounts`
- **Type:** Array of objects
- **Description:** Contains a list of accounts.

#### Account Object Fields:
- **`username`**
  - **Type:** String
  - **Description:** The username of the Genshin Impact account.
  - **Example:** `"test123"`

- **`password`**
  - **Type:** String
  - **Description:** The password associated with the username.
  - **Example:** `"password123"`

## Usage Instructions
1. **Create the `accounts.json` File**
   - Place the file in the designated directory.
   - Ensure the file follows the correct JSON format as described above.

2. **Add Accounts**
   - Add your Genshin Impact accounts to the `accounts` array.
   - Ensure each account has a `username` and a `password` field.

3. **Save the File**
   - After adding your accounts, save the `accounts.json` file.

4. **Run the Application**
   - Launch GAM using `run.bat`

## Notes
- Keep the `accounts.json` secure as it contains sensitive account credentials. Avoid sharing this file.

## Contributing
If you have suggestions for improving the `accounts.json` format or its documentation, feel free to contribute to the Genshin Account Manager GitHub repository.

