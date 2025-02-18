# Report for assignment 3

## Project

**Name:** Scrapy

**URL:** [https://github.com/scrapy/scrapy](https://github.com/scrapy/scrapy)

**Description:** *An open source and collaborative framework for extracting the data you need from websites. In a fast, simple, yet extensible way.*


## Onboarding experience

How easily can you build the project? Brieﬂy describe if everything worked as documented or not:

**(a) Did you have to install a lot of additional tools to build the software?**  
No. Only standard Python tools (like pip) were needed. For testing [tox](https://tox.wiki/en/latest/index.html) was needed and to automatically address simple code issues before every commit [pre-commit](https://pre-commit.com/) was needed.

**(b) Were those tools well documented?**  
Yes. The required tools are well documented on the contribution guide with links to the respective tools. It could have been helptful with a summary of tools needed to get started though since no package manager is used for development and each tool need to be installed individually.

**(c) Were other components installed automatically by the build script?**  
Yes. Dependencies are automatically handled via the build configuration.

**(d) Did the build conclude automatically without errors?**  
Yes. The build process completed automatically without errors.

**(e) How well do examples and tests run on your system(s)?**  
The examples and tests run smoothly on supported systems.


## Complexity

1. What are your results for five complex functions?
   * Did all methods (tools vs. manual count) get the same result?
   * Are the results clear?
2. Are the functions just complex, or also long?
3. What is the purpose of the functions?
4. Are exceptions taken into account in the given measurements?
5. Is the documentation clear w.r.t. all the possible outcomes?

## Refactoring

Plan for refactoring complex code:

Estimated impact of refactoring (lower CC, but other drawbacks?).

Carried out refactoring (optional, P+):

git diff ...

## Coverage

### Tools

Document your experience in using a "new"/different coverage tool.

How well was the tool documented? Was it possible/easy/difficult to
integrate it with your build environment?

### Your own coverage tool

Show a patch (or link to a branch) that shows the instrumented code to
gather coverage measurements.

The patch is probably too long to be copied here, so please add
the git command that is used to obtain the patch instead:

git diff ...

What kinds of constructs does your tool support, and how accurate is
its output?

### Evaluation

1. How detailed is your coverage measurement?

2. What are the limitations of your own tool?

3. Are the results of your tool consistent with existing coverage tools?

## Coverage improvement

Show the comments that describe the requirements for the coverage.

Report of old coverage: [link]

Report of new coverage: [link]

Test cases added:

git diff ...

Number of test cases added: two per team member (P) or at least four (P+).

## Self-assessment: Way of working

Current state according to the Essence standard: ...

Was the self-assessment unanimous? Any doubts about certain items?

How have you improved so far?

Where is potential for improvement?

## Overall experience

What are your main take-aways from this project? What did you learn?

Is there something special you want to mention here?
