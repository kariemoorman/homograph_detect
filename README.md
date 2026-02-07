<p align='center'><img src='homograph.png' alt='img'></p>
<p align='center'>homograph-detect</p>



---

## Description 

A simple, easy to interpret Python wrapper that intercepts downloads from `curl` and pipes the output through a Unicode homograph filter.

---

## Filter Options

There are 2 options for `curl` filtering: 

### [check_piped_curl.py](https://github.com/kariemoorman/homograph_detect/blob/main/src/src/check_piped_curl.py)

- If stdout is a terminal → just run the real curl directly (os.execv) → bypasses the homograph filter
- If stdout is piped or redirected → run curl → pipe output through `homograph_filter.py`

### [check_all_curl.py](https://github.com/kariemoorman/homograph_detect/blob/main/src/check_all_curl.py)

- Always filters curl output through `homograph_filter.py`, whether it’s going to a terminal, pipe, or file
- Uses line-buffered output so the homograph filter sees content immediately

---

## Installation & Use

- Create a target directory on your local machine:

```bash

mkdir -p ~/scripts

```

- Download scripts from repo, and place in target location:

```bash

git clone https://github.com/kariemoorman/homograph_detect.git
cd homograph_detect/src
mv *.py ~/scripts/

```

- Make scripts executable:
  
```bash

chmod +x ~/scripts/check_piped_curl.py
chmod +x ~/scripts/check_all_curl.py
chmod +x ~/scripts/homograph_filter.py

```


- Create aliase for `curl` using function you want (piped commands only vs. all curl commands) and update the shell environment:

```bash
nano ~/.zshrc

alias curl="$HOME/scripts/check_piped_curl.py"
or
alias curl="$HOME/scripts/check_all_curl.py"

source ~/.zshrc

```

- Test changes:

```bash

printf "ok а\n" > test.txt
curl file://"$PWD/test.txt" | cat

❌ Blocked: suspicious Unicode (possible homograph attack)

```


If using `check_all_curl.py`:

```bash

printf "ok а\n" > test.txt
curl file://"$PWD/test.txt"

❌ Blocked: suspicious Unicode (possible homograph attack)
```


That's it! Use `curl` as you normally would.
