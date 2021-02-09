from bs4 import BeautifulSoup
import requests
import re


class User:

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def login(self, url):
        payload = {
            'j_username': self.username,
            'j_password': self.password,
            '_eventId_proceed': ""
        }
        _url = url
        s = requests.session()
        s.get(_url)
        soup = BeautifulSoup(
            s.post('https://shib.bu.edu/idp/profile/SAML2/Redirect/SSO?execution=e1s1', data=payload).text,
            'html.parser')
        inputs = soup.find_all('input')
        url_action = soup.find('form').get('action')
        payload2 = {
            "RelayState": inputs[0].get('value'),
            "SAMLResponse": inputs[1].get('value')
        }
        s.post(url_action, data=payload2)
        return s


class Accommodate:
    def __init__(self, session):
        self.session = session
        self.professors = []
        self.pages = 0

    def download_letters(self, include_letter, year):
        last_url = 'https://bu-accommodate.symplicity.com/students/index.php?s=accessibility_request&mode=form&tab=letter&ss=letter'
        self.pages = 1
        while True:
            # print(f'Page: {i}')
            s = self.session.get(last_url)
            soup = BeautifulSoup(s.text, 'html.parser')
            try:
                next_link = soup.find('div', {"class": "lst-paging"}).find('a').find('span', {'class': 'acc_hide'},
                                                                                     text=re.compile('Next'))
                next_link = next_link.parent.get('href')
            except:
                pass
            last_url = f'https://bu-accommodate.symplicity.com/students/index.php{next_link}&tabmode=list'
            print(last_url)

            if year == 'all':
                letters = soup.find_all('li', {'class': 'list-item'})
            else:
                letters = soup.find_all('span', {'class': ''})
                l = []
                for letter in letters:
                    if letter.find(text=re.compile(year)):
                        l.append(letter.parent)
                letters = []
                for letter in l:
                    letters.append(letter.parent)
            if not letters:
                print("No letters")
                break
            for letter in letters:
                url_letter = 'https://bu-accommodate.symplicity.com/students/index.php' + letter.find('a').get('href')
                letter_load = self.session.get(url_letter, stream=True)
                soup = BeautifulSoup(letter_load.text, 'html.parser')
                prof_name = soup.find('span', text=re.compile('Dear')).text.replace("Dear ", "").replace(":",
                                                                                                         "").split()
                self.professors.append(prof_name)
                pdf = self.session.get('https://bu-accommodate.symplicity.com/students/index.php?generate_pdf=1')
                with open(prof_name[0] + prof_name[1] + '.pdf', 'wb') as f:
                    f.write(pdf.content)
                if include_letter:
                    with open(prof_name[0] + prof_name[1] + '.txt', 'w') as f:
                        f.write(
                            f"Hello {prof_name[0]} {prof_name[1]},\n\nHere is my accommodation letter for the Spring 2021 "
                            f"semester.\n\nThanks, \nYanni")

            if next_link is None:
                break

            self.pages += 1


def main():
    user = User('USERNAME', 'PASSWORD')
    session = user.login('https://c222-shib.symplicity.com/sso/')
    ac = Accommodate(session)
    ac.download_letters(False, "all")
    print(ac.professors)
    print(ac.pages)


if __name__ == "__main__":
    main()
