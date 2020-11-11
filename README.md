# KVC-version-control
Local version control system <br/>
Memory optimized by saving only unique files each commit(like git does) <br/>
Works on Windows (Possibly Linux also, but not tested yet)
## Installation
Clone repository to Your chosen directory<br/>
Add directory to the system path
 
## Usage
Go to your project directory, and open Command Prompt
```bash
kvc_main.py init #Initialize kvc repository at current directory
```
```bash
kvc_main.py commit (optional message) #Saves changes 
```
```bash
kvc_main.py commit-prev #Restores repository to last saved commit
```
```bash
kvc_main.py commit-jump (commit name) #Restores repository to chosen commit
```
```bash
kvc_main.py commit-list #Prints out last 10 commit at current branch
```
```bash
kvc_main.py commit-list-full #Prints out all commits at all branches
```
```bash
kvc_main.py branch-creation (branch name) #Creates new branch
```
```bash
kvc_main.py branch-swap (branch_name_from) (branch_name_to) #Changes current working branch
```
```bash
kvc_main.py branch-merge (branch_name_being_merged) (branch_name_merged_to) #Merges 2 branches
```
