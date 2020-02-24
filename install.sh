#!/bin/bash
echo "Welcome to CanvasCLI Installer."
echo "This will allow you to submit assignments directly in Linux shell."
echo "An alias will be made, 'canvas', to use the CLI."
echo -n "Install now? (y/n) "
read answer
if [ "$answer" != "${answer#[Yy]}" ] ;then
    mkdir ~/.canvas
    cp cli.py ~/.canvas/cli.py
    alias canvas='python3 ~/.canvas/cli.py'
    echo >> ~/.bashrc
    echo "alias canvas='python3 ~/.canvas/cli.py'" >> ~/.bashrc
    echo >> ~/.bash_profile
    echo "alias canvas='python3 ~/.canvas/cli.py'" >> ~/.bash_profile
    echo "Install complete."
else
    echo Goodbye
fi