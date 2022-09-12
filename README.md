# Project Cole
Zelda: Ocarina of Time Actor Parameter Viewer/Editor.

## Features
- Searching an actor from the list (with filters)
- View an actor's parameter list
- Delete an actor of the list
- Button to change the actor file

## Planned Features
- Edit actor parameters to get the hex value
- Reverse the param process, from hex to values on the UI
- Add an actor in the list

## TODO
- Avoid reloading the UI when an actor is deleted
- "Delete All" button (and/or "delete range")

## How it works
When the program initialises, it creates all the necessary widgets and then hides them (otherwise you can see them on the UI). Then, when we need to show the widgets, it hides the ones that are currently displayed, removes the row and shows the new widgets on a new row.

Basically, it's like the way Blender works with PR #56, generating everything on initialisation and then showing/hiding as needed.

## Requirements
- Python 3.7+ (done with 3.10, untested with previous versions but should work)
- PyQt6

## Contributions are welcome!
This project use Black to format the code properly
