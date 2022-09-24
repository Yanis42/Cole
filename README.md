# Project Cole
Zelda: Ocarina of Time Actor Parameter Viewer/Editor.

## Features
- Searching an actor from the list (with filters)
- View an actor's parameter list
- Delete an actor of the list
- Button to change the actor file
- Edit actor parameters to get the hex value
- Safe ``eval()`` function to avoid any security issues, from [Fast64](https://github.com/fast-64/fast64)
- Copy the parameters in the clipboard by clicking on the label next the parameter/rotation textbox of your choice
- Reverse the param process, from hex to values on the UI (need extra testing)

## Planned Features
- Add an actor in the list
- A list on the UI containing the current flags of the scene and warn if one is already used (Ticamus)

## TODO
- Avoid reloading the UI when an actor is deleted (?)

## How it works
When the program initialises, it creates all the necessary widgets and then hides them (otherwise you can see them on the UI). Then, when we need to show the widgets, it hides the ones that are currently displayed, removes the row and shows the new widgets on a new row.

Basically, it's like the way Blender works with PR #56, generating everything on initialisation and then showing/hiding as needed.

## Requirements
If executing from source, you will need the following:
- Python 3.7+ (done with 3.10, untested with previous versions but should work)
- PyQt6
- (Optional) PyInstaller if you want to build an executable. Note that antiviruses might get angry, if you have any doubt the source code is available.

## Contributions are welcome!
This project use Black to format the code properly
