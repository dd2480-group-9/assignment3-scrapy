# Report for assignment 3

This is a template for your report. You are free to modify it as needed.
It is not required to use markdown for your report either, but the report
has to be delivered in a standard, cross-platform format.

## Project

Name:

URL:

One or two sentences describing it

## Onboarding experience

Did it build and run as documented?
    
See the assignment for details; if everything works out of the box,
there is no need to write much here. If the first project(s) you picked
ended up being unsuitable, you can describe the "onboarding experience"
for each project, along with reason(s) why you changed to a different one.


## Complexity


#### 1. What are your results for five complex functions?
* `_next_request` got a CCN of 11 with manual counting using the formula $\pi-n+2$ while lizard got a CCN of 13. However, lizard caluclates the CCN by amount of decisions plus one. Using that formula with manual counting yield the same result of 13.
* `func`
* `func`
* `func`
* `func`
#### 2. Are the functions just complex, or also long?
All of the functions are only moderatly complex and for the most part also fairly short. There isn't a clear correlation between the CCN and NLOC.

#### 3. What is the purpose of the functions?
* `_next_request`: This function handles scheduling requests and error handling. It gets a bit complex because it has to manage several control flows and exceptions, which is just part of its job.
* `func`
* `func`
* `func`
* `func`

#### 4. Are exceptions taken into account in the given measurements?
Yes, lizard counts exceptions. Each except clause is considered a branch, thus increasing the cyclomatic complexity.

#### 5. Is the documentation clear w.r.t. all the possible outcomes?
The documentation explains the general behavior but could be improved to detail the outcomes of each branch. For many of the functions there are barely any docstrings or comments describing the code and different branching in the functions.

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
