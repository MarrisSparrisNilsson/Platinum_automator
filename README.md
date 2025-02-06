# Platinum_automator

A Python project focused on making gameplay automated in *Pokémon Platinum*

## Description / Background

The initial goal with this project has been to be more familiar with python programming. It's also an exercise to start working with automation. So for this exercise I will try
to make an automation process for the *Pokémon Platinum* game where automation can be applied to many different things.

## Requirements

1. To play the game you need to install a Nintendo DS emulator, such as [DeSmuME](https://github.com/TASEmulators/desmume).
2. You also need a copy of the game with file extension `.nds`
3. Provide the emulator with the path to the game file.
4. Done!

**Note:** This application is only tested on Windows 11 so far. Systems with other operating systems might behave differently.

## Tools and Libraries

> ### [PyAutoGUI](https://pypi.org/project/PyAutoGUI/)
>
> This library will be used to generate I/O into the Nintendo DS emulator.
>
> It can locate things on the screen and give back coordinates that can be used for
> certain calculations.
>
> It can also simulate keyboard presses which are used to control the game and the emulator.

> ### [pytesseract](https://pypi.org/project/pytesseract/)
> Python-tesseract is an optical character recognition (OCR) tool for python. That is, it will recognize and “read” the text embedded in images.
