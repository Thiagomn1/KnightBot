# Lore Keeper Discord Bot

#### Video Demo:

#### Description:

For final project in CS50 i developed a discord bot using Python and the Discord.py library with it's main purpose being to replicate messages with the dialogue box from the game Final Fantasy XIV and Fate Grand Order, along with other secondary functions.

For the dialogue box command, by using ".rp Name | Message", the bot generates an image using Pillow containing their message in the format of the game dialogue chosen by the user.

Other functionalities include sending a custom Emded message for every new member that joins, with a custom message set by the moderator with the ".welcome" command, along with some moderation commands like banning, unbanning members or clearing chat messages.

A SQLite database was also implemented with two main purposes, one allowing the user to set a default name for the dialogue command, by doing so not needing to type down their name at every command input and just their message instead. The second funcionatity being the option for them to set a custom welcome message for their server to send when a new member joins.
