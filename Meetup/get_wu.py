import requests
import os
from time import sleep

class Api:
    def __init__(self):
        # Import HTB token
        with open('token.txt', 'r') as t:
            token = t.read().strip('\n')
        
        self.base_url = "https://labs.hackthebox.com"
        self.headers = {
            "user-agent": "HTB-API",
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token}

    def call(self,endpoint):
        return requests.get(self.base_url + endpoint, headers=self.headers, allow_redirects=True)

    def get_retired_machines(self):
        print("[*] Querying the API for retired machines list")
        api_url = "/api/v4/machine/list/retired/paginated?per_page=100"

        machines = []
        for i in range(1,5):
            machines.extend(self.call(api_url + "&page=" + str(i)).json()['data'])
            print(f"[+] {len(machines)} retired machines loaded")
        
        return machines

    def handle_machine_writeup(self, boxos, diff, name, id):

        if not os.path.exists(f"./writeups/{boxos}-{diff}-{name}-{id}.pdf"):
            print(f"[+] Downloading report for {name}")
            # Download writeup
            api_url = "/api/v4/machine/writeup/"

            with open(f"./writeups/{boxos}-{diff}-{name}-{id}.pdf", "wb") as o:
                wu = self.call(api_url + str(id))
                if wu.status_code == 200:
                    o.write(wu.content)
                    print(f"\033[0;32m[!] Report for {name} downloaded as {boxos}-{diff}-{name}-{id}.pdf \033[0m")
                    sleep(3)
                elif wu.status_code == 404:
                    print(f"\033[0;31m[!] Report for {name} is not available on HTB API. SKIPPING \033[0m")
                    o.close()
                    os.remove(f"./writeups/{boxos}-{diff}-{name}-{id}.pdf")
                elif wu.status_code == 429:
                    print(f"\033[0;31m[!] Rate limit reached on HTB API. Waiting {int(wu.headers['retry-after'])+3} seconds \033[0m")
                    # Wait as instructed then relaunch
                    sleep(int(wu.headers['retry-after'])+3)
                    o.close()
                    os.remove(f"./writeups/{boxos}-{diff}-{name}-{id}.pdf")
                    handle_machine_writeup(boxos,diff,name,id)
        else:
            print(f"\033[1;32m[!] Report for {name} already found as {boxos}-{diff}-{name}-{id}.pdf. SKIPPING \033[0m")

    def get_all_writeups(self):
        machines = self.get_retired_machines()
        for machine in machines:
            self.handle_machine_writeup(machine['os'],machine['difficultyText'],machine['name'],machine['id'])


# What to do on script launch
if __name__ == '__main__':
    wrapper = Api()
    wrapper.get_all_writeups()

