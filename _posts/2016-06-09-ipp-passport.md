---
layout: post
title: IPP Passport
date: 2016-06-09
---

[Eitan Cher](http://www.eitancher.com/) handed this to me at a board game night on Monday:

{% include image.html alt="Closed IPP passport" src="/misc/ipp-passport/pics/passport-closed.jpg" %}

Inside were two maddening jigsaw puzzles designed by
[Rex Rossano Perez](http://www.twistypuzzles.com/cgi-bin/pdb-search.cgi?act=inv&key=392):

{% include image.html alt="Jigsaw puzzle" src="/misc/ipp-passport/pics/pattern.jpg" %}

Eitan created a beautiful laser cut plastic passport out of these two patterns.

The [Candian flag](https://en.wikipedia.org/wiki/Flag_of_Canada):

{% include image.html alt="Canadian flag" src="/misc/ipp-passport/pics/maple.jpg" %}

And the [Japanese flag](https://en.wikipedia.org/wiki/Flag_of_Japan):

{% include image.html alt="Japanese flag" src="/misc/ipp-passport/pics/sun.jpg" %}

Almost immediately, I knew I wasn't going to solve this puzzle by hand. During a flight to Wisconsin yesterday, I got a chance to code up a solution in Python 3
(see [GitHub](https://github.com/jfly/jfly.github.io/tree/b3d103ef174480a8104a73dff2283954fb5c886c/misc/ipp-passport#ipp-passport)).

To avoid spoilers, I won't post the solutions here, but you can find all the
solutions to the maple leaf
[here](https://github.com/jfly/jfly.github.io/blob/b3d103ef174480a8104a73dff2283954fb5c886c/misc/ipp-passport/maples.txt),
and all the solutions to the sun
[here](https://github.com/jfly/jfly.github.io/blob/b3d103ef174480a8104a73dff2283954fb5c886c/misc/ipp-passport/suns.txt).

My implementation was straightforward [BFS](https://github.com/jfly/jfly.github.io/blob/4e6b0d37fece47359ac48c02a33e796516bf85ed/misc/ipp-passport/search.py#L13-L17)
with some pruning
([if we ever end up in a position where we've created islands smaller than our smallest piece, there's no need to keep searching](https://github.com/jfly/jfly.github.io/blob/4e6b0d37fece47359ac48c02a33e796516bf85ed/misc/ipp-passport/board.py#L74-L85)).

I made no attempt to parallelize or to reduce via symmetry. Solving the maple
leaf starting with the stem took 6 minutes on my laptop, and the sun took 1.6
hours.

I used this as an opportunity to
try out some ideas that have been bouncing around in my head
since watching [this video on functional programming](https://skillsmatter.com/skillscasts/4971-domain-driven-design-with-scott-wlaschin).
I definitely want to try out a real functional programming language next.
