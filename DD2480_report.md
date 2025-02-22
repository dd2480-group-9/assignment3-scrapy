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

#### 1. What are your results for five complex functions?
* `_next_request` got a CCN of 11 with manual counting using the formula $\pi-n+2$ while lizard got a CCN of 13. However, lizard caluclates the CCN by amount of decisions plus one. Using that formula with manual counting yield the same result of 13.
* `run` got a cyclomatic complexity of 14 using the radon tool, which uses the formula 1 + number of decisions. By using the same formula, the complexity was calculated by hand to be 14 as well. 
* `_parse_sitemap` got a CC of 12 with the lizard tool, that uses the formula 1 + number of decisions. By using the same formula, the complexity was calculated by hand to be 12 as well. 
* `get_func_args` got a complexity of 11 using lizard. When manually calculated the result was 11 as well by using the formula 1 + number of decisions where number of decisions was 10. 
* `dataReceived` the number of decisions was 10 using manual counting, while lizard returned 11 because it used the formula number of decisions + 1. The results from lizard align with the manual count. 

#### 2. Are the functions just complex, or also long?
All of the functions are only moderatly complex and for the most part also fairly short. There isn't a clear correlation between the CCN and NLOC.

#### 3. What is the purpose of the functions?
* `_next_request`: This function handles scheduling requests and error handling. It gets a bit complex because it has to manage several control flows and exceptions, which is just part of its job.
* `run`: The run function loads and executes contract tests for spiders. It gets complex due to it handling both contract-tested methods and contract-based spider tests. 
* `_parse_sitemap`: This function is responsible for parsing sitemaps (either from a website or a robots.txt file) and extracting URLs that need to be processed further by the crawler.
* `get_func_args`. This function returns the list of the arguments of a calleble. The high CC does not come from the functionality of the function which is taking the arguments from a function. It comes from handling edge cases, exceptions, and etc.
* `dataReceived`: This function runs contract tests, either executing the tests and reporting results, or listing which spider methods are available for testing.

#### 4. Are exceptions taken into account in the given measurements?
Yes, lizard and Radon counts exceptions. Each except clause is considered a branch, thus increasing the cyclomatic complexity.

#### 5. Is the documentation clear w.r.t. all the possible outcomes?
The documentation explains the general behavior but could be improved to detail the outcomes of each branch. For many of the functions there are barely any docstrings or comments describing the code and different branching in the functions.


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


### Plan for `dataReceived`:
The `dataReceived` function is not complex since the  CCN is 11. However, diving the function into smaller bits of code may improve the clarity and reveal potential improvements for the code complexity. The function can be divided into 5 parts. 

```python
    def dataReceived(self, bodyBytes: bytes) -> None:
        # Return early if finished
        if self._finished.called:
            return

        assert self.transport
        self._update_body_buffer(bodyBytes)
        self._check_download_stop_signal(bodyBytes)
        self._check_max_size()
        self._check_warn_size()

    def _update_body_buffer(self, bodyBytes: bytes) -> None:
        self._bodybuf.write(bodyBytes)
        self._bytes_received += len(bodyBytes)

    def _check_download_stop_signal(self, bodyBytes: bytes) -> None:
        bytes_received_result = self._crawler.signals.send_catch_log(
            signal=signals.bytes_received,
            data=bodyBytes,
            request=self._request,
            spider=self._crawler.spider,
        )
        for handler, result in bytes_received_result:
            if isinstance(result, Failure) and isinstance(result.value, StopDownload):
                self._handle_download_stop(handler, result)

    def _handle_download_stop(self, handler, result) -> None:
        logger.debug(
            "Download stopped for %(request)s from signal handler %(handler)s",
            {"request": self._request, "handler": handler.__qualname__},
        )
        self.transport.stopProducing()
        self.transport.loseConnection()
        failure = result if result.value.fail else None
        self._finish_response(flags=["download_stopped"], failure=failure)

    def _check_max_size(self) -> None:
        if self._maxsize and self._bytes_received > self._maxsize:
            logger.warning(
                "Received (%(bytes)s) bytes larger than download max size (%(maxsize)s) in request %(request)s.",
                {
                    "bytes": self._bytes_received,
                    "maxsize": self._maxsize,
                    "request": self._request,
                },
            )
            self._bodybuf.truncate(0)
            self._finished.cancel()

    def _check_warn_size(self) -> None:
        if self._warnsize and self._bytes_received > self._warnsize and not self._reached_warnsize:
            self._reached_warnsize = True
            logger.warning(
                "Received more bytes than download warn size (%(warnsize)s) in request %(request)s.",
                {"warnsize": self._warnsize, "request": self._request},
            )

```
Diving the function into 5 different sub-functions allows enhanced readability and error handling. 


### Plan for _parse_sitemap
The _parse_sitemap function handles multiple responsibilities and can be refactored into smaller helper functions, each focused on a specific task. This would improve testability, debugging, and readability, while also lowering the overall complexity. Although the core implementation may not need improvement, breaking it into smaller, single-purpose functions will reduce complexity and make the code easier to manage. So the refactoring could be done in may ways perhaps, but could be divided into new helper functions and the _parse_sitemap  function with only simple if statements and calls to the helpers. These parts can be as the following: 

#### Check if response URL 
 ```python  
   if response.url.endswith("/robots.txt"):
    ...
``` 
This early check is good to identify if the URL is from robots.txt. To simplify the logic and improve clarity, we could extract this check into its own helper function (for example  _is_robots_txt_url)

#### Fetching and Validating Sitemap Body
 ```python  
     else:
       ...
```
Same here, the if statement inside the else is creating a complicated application and can therefore be separated. The else could remain and then call a helper function implementing this part (for example _process_sitemap_body)

#### Processing sitemap
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

#### sidemap index
 ```python  

for loc in iterloc(it, self.sitemap_alternate_links):
                    if any(x.search(loc) for x in self._follow):
                        yield Request(loc, callback=self._parse_sitemap)
 ```  
This part of the function  _parse_sitemap  can be refactored as a new helper function returning back to the original parse_sitemap where the first decition is being made. Therefore reducing the CC (for example the helper function could be _processing_sidemap)

#### URL set 
 ```python  
for loc in iterloc(it, self.sitemap_alternate_links):
                    for r, c in self._cbs:
                        if r.search(loc):
                            yield Request(loc, callback=c)
                            break
 ```
Here its the same thing, this would be called from the _parse_sitemap function and could be implemented as something like  process_URL_links

### Plan for `get_func_args`:

The `get_func_args` function returns the arguments of a function. The complexity of the function does not come from its functionality, but it comes from the checks that is made for edge cases. However, using helper functions can improve readability and makes it easy to test the functions while not necessarily improving complexity.

#### Retrieving Signature:
```python
    def get_signature(func: Callable[..., Any]) -> inspect.Signature:
        try:
            return inspect.signature(func)
        except ValueError:
            return None
```
This will handle signature retrieval from a callable.

#### Filtering Partial Arguments:
```python
    def filter_partial_args(sig: inspect.Signature, partial_func: partial) -> list[str]:   
        partial_args = partial_func.args
        partial_kw = partial_func.keywords or {}
        filtered_args = []
        for name, param in sig.parameters.items():
            if param.name in partial_args:
                continue
            if param.name in partial_kw:
                continue
            filtered_args.append(name)
        return filtered_args
```
This will take the signature, the partial.args, and partial.keywords, and return the filtered list of parameter names.

#### Stripping Self:
```python
def strip_self(args: list[str]) -> list[str]:
    return args[1:] if args and args[0] == "self" else args
```
This will remove self from args if needed.

#### Main Function:
```python
def get_func_args(func: Callable[..., Any], stripself: bool = False) -> list[str]:
    if not callable(func):
        raise TypeError(f"func must be callable, got '{type(func).__name__}'")

    sig = get_signature(func)
    if sig is None:
        return []

    if isinstance(func, partial):
        args = filter_partial_args(sig, func)
    else:
        args = list(sig.parameters)

    if stripself:
        args = strip_self(args)
    return args
```
Now the main function is easy to read, test, and modify when needed. Since the complexity was necessary due to checks, readability is improved but complexity stays similar.

### Plan for 'run' 

The run function includes many if statements, which increases the complexity. It also handles several things, such as setting up the test environment, processing spiders, handling contract requests and running tests. These could be broken down into several different methods, according to the following structure:

```python 
    def setup_test_environment(self, opts: argparse.Namespace):
        contracts = build_component_list(self.settings.getwithbase("SPIDER_CONTRACTS"))
        conman = ContractsManager(load_object(c) for c in contracts)
        verbosity = 2 if opts.verbose else 1
        runner = TextTestRunner(verbosity=verbosity)
        result = TextTestResult(runner.stream, runner.descriptions, runner.verbosity)
    return conman, result

    def process_spiders(self, args: list[str], opts: argparse.Namespace, conman, result):
        contract_reqs = defaultdict(list)

        assert self.crawler_process
        spider_loader = self.crawler_process.spider_loader

        with set_environ(SCRAPY_CHECK="true"):
            for spidername in args or spider_loader.list():  
                spidercls = spider_loader.load(spidername)
                spidercls.start_requests = lambda s: conman.from_spider(s, result)

                tested_methods = conman.tested_methods_from_spidercls(spidercls)

                if opts.list:
                    for method in tested_methods:
                        contract_reqs[spidercls.name].append(method)
                elif tested_methods:
                    self.crawler_process.crawl(spidercls)

    return contract_reqs

    def handle_contract_logging(self, contract_reqs, opts):
        for spider, methods in sorted(contract_reqs.items()):
            if not methods and not opts.verbose:
                continue
            print(spider)
            for method in sorted(methods):
                print(f"  * {method}")

    def execute_tests(self, result):
        start = time.time()
        self.crawler_process.start()
        stop = time.time()

        result.printErrors()
        result.printSummary(start, stop)

        if result.wasSuccessful():
            self.exitcode = 0
        else:
            self.exitcode = 1
   ```
By breaking down the function into four helper methods where each method only handles one task makes it easier to test and debug. It also reduces the overall complexity to be an average of 4.25 instead of 14. 


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

1. How detailed is your coverage measurement? It is not sufficiently detailed and it is destructive to the codebase. 

2. What are the limitations of your own tool? The tools we have are targeted toward a single function, therefore, it is inefficient. 

3. Are the results of your tool consistent with existing coverage tools? Yes

## Coverage improvement

Show the comments that describe the requirements for the coverage.

Report of old coverage: [link]

Report of new coverage: [link]

Test cases added:

git diff ...

Number of test cases added: two per team member (P) or at least four (P+).

## Self-assessment: Way of working

Current state according to the Essence standard: In-place (The whole team is involved in the inspection and adaptation of the way-of-working)

Was the self-assessment unanimous? Any doubts about certain items? Yes, the self-assessment was unanimous. Other than the way-of-working, there were no doubts.

How have you improved so far? We have learned how to use git, write unit tests, structure repositories, and enhance our collaboration skills. 

Where is potential for improvement? Our group needs to communicate more and meet on-site to distribute the tasks evenly and avoid chaos.

## Overall experience

What are your main takeaways from this project? What did you learn? We learned the risks and challenges of using open-source projects. We also taught ourselves to improvise and apply such projects to our use. 

Is there something special you want to mention here? Don't EVER use push force, especially the day before the deadline. 
