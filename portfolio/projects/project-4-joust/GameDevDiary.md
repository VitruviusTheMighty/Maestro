# Game Dev Diary / Log - Leonardo Ferrisi

## Entry 1:

Initially I spent a good amount of time keyframing out a character from an old cartoon.
This character, whose model and associated demo is now available at: `https://github.com/VitruviusTheMighty/Maestro/tree/main/portfolio/src/week5/sprites`

Where the demo can be run using `python simple_platform.py` when in the associated directory.

This character sprite though fun to have made has some glaring flaws, mainly a collision mask that is incredibly
inconsistent in behavior given how fluid the character changes between animation frames.

I ended up moving to a different character sprite.

## Entry 2:

My next attempt involved making a more pixelated sprite so as to allow more square collisions, but I kept running into the issue of how to keep a sprite on top of any platform.

Sprite keeps falling through.

### Entry 3:

I settled on a new sprite whose sprite sheet I pulled from itch.io. I chose this cat spritesheet due to its pixelated form and also it looks nice.
I added an idle animation for the sprite to use when not moving.
In order to repair the platforms not being solid issue I added a loop that checks if the play is colliding **and** above each of the platforms, and setting its y - velocity to zero if it is greater than 1 in such a case, otherwise apply the effects of gravity.

All in all the, sprite can sucessfully hop between platforms or jump onto them from the ground.
