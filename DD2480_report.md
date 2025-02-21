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

Plan for refactoring complex code:

Estimated impact of refactoring (lower CC, but other drawbacks?).

Carried out refactoring (optional, P+):

git diff ...

### Plan for _parse_sitemap
The _parse_sitemap function handles multiple responsibilities and can be refactored into smaller helper functions, each focused on a specific task. This would improve testability, debugging, and readability, while also lowering the overall complexity. Although the core implementation may not need improvement, breaking it into smaller, single-purpose functions will reduce complexity and make the code easier to manage. So the refactoring could be done in may ways perhaps, but could be divided into new helper functions and the _parse_sitemap  function with only simple if statements and calls to the helpers. These parts can be as the following: 

### Check if response URL 
 ```python  
   if response.url.endswith("/robots.txt"):
    ...
``` 
This early check is good to identify if the URL is from robots.txt. To simplify the logic and improve clarity, we could extract this check into its own helper function (for example  _is_robots_txt_url)

### Fetching and Validating Sitemap Body
 ```python  
     else:
       ...
```
Same here, the if statement inside the else is creating a complicated application and can therefore be separated. The else could remain and then call a helper function implementing this part (for example _process_sitemap_body)

### Processing sitemap
 ```python  
 
            if s.type == "sitemapindex":
                for loc in iterloc(it, self.sitemap_alternate_links):
                    if any(x.search(loc) for x in self._follow):
                        yield Request(loc, callback=self._parse_sitemap)
            elif s.type == "urlset":
                for loc in iterloc(it, self.sitemap_alternate_links):
                    for r, c in self._cbs:
                        if r.search(loc):
                            yield Request(loc, callback=c)
                            break
 ```

Here again i would try to implement the inside of the if and elif in different helper functions. 

### sidemap index
 ```python  

for loc in iterloc(it, self.sitemap_alternate_links):
                    if any(x.search(loc) for x in self._follow):
                        yield Request(loc, callback=self._parse_sitemap)
 ```  
This part of the function  _parse_sitemap  can be refactored as a new helper function returning back to the original parse_sitemap where the first decition is being made. Therefore reducing the CC (for example the helper function could be _processing_sidemap)

### URL set 
 ```python  
for loc in iterloc(it, self.sitemap_alternate_links):
                    for r, c in self._cbs:
                        if r.search(loc):
                            yield Request(loc, callback=c)
                            break
 ```
Here its the same thing, this would be called from the _parse_sitemap function and could be implemented as something like  process_URL_links


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
