# Flask SQLi & XSS Lab

A vulnerable web application demonstrating SQL Injection and Cross-Site Scripting (XSS), two of the OWASP Top 10 most critical web vulnerabilities. Built to understand how attackers gain initial access to systems, and how developers can prevent it.

## Motivation

In my senior year of high school, my school was hit by a ransomware attack. I didn't know how it happened, and that unknowing is what pulled me into cybersecurity. This project is my attempt to answer the question: how do attackers actually get in before deploying something like ransomware?

Ransomware doesn't appear out of nowhere. Attackers need an entry point first. This project simulates two of the most common ones.

## The Attack Chain

This project demonstrates the initial access phase of a real attack chain.

1. Attacker finds a login form or search box exposed to the internet
2. Attacker injects malicious input to manipulate the application
3. Application trusts the input and executes it, either in a database query (SQLi) or in the browser (XSS)
4. Attacker gains unauthorized access or executes malicious scripts
5. From here, an attacker could move laterally through the network and deploy ransomware

This is exactly how the 2023 MOVEit breach worked. A SQL injection vulnerability gave the Clop ransomware group initial access to thousands of organizations including British Airways and the U.S. Department of Energy.

## About the App

Built with Python, Flask, and SQLite. I deliberately kept it minimal so I could focus entirely on understanding how vulnerabilities exist at the code level rather than using existing vulnerable apps like DVWA.

The app has four routes:

- `/login` — vulnerable to SQL injection
- `/login-secure` — patched with parameterized queries
- `/search` — vulnerable to XSS
- `/search-secure` — patched with Jinja2 auto-escaping

## SQL Injection (SQLi)

The vulnerable login route builds the SQL query by directly inserting user input:
```python
query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
```

Injecting `' OR '1'='1'--` as the username causes the database to execute:
```sql
SELECT * FROM users WHERE username='' OR '1'='1'--' AND password=''
```

The `--` comments out the password check. Since `'1'='1'` is always true, login succeeds without valid credentials.

<img width="1728" height="1117" alt="Screenshot 2026-04-01 at 11 25 09 AM" src="https://github.com/user-attachments/assets/8deed6f1-cb17-4ffd-a68b-9e4dddbf9a1c" />

Intercepted and manipulated using Burp Suite Repeater to confirm the exploit at the HTTP request level:

<img width="1728" height="1117" alt="Screenshot 2026-04-01 at 11 06 03 AM" src="https://github.com/user-attachments/assets/7c8bfbb8-3547-4b9c-a441-67cad64f6813" />

The payload was URL encoded using CyberChef before being sent through Burp. Characters like `'` and `=` have special meaning in HTTP request bodies and need to be percent-encoded so they transmit correctly:

<img width="1722" height="961" alt="Screenshot 2026-04-01 at 11 16 40 AM" src="https://github.com/user-attachments/assets/4786d230-cce6-4a4a-bb61-fd989ef4dd17" />


The fix uses parameterized queries, which separate SQL structure from user input so the database never interprets input as code:
```python
query = "SELECT * FROM users WHERE username = ? AND password = ?"
cursor.execute(query, (username, password))
```

<img width="1728" height="1117" alt="Screenshot 2026-04-01 at 11 17 59 AM" src="https://github.com/user-attachments/assets/95071fb4-863b-45d4-b6a7-a6654bf379da" />

## Cross-Site Scripting (XSS)

The vulnerable search route returns user input directly in an f-string without sanitization:
```python
return f"<p>Search results for: {query}</p>"
```

Injecting `<script>alert("XSS")</script>` as a search query causes the browser to execute the script. In a real attack this script could steal session cookies, log keystrokes, or redirect users to a phishing page.

<img width="1728" height="1117" alt="Screenshot 2026-04-01 at 11 24 51 AM" src="https://github.com/user-attachments/assets/a88e52e9-899b-4144-9b40-5cf7bc4e7c8c" />


Intercepted using Burp Suite Repeater to confirm the raw unescaped script tag in the HTTP response:

<img width="1728" height="1117" alt="Screenshot 2026-04-01 at 11 23 18 AM" src="https://github.com/user-attachments/assets/edc6efcb-5b66-4fda-ae66-e18118b86d66" />

The payload was URL encoded using CyberChef before being sent through Burp:

<img width="1696" height="925" alt="Screenshot 2026-04-01 at 11 22 29 PM" src="https://github.com/user-attachments/assets/90a3fbe4-51db-48f6-adc3-e2fed1d1a5f2" />


The fix passes input through Flask's Jinja2 template engine, which auto-escapes HTML by default:
```python
return render_template("search_secure.html", query=query)
```

The same payload renders as harmless plain text instead of executable JavaScript.

<img width="1728" height="1117" alt="Screenshot 2026-04-01 at 11 26 52 AM" src="https://github.com/user-attachments/assets/63b2fe66-9b01-41c2-8fae-de522803aea3" />


## Tools Used

- Python 3 and Flask for the web application
- SQLite for the database
- Burp Suite Community Edition for intercepting and manipulating HTTP requests
- CyberChef for URL encoding payloads

## How to Run
```bash
git clone https://github.com/wonbinsoup/flask-sqli-xss-lab.git
cd flask-sqli-xss-lab
pip install flask
python3 app.py
```

Visit `http://127.0.0.1:5000` in your browser.

## Author

Daniel W Kim — CS student @ Northeastern University, focusing on Application Security.
