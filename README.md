# Brainf*** interpreter
A Brainf __interactive__ interpreter written in pure Python.
https://en.wikipedia.org/wiki/Brainfuck

## About

This interpreter has a rather basic implementation of brainf***. For commands `+ - < > , .` you can read on the linked <a href="https://en.wikipedia.org/wiki/Brainfuck">wikipedia article</a>, however when it comes to loops (`[` and `]`):<br>
The `[` symbol checks the current pointer position and if the value is __not__ 0 it proceeds with the command inside brackets and if the value __is__ 0 it skips to the corresponding `]` symbol and proceeds with the program. The important thing is, that `]` (loop end symbol) only logic is to return to the corresponding `[` (loop start symbol). The implication of that logic is that it is rather slower on larger programs, because we need to go back to the begginning of the loop only to see that wee need to go back to the end in case of current value is 0.

# How to run

## File
To interpret a file, just type in console:<br>
`python brainf.py <path_to_bf>`<br>
Where `<path_to_bf>` is path to a valid brainf*** program.

<a href="https://ibb.co/rQpbn5X"><img src="https://i.ibb.co/vcds2LM/obraz.png" alt="obraz" border="0"></a>

## Interactive

`brainf.py` can be run (and You should try it, its fun!) in an interactive mode, where you can type any valid brainfuck code and interpreter will show you the current state of the interpreter table: where the pointer is and what values are in the nearset cells.<br>
Just type `python brainf.py` in terminal and you are good to go.

<a href="https://ibb.co/ZW7Jhkt"><img src="https://i.ibb.co/f4LSCPB/obraz.png" alt="obraz" border="0"></a>

You can run a command and see what it did:

<a href="https://imgbb.com/"><img src="https://i.ibb.co/jJHn7dt/obraz.png" alt="obraz" border="0"></a>

Does my loop work as intended?

<a href="https://imgbb.com/"><img src="https://i.ibb.co/Zg6HPxs/obraz.png" alt="obraz" border="0"></a>

Wow, it DOES!<br>
Brainf.py comes also with a few utility functions like:
 * `undo` - like the name suggests, undoes previous executed command (only one for now, no history)
 
 <a href="https://imgbb.com/"><img src="https://i.ibb.co/CMby5rt/obraz.png" alt="obraz" border="0"></a>
 
 * `reset` - resets interpreter to clear state (all cells calues set to 0, pointer on the first cell)
 
 <a href="https://imgbb.com/"><img src="https://i.ibb.co/YbLv7sQ/obraz.png" alt="obraz" border="0"></a>
 
 * `quit` - and of course standard interactive command that quits the program.
 
 <a href="https://imgbb.com/"><img src="https://i.ibb.co/PTGKKBM/obraz.png" alt="obraz" border="0"></a>
 
 Don't wait, learn and develop in brainf.py today!
