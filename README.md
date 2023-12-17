# ScratchStream
Stream your desktop to Scratch (the block programming website)

A Scratch/Python program that streams your desktop to the kid's programming language Scratch. I've done something similar before but with JS and I thought it would be a fun idea to try this. 

I wrote my own protocol to transfer images in chunks to work with Scratch's cloud variable limitations. It's able to stream your desktop at a maximum resolution of `16x16` due to Scratch limitations. However, you may be able to increase this by sending multiple sets of chunks consecutively and writing some code in Scratch to combine them all but this would sacrifice latency. 

**How It Works**<br>
Scratch allows you to create up to 10 cloud variables per project. Each variable can store up to 256 characters.
> Cloud variables in Scratch are variables that are synced across every instance of the project being run

Since Scratch cloud variables can only store numbers, anything sent in this project has to be in numerical form to later be decoded in Scratch. <br><br>

An image is simply an array of pixel colors. Colors can be represented in a variety of ways like hex and rgb. Because the amount of data I can send over the cloud is limited, I want to send the image in a way that uses the least amount of characters. Each hex color is 6 characters, however hex values include A-F which means I would have to encode the hex string before sending it over making it a total of 12 characters. 
> The shortest way to encode a string in Scratch to numerical values is to just represent each character as 2 numbers. The amount of combinations that you can create with 2 digit numbers is 100 `00`-`99`. Therefore you can easily represent a-z A-Z 0-9 and even some symbols in encoded format. However, encoding the string increases the string length by a factor 2.

rgb is represented by (r, g, b) where r, g, b can range from 0-255. The minimum value that a rgb string can hold is 3 and the maximum is 9. However, there is no way to tell where a color starts and ends if you just pack it all together so there has to be a set length for the colors which is 9. The remaining space will be taken by a placeholder digit like 0 since putting 0 in front of a number preserves the value of the number. 9 characters per color is not that bad considering hex takes 12. Now we can calculate the *maximum* amount of pixels that we can send over. The calculation is simple, Scratch allows 10 cloud variables which contain 256 characters each for a total of 2560 characters. We divide this by 9 for a total of about `280`~ pixels. The image has to be a square or else you would have to indicate the size of it somehow so that Scratch decodes it correctly. Taking the square root of `280`~, we get about `16.7` which we now have to take the floor of. We can send an image 16x16 pixels large to Scratch with these limitations. Coincidentally, using 9 cloud variables can also represent a 16x16 pixel image exactly leaving you 1 extra variable. 
<br><br>
The last step is just to get our desktop as an image using the `dxcam` library and resize it so that it's 16x16 in size. We convert that to an array of pixels and add zeroes in front of rgb values less then 100 to ensure that each rgb color has a length of 9. We can combine all these rgb values into 1 huge string and then split it up into smaller chunks of 256 to then send over to Scratch.
<br><br>
On the Scratch side, you simply need a program to detect when the last chunk has changed and then combine all the cloud variables and split them into segments of 9. Next, just take the square root of the length of the segments and iterate over the colors to draw them out. 

![image](https://github.com/wa1ker38552/ScratchStream/assets/100868154/6639d763-274f-4183-9454-3a3fb787f81d)
