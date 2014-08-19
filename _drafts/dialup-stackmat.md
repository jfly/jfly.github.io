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
needed a hardware guy <<<gah so many guys>>> to figure out what was going on. Fortunately, I work at a
hardware company. One day my coworker
[Eithan Shavit](http://www.eithanshavit.com/) caught me looking at pictures of
stackmat signals. As luck would have it, Eithan studied EE before getting a job in
software. He was interested in the problem, and had some ideas for fixing it. <<< the following explanation is all his or something?>>>

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

This begs the question: how do you translate the stackmat signal into the range
of frequencies that phones support? Turns out this problem (transmision of
digital bits over a link designed for human voice) has already been solved. You
use a modem!

The word modem is actually a portmanteau of the words modulator and
demodulator. The original modems used a modulation scheme called
[frequency-shift keying](http://en.wikipedia.org/wiki/Frequency-shift_keying)
(FSK) that is surprisingly simple. Pick two distinct frequencies. Call one your
mark frequency, it represents a binary 1. Call the other frequency your space
frequency, it represents a binary 0. Whenever your digital signal is a 1, send
the mark tone, and send the space tone for 0's.

{% include image.html src="dialup-stackmat/fsk.jpg" alt="<a href='http://ironbark.xtelco.com.au/subjects/DC/lectures/7/fig_2010_07_05.jpg'>FSK</a> encoding of a digital signal" %}

Eithan did some research, and discovered the [DS8500 HART
Modem](http://www.maximintegrated.com/en/products/interface/current-loop-products-4-20ma/DS8500.html).
He convinced me to purchase an [evaluation
kit](http://datasheets.maximintegrated.com/en/ds/DS8500-KIT.pdf).

{% include image.html src="dialup-stackmat/2014-03-14 21.42.27.jpg" alt="Unboxing the DS8500 evaluation kit" %}
{% include image.html src="dialup-stackmat/2014-03-18 23.35.38.jpg" alt="Wiring up the DS8500. This was confusing!" %}

The modem FSK encoding the output of a generation 2 stackmat stopped at 0.00:

{% include image.html src="dialup-stackmat/stackmat-fsk-gerty-nexus5-iphone3gs.png" alt="Output of the DS8500 as recorded by my desktop (gerty), a Nexus 5, and an iPhone 3Gs. The top row is the incoming digital signal, the output of a generation 2 stackmat stopped at 0.00." %}

The signals recorded by the phones are still slightly distorted, but it's still
easy to tell where the 0s are and where the 1s are. Having proven that the
DS8500 actually does what we want it to, we designed our own board (Eagle CAD
files available
[here](https://github.com/jfly/fskube/tree/gh-pages/hardware/eagle)).

{% include image.html src="dialup-stackmat/FSKube_files/board_top.png" alt="Top view" %}
{% include image.html src="dialup-stackmat/FSKube_files/FSKube.brd.png" alt="Layout" %}
{% include image.html src="dialup-stackmat/FSKube_files/FSKube.sch.png" alt="Schematic" %}

We used [OSH Park](https://oshpark.com/) to print the board, which required us
to order a minimum of three boards. Eithan wisely insisted that we purchase at
least two of each component.

{% include image.html src="dialup-stackmat/2014-08-19 02.02.50.jpg" alt="A board fresh from OSH park" %}

It wasn't until everything arrived that I realized just how small the DS8500 chip is. We had no idea how we were going to solder it to the board.

{% include image.html src="dialup-stackmat/2014-04-17 18.42.30.jpg" alt="wtf could this be any tinier?" %}

Fortunately, we found a coworker on the hardware team who does board work. Part
of his job includes soldering
[QFN](http://en.wikipedia.org/wiki/Quad_Flat_No-leads_package) packages. We
gave him two boards and our two DS8500 chips. He attempted to solder the first
one using a hot air gun, but the board cracked (he's used to working on Arista
boards, which are upwards of seven layers, whereas our board is a mere two). He
soldered the second chip by hand, which meant that he couldn't solder the
"bellypad" (the large metal contact visible in the previous picture).

{% include image.html src="dialup-stackmat/IMG_20140422_162324.jpg" alt="Boards with the DS8500 soldered on. Note that the lower right board is charred and cracked from the hot air treatment." %}

After that, it was a simple matter of letting Eithan do all the work.

{% include image.html src="dialup-stackmat/IMG_20140422_183302.jpg" alt="Eithan soldering the through hole components." %}
{% include image.html src="dialup-stackmat/IMG_20140422_190723.jpg" alt="Eithan soldering the back of the board." %}

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
