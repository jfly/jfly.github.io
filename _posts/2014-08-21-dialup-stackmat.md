---
layout: post
title: Dialup Stackmat
date: 2014-08-21
hidden: true
---

For those of you who have never been to a Rubik's Cube competition, they are
controlled chaos. It goes something like this:

1. A competitor is called to bring up his solved cube and place it on a blank
   scorecard.
2. A scrambler scrambles that cube, using the scorecard to determine which
   scramble to give the competitor.
3. A runner carries that scrambled cube to a timing station along with the scorecard.
4. At the timing station, a judge performs the judging ritual
prescribed in the
[WCA regulations](https://www.worldcubeassociation.org/regulations/#A3).
5. The judge writes the competitor's solve time on the scorecard.
   Both the judge and the competitor sign the sheet.
6. A runner carries the competitor's scorecard and solved cube back to the
   scrambling station.
7. Repeat steps 2-6 until the competitor has done all of his solves.
8. The completed scorecard is given to a staff member whose sole job is to
   manually enter all the times into a computer.

Data entry is a mind-numbing, error-prone job.
[C.A.L. Cube Timer (CCT)]({% post_url 2014-08-20-cct %}) leveraged the
stackmat's display port to plug stackmats into computers. Why not do the same
thing to automate data entry at competitions?

As a matter of fact, this has been done. Back in 2012, a group of Polish programmers built a
custom piece of hardware to interface with the stackmat and provide live
results at a competition. The project is called
[opencubeware](https://www.facebook.com/opencubeware). Unfortunately, there
isn't much information about it on the Facebook group, and their website
[www.opencubeware.org](http://www.opencubeware.org/) is currently a
blank page.

How do they handle multiple ongoing rounds? What
device aggregates the results from all the devices? What form of wireless do
they use to communicate with that box? What's security like? It looks like
the devices are battery powered, how long do they last on battery? How do you program the id cards? Most importantly, how much does everything cost?

Opencubeware is a truly impressive feat of engineering, but I'm convinced it's
not the right direction for us to go. The devices appear to be wireless, and there's no discussion of security. It's also unclear how you handle multiple ongoing rounds with the minimal ui. Today, smartphones are ubiquitous and *cheap*.
I believe we can build a more secure, reliable, easy to use results system on
commodity cell phones than we could ever achieve by building our own custom device.
It's easier to create an android app than it is to write firmware for a
microcontroller. Furthermore, touch screens allow for a better, more flexible
user interface, and phones already have Wi-Fi, cameras, and some even support NFC.

Why hasn't this already been done? Unfortunately, it turns out that plugging a
stackmat into a phone isn't as straightforward as plugging a stackmat into a
computer (as CCT did).

[Dan Cohen](https://www.worldcubeassociation.org/results/p.php?i=2007COHE01)
wrote a stackmat interpreter in Objective-C in July 2010. He got it working in
the iPhone simulator on his computer, but when he loaded it onto his
phone, it just didn't work. The signal he recorded was so distorted as to be unreadable.

{% include image.html src="dialup-stackmat/dan-cohen-signals.png" alt="Dan Cohen's distorted signal" %}

In February 2012, I attended a hackathon at Berkeley with the intent of writing a
stackmat to phone interpreter. I was joined by
[Kevin Jorgensen](https://www.worldcubeassociation.org/results/p.php?i=2006JORG01),
[Darren Kwong](https://www.worldcubeassociation.org/results/p.php?i=2005KWON01),
and [Devin Corr-Robinett](https://www.worldcubeassociation.org/results/p.php?i=2006CORR01).
After a few hours, we ran into the distortion that had thwarted Dan Cohen.

{% include image.html src="dialup-stackmat/1.15_iphone3gs.png" alt="Distorted signal on an iPhone 3Gs" %}

I'm a software guy. This signal filled me with a combination of dread and
regret that I had not attended more of Professor Boser's 8am EE42 lectures.
Unable to proceed without a better understanding of what was going on, we gave up.

It wasn't until January 2014 that I revisited the problem. One day at work, my
coworker
[Eithan Shavit](http://www.eithanshavit.com/) caught me looking at pictures of
stackmat signals. As luck would have it, Eithan studied Electrical Engineering
before getting a job in software. He was interested in the distorted signal and
was able to shed some light on what was going on.

Amazingly enough, phones are designed to record human voice.
Human speech contains a large range of frequencies, approximately
[300 Hz to 3400 Hz](http://en.wikipedia.org/wiki/Voice_frequency),
to understand what somebody is saying. 
Phones can drop frequencies outside of that range if they want to, but they
*must* preserve all frequencies within that range.

Unfortunately, the digital data that comes out of a stackmat looks nothing like a speech signal.
To conceptualize what a phone does when it receives the square waves of the
stackmat signal, it is necessary to visualize the square wave in terms of its
component frequencies. This exercise is known as [Fourier
analysis](http://en.wikipedia.org/wiki/Fourier_analysis). Fortunately,
Wikipedia has already done this for us.

{% include image.html src="dialup-stackmat/Squarewave01CJC.png" alt='Components of a square wave. From <a href=\'http://en.wikipedia.org/wiki/File:Squarewave01CJC.png\'>http://en.wikipedia.org/wiki/File:Squarewave01CJC.png</a>' %}

To approximate the square wave (in red), add together all the component sine
waves. The low frequency blue wave builds most of the shape, and the higher
frequency waves serve to square out the corners. It's hard to imagine what
removing the blue wave from the signal would look like, but it should be
clear that without that low frequency component, our signal is going
to change dramatically.

To simulate the effect of sending a signal through a channel designed for
speech, we want to remove frequencies outside of the range 300 Hz to 3400
Hz. Audacity makes it easy to perform this experiment.

{% include image.html src="dialup-stackmat/no-filter.png" alt="Unfiltered stackmat signal" %}

{% include image.html src="dialup-stackmat/no-filter-analysis.png" alt="Unfiltered stackmat signal frequency analysis. Note the bias towards low frequency signals." %}

Now we apply a band pass filter that attenuates all frequencies between 300 Hz and
3400 Hz. Note that we're not harshly cutting off all frequencies outside of
this range, they are dampened instead. This is a reasonable approximation of
what happens in the real world: devices gradually lose sensitivity to
frequencies outside of their operating range, rather than dropping off entirely.
The resulting signal looks very similar to the distorted signal we saw when
plugging the stackmat into a phone!

{% include image.html src="dialup-stackmat/band-pass-filter.png" alt="300 Hz - 3400 Hz band pass filter applied to stackmat signal" %}

{% include image.html src="dialup-stackmat/band-pass-filter-analysis.png" alt="300 Hz - 3400 Hz band pass filter frequency analysis. Note that a lot of the higher frequencies are gone, and the very lowest frequencies have dropped off." %}

If you're interested in how different phones handle the stackmat signal, please
see [all these signals I've collected](/stackmat-phones/).

This begs the question: how do you translate the stackmat signal into a range
of frequencies that phones do support? It turns out this problem (transmission of
digital bits over a link designed for human voice) has already been solved.
You use a modem!

The word modem is actually a portmanteau of the words modulator and
demodulator. The original modems used a modulation scheme called
[frequency-shift keying](http://en.wikipedia.org/wiki/Frequency-shift_keying)
(FSK) that is surprisingly simple. Pick two distinct frequencies. Call one your
mark frequency, it represents a binary 1. Call the other your space
frequency, it represents a binary 0. Whenever your digital signal is a 1, send
the mark tone, and whenever your digital signal is a 0, send the space tone.
If the mark and space frequencies you chose are within the range of frequencies
that phones support, you're golden.

{% include image.html src="dialup-stackmat/fsk.jpg" alt="<a href='http://ironbark.xtelco.com.au/subjects/DC/lectures/7/fig_2010_07_05.jpg'>FSK</a> encoding of a digital signal" %}

In the previous picture, the top signal represents the stackmat signal. The
"mo" part of a modem would take this signal and produce the wavy bottom signal
(FSK encoded). We then run the FSK encoded signal into a stackmat, which
would then recover the original bits by doing frequency analysis in software.

Eithan did some research, and discovered the
[DS8500 HART Modem](http://www.maximintegrated.com/en/products/interface/current-loop-products-4-20ma/DS8500.html).
It produces frequencies of 1200 Hz and 2200 Hz, perfect for a phone.
I was very skeptical that it would be able to speak the digital signal
stackmats produce, but measurements of the stackmat's digital output voltage
were exactly the voltages the
[DS8500 data sheet](http://datasheets.maximintegrated.com/en/ds/DS8500.pdf)
asks for. The chip is only $12, why not give it a shot?

Unfortunately, using chips is not as simple as plug and play. Among other
things, the DS8500 requires an input signal of 3.6864 MHz.
Easy, run a current over a piece of quartz, and then filter the output of
that through some capacitors. Also resistors. Apparently you need resistors
everywhere (I'm convinced that resistors don't actually do anything other than
cost a few pennies and look cool). This was quickly getting out of hand.

Suffice to say, reading the DS8500 data sheet
and distilling that information into a working board requires a degree in EE.
Eithan could do it, but he wasn't sure he could get it right the first time.
Fortunately, you can purchase an
[evaluation kit](http://datasheets.maximintegrated.com/en/ds/DS8500-KIT.pdf)
that has all the necessary components soldered to a DS8500 for you. For $46.86
after tax, the evaluation kit is a rip off (all the components on the board cost
pennies, and the chip costs ~$12), but it let us verify the chip without
the time and risk of designing and soldering our own board.

{% include image.html src="dialup-stackmat/2014-03-14 21.42.27.jpg" alt="Unboxing the DS8500 evaluation kit" %}
{% include image.html src="dialup-stackmat/2014-03-18 23.35.38.jpg" alt="Wiring up the DS8500. This was tricky!" %}

You can see a stackmat plugged into the modem above. I connected the output of
the modem into my desktop, Nexus 5, and iPhone 3Gs and recorded the incoming signal.

{% include image.html src="dialup-stackmat/stackmat-fsk-gerty-nexus5-iphone3gs.png" alt="Output of the DS8500 as recorded by my desktop (gerty), a Nexus 5, and an iPhone 3Gs. The top row is the incoming digital signal, the output of a generation 2 stackmat stopped at 0.00." %}


Success!!! The signals recorded by the phones are slightly distorted (we're
still not sure why), but it's easy to tell where the 0s and 1s are.  Having
proven that the DS8500 does what we want it to, it was time to design our own
board (Eagle CAD files available
[here](https://github.com/jfly/fskube/tree/gh-pages/hardware/eagle)).

{% include image.html src="dialup-stackmat/FSKube_files/board_top.png" alt="Top view" %}
{% include image.html src="dialup-stackmat/FSKube_files/FSKube.brd.png" alt="Layout" %}
{% include image.html src="dialup-stackmat/FSKube_files/FSKube.sch.png" alt="Schematic" %}

We used [OSH Park](https://oshpark.com/) to print the board, which required us
to order a minimum of three boards. Eithan wisely insisted that we purchase at
least two of each component. Everything for one board cost $26 (see our [bill of
materials](https://docs.google.com/spreadsheets/d/1-2u8-NUTNEA3l2xFZdgK0my_7DUBfUnJsI4Eo2_YHuk/edit?usp=sharing)).
If we move onto mass production, the price should go down significantly.

{% include image.html src="dialup-stackmat/board-fresh-from-osh-park.jpg" alt="A board fresh from OSH park" %}

It wasn't until everything arrived that we realized just how small the DS8500 chip is. We had no idea how we were going to solder it to the board.

{% include image.html src="dialup-stackmat/2014-04-17 18.42.30.jpg" alt="Could this be any tinier please?" %}

Fortunately, we found a coworker on the hardware team who does board work. Part
of his job includes soldering these ridiculous
[TQFN](http://en.wikipedia.org/wiki/Quad_Flat_No-leads_package) packages. We
gave him two of our boards and our two DS8500 chips. He attempted to solder the first
one using a hot air gun, but the board cracked (our two layer board is a lot
thinner than the boards he is used to working with). He
soldered the second chip by hand, which meant that he couldn't solder the
"bellypad" (the large metal contact visible in the previous picture). Since the
bellypad is labelled as a ground, and many of the contacts on the outside of
the chip are also labelled as ground, we hoped that just soldering the outside
would be good enough.

{% include image.html src="dialup-stackmat/IMG_20140422_162324.jpg" alt="Boards with the DS8500 soldered on. Note that the lower right board is charred and cracked from the hot air treatment." %}

After that, it was a simple matter of letting Eithan do all the work.

{% include image.html src="dialup-stackmat/IMG_20140422_183302.jpg" alt="Eithan soldering the through hole components." %}
{% include image.html src="dialup-stackmat/IMG_20140422_190723.jpg" alt="Military precision" %}

Neither board worked at first. The board design called for an LED to indicate
when the modem is turned on. The combination of modem and LED drew more power
than our battery could supply. After removing the LED, the burnt board still
didn't work, presumably because the modem had been damaged by the heat.

This left us with one working board.

{% include image.html src="dialup-stackmat/finished-board.jpg" alt="The finished board." %}

With our custom board in hand, I wrote code to demodulate the FSK signal
(see [jfly/fskube](https://github.com/jfly/fskube)). All that
code is written in C++, and compiles to Javascript with
[Emscripten](https://github.com/kripken/emscripten). This is what powers the
web demo  at [http://www.jflei.com/fskube/](http://www.jflei.com/fskube/).
Since the code is written in C++, it will be easy to develop an iOS app if we
want to.
[Patricia Li](https://www.worldcubeassociation.org/results/p.php?i=2009LIPA01),
Darren Kwong, and I have already written an Android app using the
[Android NDK](https://developer.android.com/tools/sdk/ndk/index.html).

### Demo

<iframe class="youtube" width="560" height="315" src="//www.youtube.com/embed/ZFWurXR_X2I?rel=0" frameborder="0" allowfullscreen></iframe>

This is just the beginning. There is a lot of work to do before we can
run a competition with our phones. I aim to start running small practice
competitions with the Berkeley Cube Club in early 2015. I intend to see this
project though until it can be used at a large scale competition such as US
Nationals or Worlds.

## Next steps

* Test on more devices, especially iPhones.
* Design a new board for mass production. If you happen to know anything about
getting boards mass produced, please drop me a line! I'm very out of my element
here.
* Integration with a live results system for WCA competitions.

## Acknowledgements

* Eithan Shavit for teaching me everything I know about hardware and
  electricity (that's still not very much, but that's not his fault).
* Patricia Li for encouragement and for proof reading. She also wrote the skeleton
  of the Android demo app.
