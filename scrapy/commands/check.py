import argparse
import time
from collections import defaultdict
from unittest import TextTestResult as _TextTestResult
from unittest import TextTestRunner

from scrapy.commands import ScrapyCommand
from scrapy.contracts import ContractsManager
from scrapy.utils.conf import build_component_list
from scrapy.utils.misc import load_object, set_environ
from tests import coverage_data


class TextTestResult(_TextTestResult):
    def printSummary(self, start: float, stop: float) -> None:
        write = self.stream.write
        writeln = self.stream.writeln

        run = self.testsRun
        plural = "s" if run != 1 else ""

        writeln(self.separator2)
        writeln(f"Ran {run} contract{plural} in {stop - start:.3f}s")
        writeln()

        infos = []
        if not self.wasSuccessful():
            write("FAILED")
            failed, errored = map(len, (self.failures, self.errors))
            if failed:
                infos.append(f"failures={failed}")
            if errored:
                infos.append(f"errors={errored}")
        else:
            write("OK")

        if infos:
            writeln(f" ({', '.join(infos)})")
        else:
            write("\n")


class Command(ScrapyCommand):
    requires_project = True
    default_settings = {"LOG_ENABLED": False}

    def syntax(self) -> str:
        return "[options] <spider>"

    def short_desc(self) -> str:
        return "Check spider contracts"

    def add_options(self, parser: argparse.ArgumentParser) -> None:
        super().add_options(parser)
        parser.add_argument(
            "-l",
            "--list",
            dest="list",
            action="store_true",
            help="only list contracts, without checking them",
        )
        parser.add_argument(
            "-v",
            "--verbose",
            dest="verbose",
            default=False,
            action="store_true",
            help="print contract tests for all spiders",
        )

    def run(self, args: list[str], opts: argparse.Namespace) -> None:
        # load contracts
        contracts = build_component_list(self.settings.getwithbase("SPIDER_CONTRACTS"))
        conman = ContractsManager(load_object(c) for c in contracts)
        # runner = TextTestRunner(verbosity=2 if opts.verbose else 1) #1, 2
  
        if opts.verbose: #0
            verbosity = 2
            coverage_data["run"][0] = True
        else: #1
            verbosity = 1
            coverage_data["run"][1] = True
        
        runner = TextTestRunner(verbosity=verbosity)

        result = TextTestResult(runner.stream, runner.descriptions, runner.verbosity)

        # contract requests
        contract_reqs = defaultdict(list)

        assert self.crawler_process
        spider_loader = self.crawler_process.spider_loader

        with set_environ(SCRAPY_CHECK="true"):
            for spidername in args or spider_loader.list(): #2
                
                spidercls = spider_loader.load(spidername)
                spidercls.start_requests = lambda s: conman.from_spider(s, result) # type: ignore[assignment,method-assign,return-value]

                tested_methods = conman.tested_methods_from_spidercls(spidercls)

                if opts.list: #3
                    for method in tested_methods: #4
                        contract_reqs[spidercls.name].append(method)
                        coverage_data["run"][4] = True
                    coverage_data["run"][3] = True
                elif tested_methods: #5
                    self.crawler_process.crawl(spidercls)
                    coverage_data["run"][5] = True
                coverage_data["run"][2] = True

            # start checks
            if opts.list: #6
                for spider, methods in sorted(contract_reqs.items()): #7
                    if not methods and not opts.verbose: #8
                        coverage_data["run"][8] = True
                        continue
                    print(spider)
                    for method in sorted(methods): #9
                        print(f"  * {method}")
                        coverage_data["run"][9] = True
                    coverage_data["run"][7] = True
                coverage_data["run"][6] = True
            else: #10
                start = time.time()
                self.crawler_process.start()
                stop = time.time()

                result.printErrors()
                result.printSummary(start, stop)

                #self.exitcode = int(not result.wasSuccessful()) #12
                if result.wasSuccessful():  # Branch 11 
                    coverage_data["run"][11] = True
                    self.exitcode = 0
                else:  # Branch 12
                    coverage_data["run"][12] = True
                    self.exitcode = 1
                coverage_data["run"][10] = True
