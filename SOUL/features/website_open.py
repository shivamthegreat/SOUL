
import webbrowser
import re

def website_opener(domain_or_url):
    # If it looks like a full URL with scheme (http/https), just open it
    if domain_or_url.startswith("http://") or domain_or_url.startswith("https://"):
        url = domain_or_url
    else:
        # Check if it contains a slash indicating a path
        if '/' in domain_or_url:
            domain, path = domain_or_url.split('/', 1)
            path = '/' + path
        else:
            domain = domain_or_url
            path = ''

        # Add .com if no dot in domain
        if '.' not in domain:
            domain += '.com'
        
        # Validate domain
        if not re.match(r'^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', domain):
            print("Invalid domain format.")
            return False

        url = f'https://www.{domain}{path}'

    try:
        webbrowser.open(url)
        print(f"Opening {url}")
        return True
    except Exception as e:
        print(f"Failed to open {url}. Error: {e}")
        return False

# --- Take user input and call the function ---
#user_input = input("Enter the website domain or full URL: ")
#website_opener(user_input)
