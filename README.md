# Timeline miner

Basically, this tiny ML/NLP application accessible through a single page based on Python/Django and Spacy, inspired from:

- https://www.qualicen.de/natural-language-processing-timeline-extraction-with-regexes-and-spacy/
- hhttp://jsdatav.is/chap05.html

Otherwise, based on algorithm and UI from both, I reworked the algorithm with a big plus, finding the best split in timeline and colorize splits. See my discussion here https://datascience.stackexchange.com/q/85231/107273

It is to mention the current split mechanism is a brute force looking for best continuous sub-arrays with minimal standard deviation. 

### UI

Timeline for McDonald's history

![Timeline](../master/Capture.PNG)

### Examples

Through some random examples, you can see some bugs of functionality; So yes, so much work to do.

[Featured examples](/examples/)

### Contribution

Please see open issues, fork and pull request after manually testing some CSV files:

One good example for input:

Any Wikipedia summary (Introduction section) that has some historical dates. for example:

- https://en.wikipedia.org/wiki/McDonald%27s
- https://en.wikipedia.org/wiki/Nike,_Inc.
- Or anything else.

#### Test

There is obviously no automated testing now, It would be nice to create one for extreme values.

#### Collaboration and todos

- Automated tests
- Decouple code for readibility
- Revise split mechanism
- Better UI (probably with themes) and better code export

(See open issues)
(Please for any deployment, keep it fair and mention this repository)

#### Deployment

Python run django project.

It is deployed with no automation for tests here timeline-miner.herokuapp.com (limited resources).
