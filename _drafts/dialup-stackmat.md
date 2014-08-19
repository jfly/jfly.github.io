---
layout: post
title: Dialup Stackmat
---

It started with a coincidence.

Sometime after my [first Rubik's Cube
competition](https://www.worldcubeassociation.org/results/c.php?i=CaltechSpring2005),
I convinced my mom to buy me a stackmat, the timer used in speedcubing
competitions. One of the first things I noticed about the stackmat was (is? >>>
<<<) that its output port is the exact same size at the i/o port of a TI-83+.

This got me thinking, but first a short digression. (>>> better transition <<<)
I was [very into calculator programming](<<<) in high school. Outside of the
time I spent using it to do actual math, I spent hundreds of hours programming
with that cramped keyboard, and burned through untold quartets of AAA
batteries. I learned that some people had managed to [wire a PS/2 keyboard to
their calculators](http://www.radicalsoft.org/hardware/keyboard/), and it was
something I *had* to try out. A vanilla TI-83+ and general lack of EE knowledge
meant that I never actually got the project working, and my mom eventually made
me move the mess into the garage.

The upshot of all this is (was? >>>) that when my stackmat arrived, I already
had the adapter and cables to plug it into my sound card's microphone jack.

{% include image.html alt="My original stackmat and detritus from the abandoned TI-83+ PS/2 keyboard project" src="dialup-stackmat/stackmat.jpg" %}

The idea of cubing with a stackmat while my computer keeps track of my times
held irresistable appeal to me. Surely someone had written software to do just
this! I was frustrated and amazed when I couldn't find any such project, and
resigned myself to entering times manually.

I graduated from high school in 2006, spent some time that summer deciphering
the stackmat protocol. I'll never forget the thrill of zooming into a recording
and seeing a repeated wave form. I'd feared I'd see total chaos, or nothing.

{% include image.html alt="A stackmat signal I recorded ages ago" src="dialup-stackmat/signal.jpg" %}

After a long time staring at screenshots from Audacity, I was able to decode
stackmat signals by hand (many years later, I learned that I was looking at the 
the [RS-232](http://en.wikipedia.org/wiki/RS-232) standard).
Friends, summer, and other projects kept me from writing a software signal
decoder until my freshman year at Berkeley. I thank [Brian
Harvey](http://www.cs.berkeley.edu/~bh/)'s CS61A course for giving me the
confidence to finally sit down and implement it. <<< NUKE? add as
parenthetical? >>>

I proudly showed my work to the Berkeley cubers after our 
[first competition](https://www.worldcubeassociation.org/results/c.php?i=Berkeley2006).
Conveniently, [Chris Hunt](https://www.worldcubeassociation.org/results/p.php?i=2005HUNT01), the
creator of JNetCube, had driven down from Idaho and was present for my demo. As
I recall, he was excited by the prospect adding stackmat functionality to his
timer, and he gave me his contact info. I was honored and flattered (someone
who had written a *real* piece of software wanted me to contribute?!). I'm sure
that this would have happened if
[Ryan Zheng](https://www.worldcubeassociation.org/results/p.php?i=2006ZHEN02)
had not stepped in. My code had lots of issues, and Ryan wanted to hear about
all of them and fix them. Once he decided to grab his own laptop, we decended
into a full night of hacking. That night lengthened into a full weekend. At one
point, Ryan suggested the unthinkable: rather than just giving this feature to
JNetCube, we could build our own superior timer! That moment was the birth of
[C.A.L. Cube Timer (CCT)](http://cct.cubing.net/).

<<< something about cct being formative/popular, or is it silly to toot my own horn? >>>

As far as I know, I was the first person to plug a stackmat into a computer via
the soundcard. As smartphones became more <<< gah

Once you are able to get the data out of a stackmat, <<< gah

After several rewarding years of working on CCT, I abandoned the project to
work on TNoodle. TNoodle was originally meant to be a rewrite of CCT for the
web, but it evolved strangly and became the [official WCA scrambler
program](https://www.worldcubeassociation.org/posts/wca-documents-updated-january-1-2013). <<< gah

Over the years, discussions of eliminating data entry at competitions periodically occurred. <<< gah

It has been years since CCT was first released. Code to interpret the stackmat
signal has been written in Java, Javascript, and even Flash. Yet in all
this time, no one has plugged a stackmat into a smartphone! This certainly
has not been due to lack of effort.

<<<polish live results thing?>>>

[Dan Cohen](https://www.worldcubeassociation.org/results/p.php?i=2007COHE01)
wrote a stackmat interpreter in Objective-C in July 2010. He got it working in
the iPhone simulator on his computer, but when he loaded it onto his
phone, it just didn't work. The signal he recorded was so distorted as to be unreadable.

In February 2012, I attended a hackathon at Berkeley with the intent of writing a
stackmat to phone interpreter. I was joined by
[Kevin Jorgensen](https://www.worldcubeassociation.org/results/p.php?i=2006JORG01),
[Darren Kwong](https://www.worldcubeassociation.org/results/p.php?i=2005KWON01),
and [Devin Corr-Robinett](https://www.worldcubeassociation.org/results/p.php?i=2006CORR01).
After a few hours, we gave up when we ran into the same
distortion that had thwarted Dan Cohen.

{% include image.html src="dialup-stackmat/dan-cohen-signals.png" alt="Distorted iPhone signal" %}

I'm a software guy. This signal filled me with a combination of dread and
regret that I had not attended more of Professor Boser's 8am EE42 lectures. I
needed a hardware guy to figure out what was going on. Fortunately, I work at a
hardware company. One day my coworker
[Eithan Shavit](http://www.eithanshavit.com/) caught me looking at pictures of
stackmat signals. As luck would have it, Eithan studied EE before getting a job in
software. He was interested in the problem, and had some ideas for fixing it.

Amazingly enough, phones are built to record human voice. Telephones are built
to transmit frequencies between
[300 Hz to 3400 Hz](http://en.wikipedia.org/wiki/Voice_frequency).
While humans are capable of producing tones outside of this range, speech is
still comprehensible when restricted to only that frequency range.

The digital data that comes out of a stackmat looks nothing like human voice.
To conceptualize what a phone does when it sees the square waves of the
stackmat signal, it is necessary to visualize the square wave in terms of its
component frequencies. This exercise is known as [Fourier
analysis](http://en.wikipedia.org/wiki/Fourier_analysis). Fortunately,
Wikipedia has already done this for us.

{% include image.html src="dialup-stackmat/Squarewave01CJC.png" alt='Components of a square wave. From <a href=\'http://en.wikipedia.org/wiki/File:Squarewave01CJC.png\'>http://en.wikipedia.org/wiki/File:Squarewave01CJC.png</a>' %}

To approximate the square wave (in red), simple add together all the sine
waves. The low frequency blue wave builds most of the shape, and the high
frequency waves serve to square out the corners. It's hard to imagine what
removing the blue wave from the signal would look like, but it should be
clear that without that low frequency component, our signal is going
to change drastically.

To simulate the effect of sending a signal through a channel designed for
speech, we want to filter out frequencies outside of the range 300 Hz - 3400
Hz. Here's what it looks like when we apply this band pass filter to a stackmat
signal using Audacity.

The unfiltered signal:

{% include image.html src="dialup-stackmat/no-filter.png" alt="Unfiltered stackmat signal" %}

Frequency analysis of the stackmat signal (note the large quantity of low
frequency signals:

{% include image.html src="dialup-stackmat/no-filter-analysis.png" alt="Unfiltered stackmat signal frequency analysis" %}

Now apply the 300 Hz - 3400 Hz band pass filter. The resulting signal looks
very similar to the distorted signal we saw when plugging the stackmat into a
phone:

{% include image.html src="dialup-stackmat/band-pass-filter.png" alt="300 Hz - 3400 Hz band pass filter applied to stackmat signal" %}

And the resulting frequency analysis:

{% include image.html src="dialup-stackmat/band-pass-filter-analysis.png" alt="300 Hz - 3400 Hz band pass filter frequency analysis" %}

One day at work, Eithan
eithan shavit comes in, we decide that the problem is due to frequencies
outside of the frequency response curve of most phones

bought a modem!
{% include image.html src="dialup-stackmat/2014-03-14 21.42.27.jpg" alt="DS8500 eval kit" %}
{% include image.html src="dialup-stackmat/2014-03-18 22.20.40.jpg" alt="Eval kit wired up 1" %}
{% include image.html src="dialup-stackmat/2014-03-18 23.35.38.jpg" alt="Eval kit wired up 2" %}

show the signal

designed a board (copied and simplified http://datasheets.maximintegrated.com/en/ds/DS8500-KIT.pdf)

{% include image.html src="dialup-stackmat/FSKube_files/board_top.png" alt="Top view" %}
{% include image.html src="dialup-stackmat/FSKube_files/FSKube.brd.png" alt="Layout" %}
{% include image.html src="dialup-stackmat/FSKube_files/FSKube.sch.png" alt="Schematic" %}

<<< TODO - take a picture of the naked board

got it printed, bought the components

{% include image.html src="dialup-stackmat/2014-04-17 18.42.30.jpg" alt="wtf how do we solder this" %}
{% include image.html src="dialup-stackmat/2014-04-17 15.59.37.jpg" alt="Components placed, not soldered" %}

coworker was able to solder it, burned 1 board

{% include image.html src="dialup-stackmat/IMG_20140422_162324.jpg" alt="Boards with DS8500" %}

we (eithan) soldered the rest of the components on

{% include image.html src="dialup-stackmat/IMG_20140422_183302.jpg" alt="Eithan soldering" %}
{% include image.html src="dialup-stackmat/IMG_20140422_190723.jpg" alt="Eithan soldering back of board" %}

<<< show final board! >>>

i wrote a bunch of code to demodulate the signal (using zero crossing), it works, but probably could be improved on by someone who has actually studied DSP.
the code is all written in c++ and is compiled to javascript. should be able to use the NDK to write an android app, and IOS should be able to run the c++ directly.

## next steps?

* mass production?
* better design/case - output for display
* integration with a competition results system...

### thanks to everyone who supported me who i forgot to mention blah blah blah

>>>

### Demo

<iframe class="youtube" width="560" height="315" src="//www.youtube.com/embed/0M_GsnmY8Gs?rel=0" frameborder="0" allowfullscreen></iframe>
