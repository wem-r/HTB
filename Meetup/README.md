
# HackTheBox


Generate a thumbnail for the HTB Meetup France Using the [HackTheBox API](https://documenter.getpostman.com/view/13129365/TVeqbmeq)


To communicate with the API v4, you need an **App Token**. \
Go to https://app.hackthebox.com/profile/settings and <kbd>Create App Token</kbd> (<small>This does not work on the old interface, you need to use the new one</small>)

---

## Requirement

- Create a `token.txt` with your App Token in it
- To keep the HTB color theme, I used the [official style guide](https://www.hackthebox.com/docs/Hack_The_Box_Brand_Assets_Guide.pdf) and the font `Zeitung Micro Pro` (<sup>google is your friend</sup>).

---

## Usage


- Set the Meetup number/name with :
    - `-n` / `--number` :
- Set the date of the Meetup with :
    - `-d` / `--date` :
- Set the differents machines names with
    - `-m1` / `--machine1`
    - `-m2` / `--machine2`
    - `-m3` / `--machine3`


Exemple: 
```bash
python3 Gen_Thumbnails.py -n 0x0f -d "January 19 2038"  -m1 Optimum -m2 Search
```
