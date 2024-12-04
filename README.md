Videos we made using the GLRK4 Double Pendulums!

*100 Double Pendulums*

[![100 Double Pendulums](https://img.youtube.com/vi/9TLIVxt4TYo/0.jpg)](https://www.youtube.com/watch?v=9TLIVxt4TYo)

*Chaotic Art*

[![Chaos Art](https://img.youtube.com/vi/aP296WRKEqs/0.jpg)](https://www.youtube.com/watch?v=aP296WRKEqs)

**how to use**<br />
hi quick lil readme

just install the dependencies (pygame, matplotlib, scipy)
and just run whichever pendulum you'd like to use!

just drag whichever mass and drop, have fun!
100 Double Pendulums:

**the code**<br />
play with delta_t, you should find better results the smaller delta_t is.

also, there is no fps cap, so sim may look unstable, add a clock = pygame.tick.Clock() before the while loop
then in the while loop, at the end, add a clock.tick(120).

also chaos_art.py, chaos_study.py, butterfly_effect.py are just for fun, try to run it,
but it may be slow!