# CanvasCLI
Allows user to submit an assignment to Canvas using the command line.

***Currently in development.*** Cannot submit assignments at this point.

## Installation Instructions
1. Clone repo to machine: `git clone https://github.com/etekweb/CanvasCLI.git`
2. Run the installer in current context: `. install.sh` (installer currently for macOS/Linux only)
3. Use `canvas` command to start setup

## Setup
You will need an access token from Canvas.
To get this, log into Canvas online, go to Account -> Settings, scroll to Approved Integrations, and press New Access Token.
Set the token to never expire. You can revoke it at any time in the Canvas settings above.
Then, copy and paste the token into the program when prompted.

You will need to know what your Canvas URL is as well.
When prompted, input just the subdomain for your school. 
For example, if you visit https://mtu.instructure.com to log in normally, type `mtu` when prompted.

## Usage
1. Run `canvas <filepath-to-upload>`
2. Set up with access token and Canvas domain if not done yet
3. Select class number from given list
4. Select assignment number from given list
5. (tbd)

## Todo
A lot.
