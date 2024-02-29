# JetBrains Master Password Recovery
You can use this tool on Windows to recover the master password used to encrypt the KeePass keybox file, `c.kdbx`. This allows you to recover saved passwords that you have forgotten.

# Usage
```
pip install pywin32 pycryptodome
python getpw.py path_to_c.pwd
```

# Background
The KeePass database used on Windows by tools like DataGrip to store passwords is encrypted with a password that itself is encrypted twice. It is first encrypted with a static password within the IntelliJ source code, and then again with the Windows Credential Store (i.e. the current user's Windows credentials).

This program reverses that process for a given `c.pwd` file.

# Tips
- This has been tested with Jetbrains DataGrip 2023.3. Other JetBrains products and/or versions of DataGrip may not be compatible with this tool.
- The `c.kdbx` and `c.pwd` files for me were saved in `%APPDATA%\JetBrains\DataGrip2023.3`, but you should find the path that is correct for your version of DataGrip.
- Once the password is recovered, you can simply double click the `c.kdbx` file to open it in KeePass, and then paste the password provided in. This of course requires KeePass to be installed.
- You should not tamper with the KeyPass DB! Use this only to recover passwords you have forgotten. The password IDs correspond to IDs elsewhere in the XML configuration files.
- If you don't know what this tool is or does then I recommend you don't use it. It is for advanced users only.
- Your mileage may vary! It worked for me, but may not work for you.
- This tool is in no way affiliated with JetBrains.
- Use it at your own risk. I don't take any responsibility for your actions :)
