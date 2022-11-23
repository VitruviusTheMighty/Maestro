# Linux Terminal Cheatsheet,
*Adapated to markdown from (https://dev.to/cleancodestudio/linux-terminal-cheat-sheet-useful-for-beginners-2e6c)*

## Navigation Commands:

`passwd` - change password

`ls` - list directory (Can point at any point on the machine)
            -`la` a flag that lists all + permissions and hidden files

`pwd` - print working directory - check where you're at

`cd` - change directory (Can address at any point in the machine file system)

`mkdir` - make directory

`rmdir` - remove director

`rm` - remove files

`echo` - sends data (if no destination is given than data is sent as output to the terminal)

`cp` copy a file (cp [source] [desintation])

`mv` - mv a file (mv [source] [desintation])

`locate` - locate a file on the machine (locate [filename])

`updatedb` - updates the directory database (must run before running locate)

`man` - manual page of any command

`grep` - search for the following words (can be used to check if a file contains specific info)

## Linux is case sensitive so be aware of your capital letters!

`./` - your directory right now

`../` - previous folder

`~` - the users root folder

`|` - pipe the output of one command into another

`>` - use command on the following file (overwrite)

`>>` - use command on following file (appends)

## Privilege's and user commands:

`cat` - reads a file to the terminal

`chmod` - changes permissions for a file

`adduser` - make a new user

`sudo` - give root permissions for the following command being executed

`su` - switch user

## Network Commands:

`ifconfig` - print network information

`iwconfig` - wireless network information

`ping` - ping an ip address (-c flag lets you define how many times you wish to ping the given ip address)

`arp -a` - send out an arp request to check for machines on the network

`netstat -a` - shows all open ports and what is connected to these ports

`route` - shows a routing table

## Viewing, creating, and editing commands:

`history` - lists the 15 commands you entered (history | grep [command] shows all the times you run a command on the machine (including specific syntax))

`touch` - create a file

`nano` - use the nano text editor

`apt-get` - install [program name] - install a program on the machine (can be run without the install)

`apt install` - install a file from the system / kali - server

`apt purge` - program name - (You have to use the * *)

`pip install` - run an installer for local files

`git clone` - clone a github repository (This is a plugin and does not come preinstalled on most linux distributions!)
