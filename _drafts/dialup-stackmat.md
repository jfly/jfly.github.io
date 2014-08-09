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

I graduated from high school in 2006, and dedicated that summer to deciphering
the stackmat protocol. I'll never forget the thrill of zooming into a recording
and seeing a repeated wave form. I feared I'd see total chaos, or nothing.

{% include image.html alt="A stackmat signal I recorded ages ago" src="dialup-stackmat/signal.jpg" %}

After staring at screenshots from Audacity, I was eventually able to decode
stackmat signals by hand. At the time, I had no idea that I had just
essentially reverse engineered the ubiquitous
[RS-232](http://en.wikipedia.org/wiki/RS-232) standard. I knew that I wanted to
write code to interpret the signal, but I was overwhelmed and returned the
project to my backburner.

<<< went to berkeley, cs61a brian harvey, got enough confidence to code it up >>>

<<<
showed it off the berkeley cubers after the first berkeley competition
https://www.worldcubeassociation.org/results/c.php?i=Berkeley2006 chris hunt of
jnetcube was there http://sourceforge.net/projects/jnetcube/
AFAIK, i was the first to plug a stackmat into a soundcard, chris hunt had done
it with a serial cable before
>>>

<<<
that's basically the CCT story, talk about the rise of smartphones, and then square
talk about failed hackathon with kevin jorgensen, darren kwong, and Devin
Corr-Robinett @ berkeley hackathon 2012-02-16

eithan shavit comes in, we decide that the problem is due to frequencies
outside of the frequency response curve of most phones

bought a modem!
{% include image.html src="dialup-stackmat/2014-03-14 21.42.27.jpg" alt="DS8500 eval kit" %}
{% include image.html src="dialup-stackmat/2014-03-18 22.20.40.jpg" alt="Eval kit wired up 1" %}
{% include image.html src="dialup-stackmat/2014-03-18 23.35.38.jpg" alt="Eval kit wired up 2" %}

show the signal

designed a board

show the board design

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
* integration with a competition results system...

>>>

```python
def foo():
  print('foo')
```

### Demo

<iframe class="youtube" width="560" height="315" src="//www.youtube.com/embed/0M_GsnmY8Gs?rel=0" frameborder="0" allowfullscreen></iframe>
