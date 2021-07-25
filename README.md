# 2048-Game Pytho
First project after 2.5 months of learning Python

Game 2048 written in Python, pygame module. 
Also used SQLite for the database of players and their results
***
### Controls & Keys
| Key | Move |
| :---------------: | :---------------: |
|  H / h | Returns to the main menu, saving game progress |
| R / r | Resets the game to a further agreement |
| B / b | Returns the state of the game that was 1 turn ago |

### Other Keys
| Key | Move |
| :---------------: | :---------------: |
|  Backspace | Cancels the action |
| Escape | Leaves the game or cancels the action |
| Enter | Confirms action |
Mouse swipes are also available within the game area. At least 30 pixels
***
### The project consists of 3 .py files
1.	main
2.	logics
3.	database
***
## main
>Contains the main game loop
> 
>Handles click events
> 
>Renders the window, updating it

Very mediocre architecture of the game, due to the lack of planning of the game and its components, as well as improvisation.
I wanted to apply OOP, but due to the lack of any experience, I did not figure out exactly how to do it:

## logics
>Contains the core 2048 logic as functions that can be defined outside of main. Due to namespace considerations

I decided to write __doc__ for each function, but something turned out not what I wanted, but still better than nothing.
(yes, yes, there is in Russian, but there is a google translator, otherwise how would I write it?)

## database
>Contains requests to get player results
> 
>Their processing and processing format

Using my flexible thinking (code crutches), I somehow managed to get the SQLite query and their processing right
***
The repository has a development branch with a data.txt save file in JSON format. It won't go away.
You can change it and see the result in the game
Also in this thread there are unit tests that were used in the testing process 2048. (tests are as simple as possible,
I did not particularly try to complicate them)
***
The project had about 5 or 7 versions, and each had a huge number of differences and changes compared
to the previous one, but then I did not know about the git. But now I found out, but those versions are gone.
So the repository contains probably an almost finished project ... Nevertheless, the project is far from ideal, and 
I understand that it was possible to get by with 200-300 lines or use a more thoughtful architecture, OOP, etc.
As an excuse))) this is my first * big project (more than 100 lines), well, let it be as it is)