## Which package/library did you select?
I selected the package Python Arcade, or more simply just Arcade

## What is the package/library?
Arcade is meant to be used to create 2D video games. A program for an Arcade game will start with defining constants such as screen size, title, the size and scaling of sprites and tiles, player movement, player start location, layer names, camera constants, basically everything with a one-time defined value. Then there is a function to load a texture pair, essentially used so that you only need to upload one image of a character action and the game can use it for both left and right versions of the action. After that we get into a few classes. The ones that are fairly necessary are Entity, PlayerCharacter, and a MainGame class (to run the bulk of the game). Classes that are unneccesary but supported are classes for other entities, such as enemies or NPCs, and more Game classes for if you wish to have more than one map, a start screen, a game over screen, or any other screen. The Entity and related classes (PlayerCharacter and Enemy) are mainly use to set textures and animations for various actions, such as walking, jumping, and climbing. The functionality for each of these actions goes into the game window class. The main game class will have a function to initialize everything and load in sounds. Then there will be a setup function that will initialize the physics engine, load in sprites as well, as set up a camera if you've chosen to use one. There are a handful more functions that will be where you handle pressed buttons and updating everything such as checking and dealing with collisions. Most everything after that is based on your own creativity. In order to actually create these classes and functions, arcade provides all the functions you could need for manipulating sprites, maps, cameras, and controls.

## What are the functionalities of the package/library?
The functionality is to create and run a game. This means providing functions and methods for manipulating sprites, text, key presses, collision, and pretty much everything a simple game need and it does all of this fairly efficiently as well.  
This is what the game looks like at the start: ![Screenshot of the game upon startup.](https://i.imgur.com/ytwD3Z4.png)  
  
This is what the game looks like at the end: ![Screenshot of the game on endscreen](https://i.imgur.com/sWIeKfj.png)
As you can see many of the spikes have disapeared using the code:
```
self.scene[LAYER_NAME_SPIKE] in collision.sprite_lists  
    arcade.play_sound(self.game_over)  
    self.score -= 50  
    collision.remove_from_sprite_lists()  
    self.restart()
```  
which was one of my favourite parts to write. It is a good example of using several of the provided functions such as ```play_sound()```, ```remove_from_sprite_lists()```, and ```collision.sprite_lists```, which is a vairable defined through ```arcade.check_for_collision_with_lists()```. But along with those provided functions, ```restart()``` is a function that I made myself that essentially resets the players speed and position to their starting values without resetting the other sprites. Speaking of the ```play_sound()```, my game uses some of the provided resources for sounds. There are also lots of pre-made visual assets as well but I choose to make my own.  
There are also three physics engines provided by Arcade, my game uses the intermediate one, ```arcade.PhysicsEnginePlatformer```.

## When was it created?
The first version still listed on their site is Version 1.2.2, released on December 2nd 2017. It was last updated in December of 2022 [[ref]](https://api.arcade.academy/en/latest/development/release_notes.html#version-2-6-17).


## Why did you select this package/library?
I selected this package because I once saw a youtube video of a guy making a game in python. Though that video was done using the Pygame library, I decided wanted to try something similar and looked into more game development packages. Arcade stuck out to me as not too complicated but still very versitile and a 2D platformer is what I had in mind already, so my vision fit nicely with what Arcade is. 

## How did learning the package/library influence your learning of the language?
Honestly it was only so-so for my learning of the language. I definitly learned some things about working with classes and objects in Python but overall most of the code is just manipulating a few variables with if statements and a lot of the basic structure came from the site. However, what was a good learning experience was when I wanted to change those basic structures to do what I wanted and needing to read though the documentation, which wasn't always easily acceseble or clear like a language's official documentation usually is. This on top of using a small library means not as many people are asking about their problems with it on the web either. Something as simple as centering text required me to troubleshoot through several errors because I couldn't find more info on the ```arcade.draw_text``` function to figure out what was going wrong. I managed to figure it out in the end instead of giving up and trying to guess and check at a pixel location, which is a positive learning situation in and of itself.

## How was your overall experience with the package/library?
I had a pretty good experience with this package, and I'm likely going to polish up this project a bit more, though I mainly want to add my own sounds and music instead of relying on provided ones. I can definitely see myself trying it again in the future as it was super fun to work through and see the results of what I made. I'd recomend this package to others. Probably not if they intend on making anything too complicated, but if they just want a small creative project to work on this is definitly a good package to use for that.
