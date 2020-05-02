Design
======

Fetcher
-------

Initially the fetcher will just be single-threaded, but eventually, it will
work with a threadpool that will fetch feeds in parallel.

The fetcher must cleanly deal with the following cases:

* Is the feed being redirected to another feed?
* Has the feed actually been updated?
* Is the feed still present?
* Is the feed actually parseable?
