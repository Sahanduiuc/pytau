.. :changelog:

Release History
---------------

0.4.3 (2020-05-02)
++++++++++++++++++

- Added more unit tests
- Fixed build badge target URL

0.4.2 (2020-05-02)
++++++++++++++++++

- Added more unit tests
- Removed declared support for Python 3.6; missing asyncio functions

0.4.1 (2020-05-02)
++++++++++++++++++

- Added unit tests
- Integrated Azure DevOps build pipeline

0.4.0 (2020-04-30)
++++++++++++++++++

- Rewrote core graph functions using graph-theory; removed networkx dependency
- Properly fixed case where next sibling node activation skipped
- Added Network#attach() method to explicitly add a node to the graph without connecting it

0.3.1 (2020-04-26)
++++++++++++++++++

- Fixed case where next sibling node activation skipped

0.3.0 (2020-04-25)
++++++++++++++++++

- Added FlatMap operator

0.2.0 (2020-04-13)
++++++++++++++++++

- Switched back to Python 3.7.x

0.1.1 (2020-04-04)
+++++++++++++++++++

- Critical fix to setup.py to pick up package source
- Switch to using Do operator in hello_world.py example
- Improve the subscribe_trades.py example

0.1.0 (2020-04-04)
+++++++++++++++++++

- Remove dependency on APScheduler
- Rewrite to use asyncio internally
- Added websocket example
- Switched to require Python version >= 3.8

0.0.2 (2020-03-28)
+++++++++++++++++++

- Renamed OneShot to From and ForEach to Do
- Added BufferWithCount, BufferWithTime, Interval, Just and Scan operators
- Improved documentation

0.0.1 (2020-03-28)
+++++++++++++++++++

- Initial implementation
