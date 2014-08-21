---
layout: post
title: Dialup Stackmat
date: 2014-08-21
hidden: true
---

It started with a coincidence: the
[stackmat](http://www.speedstacks.com/store/retail/speed-stacks-stackmat-pro-timer/)
and the
[TI-83+](http://education.ti.com/en/us/products/calculators/graphing-calculators/ti-83-plus/features/features-summary)
have the same 2.5mm communication port.

If you haven't heard of a stackmat, it's the timer used in Rubik's cube
competitions. I first played with one at [Caltech Spring
2005](https://www.worldcubeassociation.org/results/c.php?i=CaltechSpring2005).
After the competition, I convinced my mom to buy me one.

Before I started speedcubing, I was
[very into calculator programming](/about#ti). Outside of the
time I spent using my beloved TI-83+ to do actual math, I spent hundreds of
hours and untold AAA batteries programming on that overpriced device with its
cramped keyboard. When I learned that some people had managed to
[wire a PS/2 keyboard to their calculators](http://www.radicalsoft.org/hardware/keyboard/),
it was something I *had* to try out. I bought all the components needed for the
project, but a general lack of EE knowledge
meant that I never actually got the project working, and my mom eventually made
me move the mess into our garage.

The upshot of all this is (was? <<<) that when my stackmat arrived, I already
had the adapter and cables to plug my stackmat into my computer via the
microphone jack.

{% include image.html alt="My original stackmat and detritus from the abandoned TI-83+ PS/2 keyboard project" src="dialup-stackmat/stackmat.jpg" %}

I wanted to practice with my new stackmat, but I also wanted to keep track of
my times without manually entering them into my computer. I scoured
the internet for a program to interpret the sound of my stackmat.
To my great surprise, I couldn't find any! To this day, I believe I was the first
person to try this.

I graduated from high school in 2006, and spent some time that summer deciphering
the stackmat protocol. I'll never forget the thrill of zooming into a recording
and seeing a repeated wave form.

{% include image.html alt="A stackmat signal I recorded ages ago" src="dialup-stackmat/signal.jpg" %}

After a long time staring at screenshots from Audacity, I was able to decode
stackmat signals by hand (many years later, I learned that I had reverse engineered
the [RS-232](http://en.wikipedia.org/wiki/RS-232) standard).
Friends and other projects kept me from writing a software signal
interpreter that summer. It wasn't until I had settled into my freshman year of
college that I finally sat down and coded a truly awful, barely working
stackmat interpreter in Java.

I kept this project secret, confiding only in [Darren
Kwong](https://www.worldcubeassociation.org/results/p.php?i=2005KWON01).
I decided to demonstrate my work at Berkeley's first Rubik's Cube competition,
[Berkeley Fall 2006](https://www.worldcubeassociation.org/results/c.php?i=Berkeley2006).
Of course, that didn't happen. I had never staffed a
competition before, but there's rarely a moment of free time. Berkeley's first
competition was no exception. Fortunately, we
all met up at
[Dan Dzoan](https://www.worldcubeassociation.org/results/p.php?i=2006DZOA03)'s
apartment afterwards, and I was able to show off my hard work.
I like to think that people were impressed and excited about my work, but I honestly only remember the reactions of two people:
[Chris Hunt](https://www.worldcubeassociation.org/results/p.php?i=2005HUNT01),
and [Ryan Zheng](https://www.worldcubeassociation.org/results/p.php?i=2006ZHEN02).

Chris Hunt is <<<was?>>> the creator of the legendary JNetCube. At the time,
almost every cuber I knew used JNetCube. He proposed adding my stackmat support to
it, and I remember being honored by the opportunity to contribute to a real
piece of software that other people use.

I'm sure I would have become a contributor to JNetCube if not for Ryan Zheng.
Ryan wanted to see my awful code, and then felt compelled to improve it.
He eventually pulled out his own laptop, and we decended into a full night of hacking.
That night lengthened into a full weekend. At one
point, Ryan suggested the unthinkable: rather than just giving this feature to
JNetCube, we could build our own superior timer! That moment was the birth of
[C.A.L. Cube Timer (CCT)](http://cct.cubing.net/).

Since the beginning, there was talk of incorporating CCT into Rubik's Cube
competitions. Such talk could never get past the fact that
you would need a computer at every single judging station, an organizational
nightmare. However, in recent years, smartphones have become
so ubiquitous that I believe it is time for this dream to become a reality.
Companies like [Square](https://squareup.com/) have proven that it is feasible
to plug a device into the headset jack of a smartphone and run a business.
There is no reason not to do the same at cube competitions! Why hasn't this
already been done? Unfortunately, it turns out that plugging a stackmat into a
phone isn't as straightforward as plugging a stackmat into a computer.

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
regret that I had not attended more of Professor Boser's 8am EE42 lectures.
Fortunately, I work at a hardware company. One day my coworker
[Eithan Shavit](http://www.eithanshavit.com/) caught me looking at pictures of
stackmat signals. As luck would have it, Eithan studied EE before getting a job in
software. He was interested in the problem, and had some ideas for fixing it. <<< the following explanation is all his or something?>>>

Amazingly enough, phones are designed to record human voice. Human speech contains
a large range of frequencies, but you only need to listen to a small
range of those frequencies to understand what somebody is saying. That range of
frequencies is approximately [300 Hz to 3400
Hz](http://en.wikipedia.org/wiki/Voice_frequency). Phones aren't necessarily
built to record frequencies outside of that range.

The digital data that comes out of a stackmat looks nothing like human voice.
To conceptualize what a phone does when it receives the square waves of the
stackmat signal, it is necessary to visualize the square wave in terms of its
component frequencies. This exercise is known as [Fourier
analysis](http://en.wikipedia.org/wiki/Fourier_analysis). Fortunately,
Wikipedia has already done this for us.

{% include image.html src="dialup-stackmat/Squarewave01CJC.png" alt='Components of a square wave. From <a href=\'http://en.wikipedia.org/wiki/File:Squarewave01CJC.png\'>http://en.wikipedia.org/wiki/File:Squarewave01CJC.png</a>' %}

To approximate the square wave (in red), add together all the component sine
waves. The low frequency blue wave builds most of the shape, and the high
frequency waves serve to square out the corners. It's hard to imagine what
removing the blue wave from the signal would look like, but it should be
clear that without that low frequency component, our signal is going
to change dramatically.

To simulate the effect of sending a signal through a channel designed for
speech, we want to remove frequencies outside of the range 300 Hz to 3400
Hz. Audacity makes it easy to perform this experiment.

The unfiltered signal:

{% include image.html src="dialup-stackmat/no-filter.png" alt="Unfiltered stackmat signal" %}

Frequency analysis of the stackmat signal (note the large quantity of low
frequency signals:

{% include image.html src="dialup-stackmat/no-filter-analysis.png" alt="Unfiltered stackmat signal frequency analysis" %}

Now apply a band pass filter that removes all frequencies between 300 Hz and 3400 Hz. The resulting signal looks
very similar to the distorted signal we saw when plugging the stackmat into a
phone:

{% include image.html src="dialup-stackmat/band-pass-filter.png" alt="300 Hz - 3400 Hz band pass filter applied to stackmat signal" %}

And the resulting frequency analysis:

{% include image.html src="dialup-stackmat/band-pass-filter-analysis.png" alt="300 Hz - 3400 Hz band pass filter frequency analysis" %}

This begs the question: how do you translate the stackmat signal into a range
of frequencies that phones do support? It turns out this problem (transmision of
digital bits over a link designed for human voice) has already been solved.
Use a modem!

The word modem is actually a portmanteau of the words modulator and
demodulator. The original modems used a modulation scheme called
[frequency-shift keying](http://en.wikipedia.org/wiki/Frequency-shift_keying)
(FSK) that is surprisingly simple. Pick two distinct frequencies. Call one your
mark frequency, it represents a binary 1. Call the other your space
frequency, it represents a binary 0. Whenever your digital signal is a 1, send
the mark tone, and whenever your digital signal is a 0, send the space tone.

{% include image.html src="dialup-stackmat/fsk.jpg" alt="<a href='http://ironbark.xtelco.com.au/subjects/DC/lectures/7/fig_2010_07_05.jpg'>FSK</a> encoding of a digital signal" %}

Eithan did some research, and discovered the
[DS8500 HART Modem](http://www.maximintegrated.com/en/products/interface/current-loop-products-4-20ma/DS8500.html).
He convinced me to purchase an
[evaluation kit](http://datasheets.maximintegrated.com/en/ds/DS8500-KIT.pdf).

{% include image.html src="dialup-stackmat/2014-03-14 21.42.27.jpg" alt="Unboxing the DS8500 evaluation kit" %}
{% include image.html src="dialup-stackmat/2014-03-18 23.35.38.jpg" alt="Wiring up the DS8500. This was confusing!" %}

You can see a stackmat plugged into the modem above. I connected the output of
the modem into my desktop, Nexus 5, and iPhone 3Gs and recorded the signals below:

{% include image.html src="dialup-stackmat/stackmat-fsk-gerty-nexus5-iphone3gs.png" alt="Output of the DS8500 as recorded by my desktop (gerty), a Nexus 5, and an iPhone 3Gs. The top row is the incoming digital signal, the output of a generation 2 stackmat stopped at 0.00." %}


Success!! The signals recorded by the phones are slightly distorted (we're
still not sure why), but it's easy to tell where the 0s and 1s are.  Having
proven that the DS8500 does what we want it to, we designed our own
board (Eagle CAD files available
[here](https://github.com/jfly/fskube/tree/gh-pages/hardware/eagle)).

{% include image.html src="dialup-stackmat/FSKube_files/board_top.png" alt="Top view" %}
{% include image.html src="dialup-stackmat/FSKube_files/FSKube.brd.png" alt="Layout" %}
{% include image.html src="dialup-stackmat/FSKube_files/FSKube.sch.png" alt="Schematic" %}

We used [OSH Park](https://oshpark.com/) to print the board, which required us
to order a minimum of three boards. Eithan wisely insisted that we purchase at
least two of each component (<<< link to BOM? include price estimate here).

<<< TODO take a better picture, this one is shit >>>

{% include image.html src="dialup-stackmat/2014-08-19 02.02.50.jpg" alt="A board fresh from OSH park" %}

It wasn't until everything arrived that we realized just how small the DS8500 chip is. We had no idea how we were going to solder it to the board.

{% include image.html src="dialup-stackmat/2014-04-17 18.42.30.jpg" alt="Could this be any tinier please?" %}

Fortunately, we found a coworker on the hardware team who does board work. Part
of his job includes soldering these ridiculous
[TQFN](http://en.wikipedia.org/wiki/Quad_Flat_No-leads_package) packages. We
gave him two boards and two DS8500 chips. He attempted to solder the first
one using a hot air gun, but the board cracked (our two layer board is a lot
thinner than the boards he is used to working with). He
soldered the second chip by hand, which meant that he couldn't solder the
"bellypad" (the large metal contact visible in the previous picture).

{% include image.html src="dialup-stackmat/IMG_20140422_162324.jpg" alt="Boards with the DS8500 soldered on. Note that the lower right board is charred and cracked from the hot air treatment." %}

After that, it was a simple matter of letting Eithan do all the work.

{% include image.html src="dialup-stackmat/IMG_20140422_183302.jpg" alt="Eithan soldering the through hole components." %}
{% include image.html src="dialup-stackmat/IMG_20140422_190723.jpg" alt="Eithan soldering the back of the board." %}

Neither board worked at first. The board design called for an LED to indicate
when the modem is turned on. The combination of modem and LED drew more power
than our battery could supply. After removing the LED, the burnt board still
didn't work, presumably because the modem had been damaged by the heat.

This left us with one working board:

<<< show final board! >>>

With the hardware in hand, I wrote code to demodulate the FSK signal
(see [jfly/fskube](https://github.com/jfly/fskube)). All that
code is written in C++, and compiles to Javascript with
[Emscripten](https://github.com/kripken/emscripten). This is what powers the
web demo  at [http://www.jflei.com/fskube/](http://www.jflei.com/fskube/).
Since the code is written in C++, it will be easy to develop iOS and Android
apps without having to rewrite anything.

### Demo!

<<< TODO - record a better video with actual commentary >>>

<iframe class="youtube" width="560" height="315" src="//www.youtube.com/embed/0M_GsnmY8Gs?rel=0" frameborder="0" allowfullscreen></iframe>

## Next steps

* Test on more devices, especially iPhones.
* Design a new board for mass production. If you happen to know anything about
getting boards mass produced, please drop me a line! I'm very out of my element
here.
* Integration with a live results system for WCA competitions.

Thanks for reading! <<< more bland, please
