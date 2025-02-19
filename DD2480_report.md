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
Yes. The required tools are well documented on the contribution guide with links to the respective tools. It could have been helptful with a summary of tools needed to get started those tools needed to be installed individually and the information was a little bit spread out in the contribution documentation.

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

### Plan for `_next_request`:
The `_next_request`function handles the engine workflow. Although the code isn’t overly complex and refactoring isn’t strictly necessary, extracting some logic into helper functions could improve clarity and lower the CCN of the function.`_next_request` can be divided into four main parts:

#### Early checks:
```python
if self.slot is None:
    return

assert self.spider is not None  # typing

if self.paused:
    return
```
These initial checks are reasonable to keep at the beginning of the function. Depending on how the cyclomatic complexity is calculated, they might not even affect the CCN. However, you could extract these into a helper function (for example `_can_process_request`) that encapsulates all the early conditions.

#### Scheduler handling
```python
while (
    not self._needs_backout()
    and self._next_request_from_scheduler() is not None
):
    pass
```
This loop waits until there are no scheduler requests before proceeding. Although it’s not very complex and fits well in the function, extracting it into its own helper (for example `_process_scheduler_requests`) could make the overall functionality of `_next_request` more focused.


#### Processing next requests
```python
if self.slot.start_requests is not None and not self._needs_backout():
    try:
        request_or_item = next(self.slot.start_requests)
    except StopIteration:
        self.slot.start_requests = None
    except Exception:
        self.slot.start_requests = None
        logger.error(
            "Error while obtaining start requests",
            exc_info=True,
            extra={"spider": self.spider},
        )
    else:
        if isinstance(request_or_item, Request):
            self.crawl(request_or_item)
        elif is_item(request_or_item):
            self.scraper.start_itemproc(request_or_item, response=None)
        else:
            logger.error(
                f"Got {request_or_item!r} among start requests. Only "
                f"requests and items are supported. It will be "
                f"ignored."
            )
```
This is the core part of the function that handles processing the next request. It’s suggested to keep this section within `_next_request` since it’s central to its purpose, though you might consider extracting parts of the error handling if it becomes more complex in teh future.

#### Idle-State handling
```python
if self.spider_is_idle() and self.slot.close_if_idle:
    self._spider_idle()
```
This final section handles the idle state of the spider. Even though it isn’t overly complex, moving it to a dedicated helper function (for example `_handle_idle_state`) could make the code more coherent and improve readability.

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
